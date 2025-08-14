#!/usr/bin/env python
"""
Generate documentation for the package using pdoc.

This script automates the generation of API documentation from docstrings.
It supports both HTML and Markdown output formats.

Usage:
    python scripts/generate_docs.py [--format {html,markdown}] [--output-dir DIRECTORY]
"""

import argparse
import importlib
import importlib.util
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import List, Literal, Optional, Union


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
    docs_dir = output_dir or root_dir / "docs"
    
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
    
    # Generate documentation using pdoc
    print(f"Generating {format_type} documentation for {package_name}...")
    
    # Prepare the pdoc command
    pdoc_args: List[str] = [
        sys.executable, "-m", "pdoc",
        "--force",
    ]
    
    # Add format-specific args
    if format_type == "html":
        pdoc_args.extend(["--html", "--output-dir", str(docs_dir)])
    elif format_type == "markdown":
        pdoc_args.extend(["--output-dir", str(docs_dir)])
    
    # Add package name
    pdoc_args.append(package_name)
    
    try:
        subprocess.check_call(pdoc_args)
        print(f"Documentation generated successfully in {docs_dir}")
        
        # Create an index.html file if using markdown format
        if format_type == "markdown":
            index_path = docs_dir / "index.html"
            with open(index_path, "w") as f:
                f.write(f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="0;url=./{package_name}/">
    <title>{package_name} Documentation</title>
</head>
<body>
    <p>Redirecting to <a href="./{package_name}/">{package_name} documentation</a>...</p>
</body>
</html>
""")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error generating documentation: {e}")
        return False


def parse_args() -> argparse.Namespace:
    """
    Parse command line arguments.
    
    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(description="Generate package documentation")
    parser.add_argument(
        "--format",
        choices=["html", "markdown"],
        default="html",
        help="Output format (default: html)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Output directory (default: docs/)",
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
    ):
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
