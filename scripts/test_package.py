#!/usr/bin/env python3
"""Run a basic verification of the greeting-toolkit package.

This script performs a series of smoke tests to ensure the package works
correctly after renaming:

1. Install the project in editable mode.
2. Import the ``greeting_toolkit`` module.
3. Execute a simple CLI command.
4. Run the test suite.
5. Build the documentation to ensure docs generation succeeds.

The documentation is generated into a temporary directory so no repository
files are modified.
"""
from __future__ import annotations

import os
import subprocess  # noqa: S404  # nosec B404
import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def run(cmd: list[str], **kwargs: object) -> None:
    """Execute ``cmd`` safely and stream its output."""
    if not all(isinstance(part, str) for part in cmd):
        raise TypeError("Command parts must be strings")
    sys.stdout.write(f"$ {' '.join(cmd)}\n")
    subprocess.run(cmd, check=True, **kwargs)  # noqa: S603  # nosec B603


def main() -> int:
    """Run verification steps and return exit code."""
    run([sys.executable, "-m", "pip", "install", "-e", str(PROJECT_ROOT)])
    run([sys.executable, "-c", "import greeting_toolkit"])
    run(["greeting-toolkit", "hello", "World"])

    env = os.environ.copy()
    env["PYTHONPATH"] = str(PROJECT_ROOT / "src")
    run([sys.executable, "-m", "pytest", "--no-cov"], env=env)

    # Ensure documentation can be generated with a known version
    run([sys.executable, "-m", "pip", "install", "pdoc==14.3.0"])
    with tempfile.TemporaryDirectory() as tmpdir:
        run([sys.executable, "-m", "pdoc", "greeting_toolkit", "-o", tmpdir])

    sys.stdout.write("All checks completed successfully.\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
