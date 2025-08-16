import subprocess
import sys
from pathlib import Path


def test_docstring_coverage_script_runs():
    script = Path("scripts/check_docstrings_coverage.py")
    result = subprocess.run(
        [sys.executable, str(script), "--dir", "src/greeting_toolkit"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
