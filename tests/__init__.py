"""Tests for the package __init__ module."""

import importlib
import re
import sys
from unittest.mock import patch

import pytest

import my_python_package


def test_package_version():
    """Test that the package has a valid version string."""
    assert hasattr(my_python_package, "__version__")
    assert isinstance(my_python_package, str)
    # Check that it follows semantic versioning (major.minor.patch)
    assert re.match(r"^\d+\.\d+\.\d+", my_python_package.__version__)


def test_package_author():
    """Test that the package has an author string."""
    assert hasattr(my_python_package, "__author__")
    assert isinstance(my_python_package.__author__, str)
    assert my_python_package.__author__ == "Diogo Ribeiro"


def test_package_exports():
    """Test that the package exports the expected functions."""
    # Check __all__ contents
    assert hasattr(my_python_package, "__all__")
    assert isinstance(my_python_package.__all__, list)

    # Check expected functions are in __all__
    expected_functions = [
        "hello",
        "generate_greeting",
        "random_greeting",
        "validate_name",
        "create_greeting_list",
        "format_greeting",
    ]
    for func in expected_functions:
        assert func in my_python_package.__all__

    # Check functions are actually exported
    for func in my_python_package.__all__:
        assert hasattr(my_python_package, func)
        assert callable(getattr(my_python_package, func))


def test_module_imports():
    """Test that all package imports work properly."""
    # Test importing the main module
    importlib.reload(my_python_package)

    # Test importing submodules
    from my_python_package import config
    from my_python_package import core
    from my_python_package import cli
    from my_python_package import logging

    # Verify the modules loaded correctly
    assert hasattr(config, "Config")
    assert hasattr(core, "hello")
    assert hasattr(cli, "main")
    assert hasattr(logging, "logger")


def test_main_function():
    """Test the _main function that handles module execution."""
    # Create a mock for sys.exit and cli.main
    with patch("my_python_package.cli.main", return_value=42) as mock_main:
        with patch("sys.exit") as mock_exit:
            # Call _main function
            my_python_package._main()

            # Verify cli.main was called
            mock_main.assert_called_once()

            # Verify sys.exit was called with the return value from cli.main
            mock_exit.assert_called_once_with(42)


def test_direct_execution():
    """Test module execution behavior."""
    # We can't directly test __name__ == "__main__" code paths in an imported module,
    # but we can test the behavior indirectly by simulating it

    # Save original __name__
    original_name = my_python_package.__name__

    try:
        # Set up the module as if it's being run directly
        with patch.object(my_python_package, "__name__", "__main__"):
            with patch("my_python_package._main") as mock_main:
                # Re-execute the module code
                exec(open(my_python_package.__file__).read(), vars(my_python_package))

                # Verify _main was called
                mock_main.assert_called_once()
    finally:
        # Restore original __name__
        my_python_package.__name__ = original_name


def test_doctest_examples():
    """Test that the doctest examples in __init__ work correctly."""
    import doctest

    # Run doctests on the module
    result = doctest.testmod(my_python_package)

    # Verify all tests passed (failures == 0)
    assert result.failed == 0
    assert result.attempted > 0  # Make sure some tests were actually run
