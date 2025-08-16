#!/usr/bin/env python
"""
Generate API documentation RST files for Sphinx.

This script inspects the Python modules in the package and creates
RST files for the API documentation.
"""

import importlib
import inspect
import os
import pkgutil
import sys
from pathlib import Path
from typing import List, Set

# Add the project to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

PACKAGE_NAME = "greeting_toolkit"
API_DIR = Path(__file__).parent / "api"


def generate_module_rst(module_name: str, output_path: Path) -> None:
    """Generate RST file for a module."""
    module = importlib.import_module(module_name)

    # Create the content for the RST file
    content = [
        f"{module_name}",
        "=" * len(module_name),
        "",
        f".. automodule:: {module_name}",
        "   :members:",
        "   :undoc-members:",
        "   :show-inheritance:",
        "",
    ]

    # Get all classes in the module
    classes = inspect.getmembers(module, inspect.isclass)
    for class_name, class_obj in classes:
        if class_obj.__module__ == module_name:
            content.extend([
                f"{module_name}.{class_name}",
                "-" * len(f"{module_name}.{class_name}"),
                "",
                f".. autoclass:: {module_name}.{class_name}",
                "   :members:",
                "   :undoc-members:",
                "   :show-inheritance:",
                "",
            ])

    # Write the RST file
    with open(output_path, "w") as f:
        f.write("\n".join(content))


def generate_package_rst(package_name: str, output_path: Path, modules: List[str]) -> None:
    """Generate RST file for a package."""
    # Create the content for the RST file
    content = [
        f"{package_name}",
        "=" * len(package_name),
        "",
        f".. automodule:: {package_name}",
        "   :members:",
        "   :undoc-members:",
        "   :show-inheritance:",
        "",
        "Submodules",
        "----------",
        "",
        ".. toctree::",
        "   :maxdepth: 1",
        "",
    ]

    # Add modules to the toctree
    for module in sorted(modules):
        if module != package_name:
            module_short = module.split(".")[-1]
            content.append(f"   {module_short}")

    content.append("")

    # Write the RST file
    with open(output_path, "w") as f:
        f.write("\n".join(content))


def generate_modules_rst(output_path: Path, packages: List[str]) -> None:
    """Generate the modules.rst file that includes all packages."""
    # Create the content for the RST file
    content = [
        "API Reference",
        "============",
        "",
        ".. toctree::",
        "   :maxdepth: 2",
        "",
    ]

    # Add packages to the toctree
    for package in sorted(packages):
        package_short = package.split(".")[-1]
        content.append(f"   {package_short}")

    content.append("")

    # Write the RST file
    with open(output_path, "w") as f:
        f.write("\n".join(content))


def discover_modules(package_name: str) -> Set[str]:
    """Discover all modules in the package."""
    modules = set()

    def walk_packages(pkg_name, prefix=""):
        try:
            pkg = importlib.import_module(pkg_name)

            # Check if this is a package
            if hasattr(pkg, "__path__"):
                for _, name, is_pkg in pkgutil.iter_modules(pkg.__path__, pkg_name + "."):
                    if not name.startswith("_"):  # Skip private modules
                        modules.add(name)
                        if is_pkg:
                            walk_packages(name)
        except (ImportError, AttributeError):
            print(f"Error importing {pkg_name}")

    # Start with the base package
    modules.add(package_name)
    walk_packages(package_name)

    return modules


def main() -> None:
    """Generate API documentation RST files."""
    # Create the API directory if it doesn't exist
    os.makedirs(API_DIR, exist_ok=True)

    # Discover modules
    modules = discover_modules(PACKAGE_NAME)

    # List of packages (modules with submodules)
    packages = []
    submodules = {}

    # Group modules by package
    for module in modules:
        parts = module.split(".")
        if len(parts) > 1:
            package = ".".join(parts[:-1])
            submodules.setdefault(package, []).append(module)
        else:
            packages.append(module)

    # Generate RST files for each module
    for module in modules:
        if module in packages or module in submodules:
            continue  # Skip packages (they'll be handled separately)

        output_path = API_DIR / f"{module.split('.')[-1]}.rst"
        generate_module_rst(module, output_path)

    # Generate RST files for each package
    for package, package_modules in submodules.items():
        # Add the package to the modules list for each submodule
        package_modules.append(package)

        output_path = API_DIR / f"{package.split('.')[-1]}.rst"
        generate_package_rst(package, output_path, package_modules)

        # Also generate RST files for each submodule
        for module in package_modules:
            if module != package:  # Skip the package itself
                output_path = API_DIR / f"{module.split('.')[-1]}.rst"
                generate_module_rst(module, output_path)

    # Generate the modules.rst file
    generate_modules_rst(API_DIR / "modules.rst", packages + list(submodules.keys()))

    print(f"Generated API documentation in {API_DIR}")


if __name__ == "__main__":
    main()
