"""
my_python_package - A minimal but production-ready Python package.

This package demonstrates a properly structured Python project
with modern tooling and configuration.

The package provides various greeting functions with configurable
options for formatting, randomization, and validation.

Examples:
    >>> from my_python_package import hello
    >>> hello("World")
    'Hello, World!'
    
    >>> from my_python_package import generate_greeting
    >>> import re
    >>> # Time-based greeting will vary by time of day
    >>> bool(re.match(r'(Good (morning|afternoon|evening)|Hello), World!', 
    ...               generate_greeting("World", time_based=True)))
    True
    
    >>> from my_python_package import random_greeting
    >>> # Random greeting will contain the name
    >>> "World" in random_greeting("World")
    True
"""

# Import public-facing functions
from .core import (
    create_greeting_list,
    format_greeting,
    generate_greeting,
    hello,
    random_greeting,
    validate_name,
)

# Version and author information
__version__: str = "0.2.0"
__author__: str = "Diogo Ribeiro"

# Public API
__all__ = [
    "hello", 
    "generate_greeting",
    "random_greeting",
    "validate_name",
    "create_greeting_list",
    "format_greeting",
]

# Enable CLI usage with python -m my_python_package
def _main() -> None:
    """
    Entry point for module execution.
    
    This function is called when the module is run directly
    with `python -m my_python_package`.
    """
    from .cli import main
    import sys
    sys.exit(main())


if __name__ == "__main__":
    _main()
