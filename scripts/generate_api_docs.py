#!/usr/bin/env python
"""
Generate API documentation for the package using pdoc.

This script automatically generates API documentation from docstrings in a more
structured way than the simple generate_docs.py script. It includes special
handling for modules, classes, and functions, and creates a more comprehensive
documentation structure.

Usage:
    python scripts/generate_api_docs.py [--format {html,markdown}] [--output-dir DIRECTORY]
"""

import argparse
import importlib
import inspect
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Literal, Optional, Set, Tuple, Union


def check_pdoc_installed() -> bool:
    """
    Check if pdoc is installed.

    Returns:
        True if pdoc is installed, False otherwise
    """
    try:
        importlib.util.find_spec("pdoc")
        return True
    except ImportError:
        print("pdoc is not installed. Installing it now...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pdoc"])
            return True
        except subprocess.CalledProcessError:
            print("Failed to install pdoc. Please install it manually: pip install pdoc")
            return False


def get_module_structure(
    package_name: str,
    exclude_private: bool = True,
    exclude_dirs: Optional[Set[str]] = None
) -> Dict[str, List[str]]:
    """
    Get the structure of a package, including modules and subpackages.

    Args:
        package_name: Name of the package to document
        exclude_private: Whether to exclude private modules (starting with _)
        exclude_dirs: Set of directory names to exclude

    Returns:
        Dictionary mapping package/subpackage names to lists of module names
    """
    if exclude_dirs is None:
        exclude_dirs = {"__pycache__", "tests", "examples"}

    try:
        package = importlib.import_module(package_name)
    except ImportError:
        print(f"Could not import {package_name}. Make sure it is installed.")
        return {}

    # Find the package directory
    if not hasattr(package, "__file__"):
        print(f"Package {package_name} has no __file__ attribute.")
        return {}

    package_dir = Path(package.__file__).parent
    structure: Dict[str, List[str]] = {package_name: []}

    # Find all Python files in the package directory
    for root, dirs, files in os.walk(package_dir):
        # Skip excluded directories
        dirs[:] = [d for d in dirs if d not in exclude_dirs]

        # Calculate the module path relative to the package
        rel_path = Path(root).relative_to(package_dir.parent)
        module_path = str(rel_path).replace(os.sep, ".")

        # Skip private modules if requested
        if exclude_private and any(part.startswith("_") for part in module_path.split(".")):
            continue

        # Find Python files in this directory
        py_files = [f for f in files if f.endswith(".py") and not (exclude_private and f.startswith("_"))]
        if py_files:
            # Add this subpackage if it's not already in the structure
            if module_path not in structure:
                structure[module_path] = []

            # Add modules to the subpackage
            for py_file in py_files:
                if py_file == "__init__.py":
                    continue
                module_name = f"{module_path}.{py_file[:-3]}"
                structure[module_path].append(module_name)

    return structure


def create_module_doc_file(
    module_name: str,
    output_dir: Path,
    format_type: Literal["html", "markdown"] = "markdown"
) -> Path:
    """
    Create documentation for a single module.

    Args:
        module_name: Name of the module to document
        output_dir: Directory to write documentation
        format_type: Output format (html or markdown)

    Returns:
        Path to the generated documentation file
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Determine output file extension
    ext = ".html" if format_type == "html" else ".md"

    # Generate output file path
    module_parts = module_name.split(".")
    output_path = output_dir
    for part in module_parts[:-1]:
        output_path = output_path / part
        os.makedirs(output_path, exist_ok=True)

    output_file = output_path / f"{module_parts[-1]}{ext}"

    # Call pdoc to generate documentation
    cmd = [
        sys.executable,
        "-m",
        "pdoc",
        f"--output-dir={output_path}",
    ]

    if format_type == "html":
        cmd.append("--html")

    cmd.append(module_name)

    try:
        subprocess.check_call(cmd)
        return output_file
    except subprocess.CalledProcessError as e:
        print(f"Error generating documentation for {module_name}: {e}")
        return output_file


def create_index_file(
    structure: Dict[str, List[str]],
    output_dir: Path,
    format_type: Literal["html", "markdown"] = "markdown",
    package_name: str = "my_python_package"
) -> None:
    """
    Create an index file that links to all the module documentation.

    Args:
        structure: Package structure from get_module_structure()
        output_dir: Directory to write documentation
        format_type: Output format (html or markdown)
        package_name: Name of the package
    """
    # Determine output file and content type
    if format_type == "html":
        index_file = output_dir / "index.html"
        template = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{package} API Documentation</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }}
        h1 {{
            border-bottom: 1px solid #eaecef;
            padding-bottom: 0.3em;
        }}
        h2 {{
            margin-top: 24px;
            font-size: 1.5em;
        }}
        a {{
            color: #0366d6;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        .module-list {{
            margin-left: 20px;
        }}
    </style>
</head>
<body>
    <h1>{package} API Documentation</h1>
    <p>This is the API documentation for the {package} package.</p>

    <h2>Package Structure</h2>
    {content}
</body>
</html>
"""
        package_content = "<ul>\n"
        for package, modules in sorted(structure.items()):
            if package == package_name:
                package_link = f"./{package.split('.')[-1]}/index.html"
                package_content += f'    <li><a href="{package_link}">{package}</a></li>\n'
            else:
                package_parts = package.split(".")
                package_link = f"./{'/'.join(package_parts)}/index.html"
                package_content += f'    <li><a href="{package_link}">{package}</a></li>\n'

            if modules:
                package_content += '    <ul class="module-list">\n'
                for module in sorted(modules):
                    module_parts = module.split(".")
                    module_link = f"./{'/'.join(module_parts[:-1])}/{module_parts[-1]}.html"
                    package_content += f'        <li><a href="{module_link}">{module}</a></li>\n'
                package_content += '    </ul>\n'

        package_content += "</ul>"
        content = template.format(package=package_name, content=package_content)
    else:
        # Markdown format
        index_file = output_dir / "README.md"
        content = f"# {package_name} API Documentation\n\n"
        content += f"This is the API documentation for the {package_name} package.\n\n"
        content += "## Package Structure\n\n"

        for package, modules in sorted(structure.items()):
            if package == package_name:
                package_link = f"./{package.split('.')[-1]}/index.html"
                content += f"- [{package}]({package_link})\n"
            else:
                package_parts = package.split(".")
                package_link = f"./{'/'.join(package_parts)}/index.html"
                content += f"- [{package}]({package_link})\n"

            if modules:
                for module in sorted(modules):
                    module_parts = module.split(".")
                    module_link = f"./{'/'.join(module_parts[:-1])}/{module_parts[-1]}.html"
                    content += f"  - [{module}]({module_link})\n"

    # Write the index file
    with open(index_file, "w") as f:
        f.write(content)


def generate_docs(
    format_type: Literal["html", "markdown"] = "html",
    output_dir: Optional[Path] = None,
    package_name: str = "my_python_package",
) -> bool:
    """
    Generate documentation using pdoc.

    Args:
        format_type: Output format (html or markdown)
        output_dir: Directory to output documentation (defaults to 'docs')
        package_name: Name of the package to document

    Returns:
        True if documentation was generated successfully, False otherwise
    """
    # Get the project root directory
    root_dir = Path(__file__).parent.parent.absolute()

    # Define the output directory for docs
    docs_dir = output_dir or root_dir / "docs" / "api"

    # Create docs directory if it doesn't exist
    os.makedirs(docs_dir, exist_ok=True)

    # Clear previous docs
    for item in docs_dir.iterdir():
        if item.is_dir():
            shutil.rmtree(item)
        else:
            if not item.name.startswith("."):  # Preserve hidden files
                item.unlink()

    # Import the package to ensure it's in sys.modules
    try:
        importlib.import_module(package_name)
    except ImportError:
        print(f"Could not import {package_name}. Make sure it is installed.")
        return False

    # Get the package structure
    structure = get_module_structure(package_name)
    if not structure:
        print(f"Could not determine the structure of {package_name}.")
        return False

    # Generate documentation using pdoc
    print(f"Generating {format_type} documentation for {package_name}...")

    # Process each module
    for package, modules in structure.items():
        # Generate documentation for the package itself
        create_module_doc_file(package, docs_dir, format_type)

        # Generate documentation for each module
        for module in modules:
            create_module_doc_file(module, docs_dir, format_type)

    # Create an index file
    create_index_file(structure, docs_dir, format_type, package_name)

    print(f"Documentation generated successfully in {docs_dir}")
    return True


def parse_args() -> argparse.Namespace:
    """
    Parse command line arguments.

    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(description="Generate API documentation")
    parser.add_argument(
        "--format",
        choices=["html", "markdown"],
        default="html",
        help="Output format (default: html)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Output directory (default: docs/api/)",
    )
    parser.add_argument(
        "--package",
        default="my_python_package",
        help="Package name to document (default: my_python_package)",
    )
    return parser.parse_args()


def main() -> int:
    """
    Main function.

    Returns:
        Exit code (0 for success, 1 for failure)
    """
    args = parse_args()

    if not check_pdoc_installed():
        return 1

    format_type: Literal["html", "markdown"] = "html"
    if args.format == "markdown":
        format_type = "markdown"

    if not generate_docs(
        format_type=format_type,
        output_dir=args.output_dir,
        package_name=args.package,
    ):
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
