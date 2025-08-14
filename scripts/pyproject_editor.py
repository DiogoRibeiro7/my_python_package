#!/usr/bin/env python
"""
pyproject_editor.py

A small, typed CLI to update `pyproject.toml` safely:
- Works with both Poetry (`[tool.poetry]`) and PEP 621 (`[project]`).
- Preserves formatting and comments via tomlkit.
- Subcommands:
    * bump-version {major,minor,patch}
    * set-dep <name> <spec> [--group <group>]
    * remove-dep <name> [--group <group>]
    * set-python <spec>
    * print (pretty-prints the effective model)

Examples:
    python scripts/pyproject_editor.py bump-version patch
    python scripts/pyproject_editor.py set-dep numpy "^1.26"
    python scripts/pyproject_editor.py set-dep ruff "^0.5" --group dev
    python scripts/pyproject_editor.py remove-dep numpy
    python scripts/pyproject_editor.py set-python ">=3.10,<3.13"
    python scripts/pyproject_editor.py print --check
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from difflib import unified_diff
from pathlib import Path
from typing import Literal, Optional, Tuple

import tomlkit
from tomlkit.toml_document import TOMLDocument

VersionBump = Literal["major", "minor", "patch"]


@dataclass(frozen=True)
class Paths:
    root: Path
    pyproject: Path


def _ensure_file(p: Path) -> None:
    if not p.exists():
        raise FileNotFoundError(f"File not found: {p}")
    if not p.is_file():
        raise IsADirectoryError(f"Expected a file, got directory: {p}")


def _load_doc(path: Path) -> TOMLDocument:
    text = path.read_text(encoding="utf-8")
    return tomlkit.parse(text)


def _dump_doc(doc: TOMLDocument) -> str:
    # tomlkit returns a string preserving formatting/comments
    return tomlkit.dumps(doc)


def _detect_layout(doc: TOMLDocument) -> Literal["poetry", "pep621"]:
    """
    Return which layout the pyproject uses for metadata:
    - "poetry" if [tool.poetry] exists
    - "pep621" if [project] exists
    We prefer Poetry if both exist.
    """
    if "tool" in doc and isinstance(doc["tool"], dict) and "poetry" in doc["tool"]:
        return "poetry"
    if "project" in doc:
        return "pep621"
    raise ValueError("Unsupported pyproject: neither [tool.poetry] nor [project] found.")


def _get_version(doc: TOMLDocument) -> str:
    layout = _detect_layout(doc)
    if layout == "poetry":
        v = doc["tool"]["poetry"].get("version")
    else:
        v = doc["project"].get("version")
    if not isinstance(v, str):
        raise ValueError("Version is missing or not a string.")
    return v


def _set_version(doc: TOMLDocument, version: str) -> None:
    layout = _detect_layout(doc)
    if layout == "poetry":
        doc["tool"]["poetry"]["version"] = version
    else:
        doc["project"]["version"] = version


_version_re = re.compile(r"^(?P<maj>\d+)\.(?P<min>\d+)\.(?P<pat>\d+)(?P<rest>.*)?$")


def _bump_semver(v: str, level: VersionBump) -> str:
    """
    Minimal semantic version bump for MAJOR.MINOR.PATCH[rest].
    'rest' (like -rc.1) is dropped on bump to keep things predictable.
    """
    m = _version_re.match(v)
    if not m:
        raise ValueError(f"Version '{v}' is not MAJOR.MINOR.PATCH[pre].")
    maj, min_, pat = int(m["maj"]), int(m["min"]), int(m["pat"])
    if level == "major":
        maj, min_, pat = maj + 1, 0, 0
    elif level == "minor":
        min_, pat = min_ + 1, 0
    elif level == "patch":
        pat = pat + 1
    else:
        raise ValueError(f"Unknown bump level: {level}")
    return f"{maj}.{min_}.{pat}"


def _get_poetry_dep_table(doc: TOMLDocument, group: Optional[str]) -> tomlkit.items.Table:
    """
    Return a writable table for dependencies in Poetry layout.
    Supports:
      - main deps: [tool.poetry.dependencies]
      - dev deps (legacy): [tool.poetry.dev-dependencies]
      - named groups: [tool.poetry.group.<group>.dependencies]
    """
    tool = doc.setdefault("tool", tomlkit.table())
    poetry = tool.setdefault("poetry", tomlkit.table())
    if group is None or group == "main":
        return poetry.setdefault("dependencies", tomlkit.table())

    # Poetry 1.2+ group
    group_tbl = poetry.setdefault("group", tomlkit.table())
    g = group_tbl.setdefault(group, tomlkit.table())
    return g.setdefault("dependencies", tomlkit.table())


def _ensure_pep621_arrays(doc: TOMLDocument) -> Tuple[tomlkit.items.Array, tomlkit.items.Table]:
    """
    Return (project.dependencies Array, project.optional-dependencies Table).
    Create them if missing.
    """
    project = doc.setdefault("project", tomlkit.table())
    deps = project.setdefault("dependencies", tomlkit.array())  # type: ignore[assignment]
    opt = project.setdefault("optional-dependencies", tomlkit.table())
    # Typing guards:
    if not isinstance(deps, tomlkit.items.Array):
        raise TypeError("[project.dependencies] must be an array.")
    if not isinstance(opt, tomlkit.items.Table):
        raise TypeError("[project.optional-dependencies] must be a table.")
    return deps, opt


def _set_dep(doc: TOMLDocument, name: str, spec: str, group: Optional[str]) -> None:
    """
    Set or update a dependency across layouts.
    - Poetry: name = {version = spec} or name = spec (string)
    - PEP 621: strings like "name spec" in arrays
    """
    layout = _detect_layout(doc)
    if layout == "poetry":
        deps = _get_poetry_dep_table(doc, group)
        # Use simple string pin if spec looks like a simple constraint; Poetry supports both forms.
        deps[name] = spec
        return

    # PEP 621
    deps, opt = _ensure_pep621_arrays(doc)
    target_array = deps if (group is None or group == "main") else opt.setdefault(group, tomlkit.array())
    if not isinstance(target_array, tomlkit.items.Array):
        raise TypeError(f"[project.optional-dependencies.{group}] must be an array.")

    # Replace existing line if package already present
    pk_prefix = f"{name} "
    new_line = f"{name} {spec}"
    found_idx = None
    for i, item in enumerate(list(target_array)):  # make a copy to avoid iterator issues
        if isinstance(item, str) and (item == name or item.startswith(pk_prefix)):
            found_idx = i
            break
    if found_idx is not None:
        target_array[found_idx] = new_line
    else:
        target_array.append(new_line)


def _remove_dep(doc: TOMLDocument, name: str, group: Optional[str]) -> bool:
    """
    Remove a dependency. Returns True if removed, False if not found.
    """
    layout = _detect_layout(doc)
    if layout == "poetry":
        deps = _get_poetry_dep_table(doc, group)
        if name in deps:
            del deps[name]
            return True
        return False

    # PEP 621
    deps, opt = _ensure_pep621_arrays(doc)
    arrays = []
    if group is None or group == "main":
        arrays.append(deps)
    else:
        arrays.append(opt.get(group))
    removed = False
    for arr in arrays:
        if not isinstance(arr, tomlkit.items.Array):
            continue
        keep = []
        for item in arr:
            if isinstance(item, str) and (item == name or item.startswith(f"{name} ")):
                removed = True
            else:
                keep.append(item)
        # Replace contents
        while len(arr) > 0:
            del arr[0]
        for k in keep:
            arr.append(k)
    return removed


def _set_python_constraint(doc: TOMLDocument, spec: str) -> None:
    """
    Set Python constraint:
    - Poetry: [tool.poetry.dependencies].python = "<spec>"
    - PEP 621: [project].requires-python = "<spec>"
    """
    layout = _detect_layout(doc)
    if layout == "poetry":
        tool = doc.setdefault("tool", tomlkit.table())
        poetry = tool.setdefault("poetry", tomlkit.table())
        deps = poetry.setdefault("dependencies", tomlkit.table())
        deps["python"] = spec
        return

    project = doc.setdefault("project", tomlkit.table())
    project["requires-python"] = spec


def _write_or_diff(path: Path, old_text: str, new_text: str, check: bool) -> int:
    if check:
        diff = "".join(unified_diff(old_text.splitlines(True), new_text.splitlines(True),
                                    fromfile=str(path), tofile=str(path)))
        sys.stdout.write(diff)
        return 0
    path.write_text(new_text, encoding="utf-8")
    return 0


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Safely edit pyproject.toml")
    parser.add_argument("--file", default="pyproject.toml", help="Path to pyproject.toml")
    parser.add_argument("--check", action="store_true",
                        help="Do not write; print a unified diff of proposed changes.")

    sub = parser.add_subparsers(dest="cmd", required=True)

    b = sub.add_parser("bump-version", help="Bump semantic version")
    b.add_argument("level", choices=["major", "minor", "patch"], type=str)

    sd = sub.add_parser("set-dep", help="Set or update a dependency")
    sd.add_argument("name", type=str)
    sd.add_argument("spec", type=str, help='Version constraint, e.g. "^1.26" or ">=1.0,<2.0"')
    sd.add_argument("--group", type=str, default=None, help='Dependency group (Poetry: "dev", or PEP 621 optional group)')

    rd = sub.add_parser("remove-dep", help="Remove a dependency")
    rd.add_argument("name", type=str)
    rd.add_argument("--group", type=str, default=None)

    sp = sub.add_parser("set-python", help="Set Python version constraint")
    sp.add_argument("spec", type=str, help='e.g. ">=3.10,<3.13"')

    sub.add_parser("print", help="Pretty-print normalized metadata")

    args = parser.parse_args(argv)

    pyproject = Path(args.file)
    _ensure_file(pyproject)
    before = pyproject.read_text(encoding="utf-8")
    doc = _load_doc(pyproject)

    if args.cmd == "bump-version":
        current = _get_version(doc)
        new = _bump_semver(current, args.level)  # type: ignore[arg-type]
        _set_version(doc, new)

    elif args.cmd == "set-dep":
        if not args.name.strip():
            raise ValueError("Dependency name cannot be empty.")
        if not args.spec.strip():
            raise ValueError("Spec cannot be empty.")
        _set_dep(doc, args.name.strip(), args.spec.strip(), args.group)

    elif args.cmd == "remove-dep":
        removed = _remove_dep(doc, args.name.strip(), args.group)
        if not removed:
            print(f"Dependency '{args.name}' not found.", file=sys.stderr)

    elif args.cmd == "set-python":
        _set_python_constraint(doc, args.spec.strip())

    elif args.cmd == "print":
        # For now, we just re-dump (preserves comments). Could add normalization.
        sys.stdout.write(_dump_doc(doc))
        return 0

    else:
        parser.error("Unknown command")  # unreachable with argparse choices

    after = _dump_doc(doc)
    if before == after:
        # Nothing changed; still show diff in --check mode for transparency.
        return _write_or_diff(pyproject, before, after, args.check)

    return _write_or_diff(pyproject, before, after, args.check)


if __name__ == "__main__":
    sys.exit(main())
