#!/usr/bin/env python
"""
Check docstring coverage in the project.

This script inspects Python modules, classes, and functions to ensure
they have proper docstrings. It reports items that are missing docstrings
and provides an overall coverage percentage.

Usage:
    python scripts/check_docstring_coverage.py [--min-coverage PERCENTAGE]

Examples:
    # Check docstring coverage
    python scripts/check_docstring_coverage.py

    # Check and fail if below 80%
    python scripts/check_docstring_coverage.py --min-coverage 80
"""

import ast
import os
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Dict, List, NamedTuple, Optional, Set, Tuple


class DocItem(NamedTuple):
    """Information about a Python module item that should have a docstring."""

    name: str
    path: str
    lineno: int
    type: str  # "module", "class", or "function"
    has_docstring: bool


def is_public(name: str) -> bool:
    """
    Check if a name is public (not starting with underscore).

    Args:
        name: The name to check

    Returns:
        True if the name is public, False otherwise
    """
    return not name.startswith("_") or (
        name.startswith("__") and name.endswith("__")
    )  # Special methods are public


def should_have_docstring(node: ast.AST, include_all: bool = False) -> bool:
    """
    Determine if a node should have a docstring based on our standards.

    Args:
        node: The AST node to check
        include_all: Whether to include all items or just public ones

    Returns:
        True if the node should have a docstring, False otherwise
    """
    if isinstance(node, ast.Module):
        return True
    if isinstance(node, ast.ClassDef):
        return include_all or is_public(node.name)
    if isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
        # Skip property setters and simple properties
        if hasattr(node, "decorator_list"):
            for decorator in node.decorator_list:
                if isinstance(decorator, ast.Name) and decorator.id == "property":
                    if len(node.body) <= 2:  # Simple property getter
                        return False
                if isinstance(decorator, ast.Attribute) and decorator.attr == "setter":
                    return False
        if node.name == "__init__" and len(node.body) <= 2:
            # Skip simple __init__ methods that just assign attributes
            return False
        return include_all or is_public(node.name)
    return False


def get_docstring(node: ast.AST) -> Optional[str]:
    """
    Extract docstring from an AST node.

    Args:
        node: The AST node to extract docstring from

    Returns:
        The docstring if present, None otherwise
    """
    try:
        if not node.body:
            return None
        first_node = node.body[0]
        if isinstance(first_node, ast.Expr) and isinstance(first_node.value, ast.Str):
        if isinstance(first_node, ast.Expr):
            if (
                isinstance(first_node.value, ast.Str)
                or (isinstance(first_node.value, ast.Constant) and isinstance(first_node.value.value, str))
            ):
                return first_node.value.s if hasattr(first_node.value, "s") else first_node.value.value
        return None
    except (AttributeError, IndexError):
        return None


def check_file_docstrings(file_path: Path, include_all: bool = False) -> List[DocItem]:
    """
    Check docstring coverage for a Python file.

    Args:
        file_path: Path to the Python file
        include_all: Whether to check all items or just public ones

    Returns:
        List of DocItem instances for each item that should have a docstring
    """
    with open(file_path, "r", encoding="utf-8") as f:
        try:
            tree = ast.parse(f.read(), filename=str(file_path))
        except SyntaxError:
            print(f"Syntax error in {file_path}")
            return []

    results: List[DocItem] = []

    # Check module docstring
    module_has_doc = bool(get_docstring(tree))
    if should_have_docstring(tree, include_all):
        results.append(
            DocItem(
                name=file_path.stem,
                path=str(file_path),
                lineno=1,
                type="module",
                has_docstring=module_has_doc,
            )
        )

    # Check classes and functions
    for node in ast.walk(tree):
        if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            if should_have_docstring(node, include_all):
                item_type = "class" if isinstance(node, ast.ClassDef) else "function"
                has_doc = bool(get_docstring(node))
                results.append(
                    DocItem(
                        name=node.name,
                        path=str(file_path),
                        lineno=node.lineno,
                        type=item_type,
                        has_docstring=has_doc,
                    )
                )

        # Check methods inside classes
        if isinstance(node, ast.ClassDef):
            for item in node.body:
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    if should_have_docstring(item, include_all):
                        has_doc = bool(get_docstring(item))
                        results.append(
                            DocItem(
                                name=f"{node.name}.{item.name}",
                                path=str(file_path),
                                lineno=item.lineno,
                                type="method",
                                has_docstring=has_doc,
                            )
                        )

    return results


def check_directory_docstrings(
    directory: Path, include_all: bool = False, exclude: Optional[Set[str]] = None
) -> Tuple[List[DocItem], Dict[str, float]]:
    """
    Check docstring coverage for all Python files in a directory.

    Args:
        directory: Directory to check
        include_all: Whether to check all items or just public ones
        exclude: Set of directory names to exclude

    Returns:
        Tuple of (all DocItems, stats by type)
    """
    if exclude is None:
        exclude = {
            "__pycache__",
            ".git",
            ".github",
            "venv",
            ".venv",
            "build",
            "dist",
            ".mypy_cache",
            ".pytest_cache",
            ".ruff_cache",
        }

    all_results: List[DocItem] = []
    for root, dirs, files in os.walk(directory):
        # Skip excluded directories
        dirs[:] = [d for d in dirs if d not in exclude]

        for file in files:
            if file.endswith(".py"):
                file_path = Path(root) / file
                results = check_file_docstrings(file_path, include_all)
                all_results.extend(results)

    # Calculate statistics
    stats: Dict[str, Dict[str, int]] = {"module": {}, "class": {}, "function": {}, "method": {}}
    for item in all_results:
        stats.setdefault(item.type, {})
        stats[item.type].setdefault("total", 0)
        stats[item.type].setdefault("with_docstring", 0)

        stats[item.type]["total"] += 1
        if item.has_docstring:
            stats[item.type]["with_docstring"] += 1

    # Calculate percentages
    percentages: Dict[str, float] = {}
    total_items = 0
    total_with_docs = 0

    for item_type, counts in stats.items():
        if counts.get("total", 0) > 0:
            percentage = (counts.get("with_docstring", 0) / counts["total"]) * 100
            percentages[item_type] = percentage
            total_items += counts["total"]
            total_with_docs += counts.get("with_docstring", 0)

    if total_items > 0:
        percentages["overall"] = (total_with_docs / total_items) * 100
    else:
        percentages["overall"] = 100.0

    return all_results, percentages


def print_report(
    items: List[DocItem], stats: Dict[str, float], show_documented: bool = False
) -> None:
    """
    Print a docstring coverage report.

    Args:
        items: List of DocItem instances
        stats: Statistics dictionary with percentages
        show_documented: Whether to show items with docstrings
    """
    # Print missing docstrings
    missing = [item for item in items if not item.has_docstring]
    if missing:
        print("\nMissing docstrings:")
        print("-" * 80)
        for item in sorted(missing, key=lambda x: (x.path, x.lineno)):
            print(f"{item.path}:{item.lineno} - {item.type} '{item.name}'")
    else:
        print("\nAll items have docstrings!")

    # Print documented items if requested
    if show_documented:
        documented = [item for item in items if item.has_docstring]
        if documented:
            print("\nDocumented items:")
            print("-" * 80)
            for item in sorted(documented, key=lambda x: (x.path, x.lineno)):
                print(f"{item.path}:{item.lineno} - {item.type} '{item.name}'")

    # Print statistics
    print("\nDocstring coverage statistics:")
    print("-" * 80)
    for item_type, percentage in sorted(stats.items()):
        if item_type != "overall":
            print(f"{item_type.capitalize()}: {percentage:.1f}%")

    # Print overall percentage
    print("\n" + "=" * 80)
    print(f"Overall docstring coverage: {stats.get('overall', 0):.1f}%")
    print("=" * 80)


def main():
    """Run the docstring coverage check."""
    parser = ArgumentParser(description="Check docstring coverage")
    parser.add_argument(
        "--dir", type=str, default="src", help="Directory to check (default: src)"
    )
    parser.add_argument(
        "--include-all",
        action="store_true",
        help="Include private functions and classes (starting with _)",
    )
    parser.add_argument(
        "--show-documented",
        action="store_true",
        help="Show items with docstrings in the report",
    )
    parser.add_argument(
        "--min-coverage",
        type=float,
        default=0,
        help="Minimum required docstring coverage percentage",
    )
    args = parser.parse_args()

    directory = Path(args.dir)
    if not directory.exists() or not directory.is_dir():
        print(f"Error: {args.dir} is not a valid directory")
        return 1

    items, stats = check_directory_docstrings(directory, args.include_all)
    print_report(items, stats, args.show_documented)

    # Check minimum coverage requirement
    overall_coverage = stats.get("overall", 0)
    if args.min_coverage > 0 and overall_coverage < args.min_coverage:
        print(
            f"\nError: Docstring coverage ({overall_coverage:.1f}%) "
            f"is below the minimum requirement ({args.min_coverage}%)"
        )
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
