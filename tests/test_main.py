"""Tests for invoking the package as a module."""

import subprocess
import sys


def test_module_execution():
    """Running ``python -m greeting_toolkit`` should execute the CLI."""
    result = subprocess.run(  # noqa: S603
        [sys.executable, "-m", "greeting_toolkit", "hello", "World"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert result.returncode == 0
    assert "Hello, World!" in result.stdout
