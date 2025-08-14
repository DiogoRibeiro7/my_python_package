# my_python_package

[![PyPI version](https://img.shields.io/pypi/v/my_python_package.svg)](https://pypi.org/project/my_python_package/) [![Python Versions](https://img.shields.io/pypi/pyversions/my_python_package.svg)](https://pypi.org/project/my_python_package/) [![Tests](https://github.com/DiogoRibeiro7/my_python_package/actions/workflows/test.yml/badge.svg)](https://github.com/DiogoRibeiro7/my_python_package/actions/workflows/test.yml) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A minimal but production-ready Python package scaffold configured for publishing to [PyPI](https://pypi.org).

## Features

- Modern Python packaging with Poetry
- Automated dependency management
- Comprehensive testing setup
- Continuous Integration workflows
- Code quality tools preconfigured

## Installation

```bash
pip install my_python_package
```

Or with Poetry:

```bash
poetry add my_python_package
```

## Usage

```python
from my_python_package import hello

# Basic usage
greeting = hello("World")
print(greeting)  # Output: Hello, World!

# With custom greeting
custom = hello("Python", greeting="Hi")
print(custom)  # Output: Hi, Python!
```

## Development

### Setup

1. Clone the repository

  ```bash
  git clone https://github.com/DiogoRibeiro7/my_python_package.git
  cd my_python_package
  ```

2. Install dependencies

  ```bash
  poetry install
  ```

3. Setup pre-commit hooks

  ```bash
  pre-commit install
  ```

### Testing

Run tests with pytest:

```bash
poetry run pytest
```

Run tests with coverage:

```bash
poetry run pytest --cov=my_python_package
```

### Code Quality

This project uses:

- Ruff for linting and formatting
- Mypy for type checking
- Pre-commit for automated checks

### Building and Publishing

Build the package:

```bash
poetry build
```

Publish to PyPI (use TestPyPI first!):

```bash
# Test PyPI
poetry config repositories.testpypi https://test.pypi.org/legacy/
poetry publish -r testpypi --username __token__ --password <your-test-token>

# Production PyPI
poetry publish --username __token__ --password <pypi-token>
```

## Project Structure

```text
my_python_package/
├── pyproject.toml            # Project metadata, dependencies
├── README.md                 # Project overview
├── LICENSE                   # MIT license
├── .gitignore                # Git ignore rules
├── .pre-commit-config.yaml   # Pre-commit hooks configuration
├── src/
│   └── my_python_package/    # Package source code
│       ├── __init__.py       # Package exports
│       └── core.py           # Core functionality
├── tests/                    # Test directory
│   └── test_core.py          # Unit tests
├── examples/                 # Usage examples
│   └── usage.py              # Basic example
├── scripts/                  # Utility scripts
│   ├── pyproject_editor.py   # Safe pyproject.toml editing
│   ├── pyproject_updater.py  # Dependency upgrade utility
│   └── check_imports_vs_pyproject.py  # Import checker
└── .github/                  # GitHub config
    └── workflows/            # CI/CD workflows
        ├── test.yml          # Run tests on push/PR
        ├── auto-pyproject-update.yml  # Version bumping
        └── auto-upgrade-pyproject.yml # Dependency upgrades
```

## Automated Workflows

The repository includes GitHub Actions for:

1. **Running Tests**: Runs the test suite on multiple Python versions
2. **Version Bumping**: Automatically bumps version on push to main based on commit message:

  - `BREAKING CHANGE` → major version bump
  - `feat:` prefix → minor version bump
  - Otherwise → patch version bump

3. **Dependency Updates**: Weekly PR to update dependency constraints to latest

## License

This project is licensed under the MIT License - see the <LICENSE> file for details.
