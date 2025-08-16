"""Tests for the package __init__ module."""

import importlib
import re
from unittest.mock import patch

import pytest

import greeting_toolkit


def test_package_version():
    """Test that the package has a valid version string."""
    assert hasattr(greeting_toolkit, "__version__")
    assert isinstance(greeting_toolkit.__version__, str)
    # Check that it follows semantic versioning (major.minor.patch)
    assert re.match(r"^\d+\.\d+\.\d+", greeting_toolkit.__version__)


def test_package_author():
    """Test that the package has an author string."""
    assert hasattr(greeting_toolkit, "__author__")
    assert isinstance(greeting_toolkit.__author__, str)
    assert greeting_toolkit.__author__ == "Diogo Ribeiro"


def test_package_exports():
    """Test that the package exports the expected functions."""
    # Check __all__ contents
    assert hasattr(greeting_toolkit, "__all__")
    assert isinstance(greeting_toolkit.__all__, list)

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
        assert func in greeting_toolkit.__all__

    # Check functions are actually exported
    for func in greeting_toolkit.__all__:
        assert hasattr(greeting_toolkit, func)
        assert callable(getattr(greeting_toolkit, func))


def test_module_imports():
    """Test that all package imports work properly."""
    # Test importing the main module
    importlib.reload(greeting_toolkit)

    # Test importing submodules
    from greeting_toolkit import cli, config, core, logging

    # Verify the modules loaded correctly
    assert hasattr(config, "Config")
    assert hasattr(core, "hello")
    assert hasattr(cli, "main")
    assert hasattr(logging, "logger")


def test_main_function():
    """Test the _main function that handles module execution."""
    # Create a mock for sys.exit and cli.main
    with patch("greeting_toolkit.cli.main", return_value=42) as mock_main:
        with patch("sys.exit") as mock_exit:
            # Call _main function
            greeting_toolkit._main()

            # Verify cli.main was called
            mock_main.assert_called_once()

            # Verify sys.exit was called with the return value from cli.main
            mock_exit.assert_called_once_with(42)


def test_direct_execution():
    """Test module execution behavior."""
    # We can't directly test __name__ == "__main__" code paths in an imported module,
    # but we can test the behavior indirectly by simulating it

    # Save original __name__
    original_name = greeting_toolkit.__name__

    try:
        # Set up the module as if it's being run directly
        with patch.object(greeting_toolkit, "__name__", "__main__"):
            with pytest.raises(SystemExit):
                exec(open(greeting_toolkit.__file__).read(), vars(greeting_toolkit))
    finally:
        # Restore original __name__
        greeting_toolkit.__name__ = original_name


def test_doctest_examples():
    """Test that the doctest examples in __init__ work correctly."""
    import doctest

    # Run doctests on the module
    result = doctest.testmod(greeting_toolkit)

    # Verify all tests passed (failures == 0)
    assert result.failed == 0
    assert result.attempted > 0  # Make sure some tests were actually run
