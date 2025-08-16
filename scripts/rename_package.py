#!/usr/bin/env python3
"""Rename the project package.

This helper script updates common project files when renaming a Python package.
It performs a simple search and replace on text files and renames the source
package directory.

Usage:
    python scripts/rename_package.py old_name new_name

Both ``old_name`` and ``new_name`` should be given using the distribution name
form (hyphens allowed). The script will automatically convert them to module
names by replacing hyphens with underscores when updating imports and source
folders.
"""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable

TEXT_EXTENSIONS = {
    ".py",
    ".toml",
    ".md",
    ".rst",
    ".txt",
    ".yaml",
    ".yml",
    ".ini",
    ".cfg",
    ".json",
    "Makefile",
    "Dockerfile",
    "",
}


def iter_text_files(root: Path) -> Iterable[Path]:
    """Yield text files under ``root`` excluding the ``.git`` directory."""
    for path in root.rglob("*"):
        if path.is_dir() or ".git" in path.parts:
            continue
        ext = path.suffix
        if path.name in TEXT_EXTENSIONS or ext in TEXT_EXTENSIONS:
            try:
                path.read_text()
            except UnicodeDecodeError:
                continue
            yield path


def replace_in_file(path: Path, replacements: dict[str, str]) -> None:
    content = path.read_text()
    new_content = content
    for old, new in replacements.items():
        new_content = new_content.replace(old, new)
    if new_content != content:
        path.write_text(new_content)


def main() -> None:
    parser = argparse.ArgumentParser(description="Rename Python package in project")
    parser.add_argument("old_name", help="Current package name (distribution form)")
    parser.add_argument("new_name", help="New package name (distribution form)")
    args = parser.parse_args()

    old_dist = args.old_name
    new_dist = args.new_name
    old_mod = old_dist.replace("-", "_")
    new_mod = new_dist.replace("-", "_")
    old_cli = old_mod.replace("_", "-")
    new_cli = new_mod.replace("_", "-")

    project_root = Path(__file__).resolve().parent.parent

    # Rename source directory
    src = project_root / "src"
    old_pkg_dir = src / old_mod
    new_pkg_dir = src / new_mod
    if old_pkg_dir.exists() and not new_pkg_dir.exists():
        old_pkg_dir.rename(new_pkg_dir)

    replacements = {
        old_dist: new_dist,
        old_mod: new_mod,
        old_cli: new_cli,
    }

    for file in iter_text_files(project_root):
        replace_in_file(file, replacements)


if __name__ == "__main__":
    main()
