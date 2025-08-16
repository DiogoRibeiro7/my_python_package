"""greeting_toolkit - A minimal but production-ready Python package.

This package demonstrates a properly structured Python project
with modern tooling and configuration.

The package provides various greeting functions with configurable
options for formatting, randomization, and validation.

Examples:
    >>> from greeting_toolkit import hello
    >>> hello("World")
    'Hello, World!'

    >>> from greeting_toolkit import generate_greeting
    >>> import re
    >>> # Time-based greeting will vary by time of day
    >>> bool(re.match(r'(Good (morning|afternoon|evening)|Hello), World!',
    ...               generate_greeting("World", time_based=True)))
    True

    >>> from greeting_toolkit import random_greeting
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
__version__: str = "0.3.0"
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


# Enable CLI usage with python -m greeting_toolkit
def _main() -> None:
    """Entry point for module execution.

    This function is called when the module is run directly
    with `python -m greeting_toolkit`.
    """
    import sys

    from .cli import main

    sys.exit(main())


if __name__ == "__main__":
    _main()
