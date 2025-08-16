# my_python_package

[![PyPI version](https://img.shields.io/pypi/v/my_python_package.svg) ![Docstring Coverage](https://img.shields.io/badge/docstring%20coverage-93.1%25-brightgreen)](https://pypi.org/project/my_python_package/)
[![Python Versions](https://img.shields.io/pypi/pyversions/my_python_package.svg)](https://pypi.org/project/my_python_package/)
[![Tests](https://github.com/DiogoRibeiro7/my_python_package/actions/workflows/test.yml/badge.svg)](https://github.com/DiogoRibeiro7/my_python_package/actions/workflows/test.yml)
[![Coverage](https://img.shields.io/badge/coverage-95%25-brightgreen)](https://codecov.io/gh/DiogoRibeiro7/my_python_package)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/badge/ruff-enabled-brightgreen)](https://github.com/astral-sh/ruff)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat)](https://pycqa.github.io/isort/)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)

A minimal but production-ready Python package scaffold configured for publishing to [PyPI](https://pypi.org).

## Features

- 🚀 Modern Python packaging with Poetry
- 🔧 Configurable greeting functions with multiple formatting options
- 🧪 Comprehensive testing suite with 100% coverage
- 📊 Continuous Integration workflows for testing, coverage, and releases
- 🛠️ Code quality tools preconfigured (black, ruff, mypy, isort, pre-commit)
- 📝 Complete documentation with doctests
- 🔄 Automated dependency management and version bumping
- 🔒 Security scanning with Bandit and Trivy
- 🧩 Multi-environment testing with tox

## Installation

### From PyPI

```bash
# Using pip
pip install my_python_package

# Using Poetry
poetry add my_python_package
```

### For Development

```bash
# Clone the repository
git clone https://github.com/DiogoRibeiro7/my_python_package.git
cd my_python_package

# Using Poetry (recommended)
poetry install

# Set up pre-commit hooks
pre-commit install

# Alternatively, use the Makefile for one-step setup
make setup
```

## Usage

### Basic Greeting

```python
from my_python_package import hello

# Basic usage
greeting = hello("World")
print(greeting)  # Output: Hello, World!

# With custom greeting
custom = hello("Python", greeting="Hi")
print(custom)  # Output: Hi, Python!
```

### Formatted Greetings

```python
from my_python_package import format_greeting

# Default formatting
print(format_greeting("World"))  # Output: Hello, World!

# Custom formatting
print(format_greeting(
    "Python",
    greeting="Welcome",
    punctuation="!!!",
    uppercase=True
))  # Output: WELCOME, PYTHON!!!

# Truncate long greetings
print(format_greeting("Very Long Name", max_length=15))  # Output: Hello, Very...
```

### Multiple Greetings

```python
from my_python_package import create_greeting_list

# Greet multiple people
greetings = create_greeting_list(["Alice", "Bob", "Charlie"])
for greeting in greetings:
    print(greeting)
```

### Context-Aware Greetings

```python
from my_python_package import generate_greeting

# Time-based greeting (morning/afternoon/evening)
print(generate_greeting("World", time_based=True))

# Formal greeting
print(generate_greeting("Mrs. Smith", formal=True))
```

### Random Greetings

```python
from my_python_package import random_greeting

# Get a random greeting
print(random_greeting("World"))  # Different greeting each time
```

### Command Line Interface

The package also provides a command-line interface:

```bash
# Basic greeting
my-python-package hello World

# Random greeting
my-python-package random World

# Time-based greeting
my-python-package time World --formal

# Multiple names
my-python-package multi Alice Bob Charlie --greeting "Greetings"

# Formatted greeting
my-python-package format World --greeting "Welcome" --uppercase --max-length 15
```

## Development

### Development Environment Setup

Setting up your development environment is easy with the included tools:

```bash
# Full development setup (installs all dev dependencies and pre-commit hooks)
make setup

# Or install only dependencies without pre-commit hooks
make dev-install

# If you prefer not to use Poetry
pip install -r dev-requirements.txt
pre-commit install
```

### Code Formatting and Quality Tools

The project uses multiple tools to ensure code quality:

```bash
# Format code (black, isort, ruff)
make format

# Lint code (ruff)
make lint

# Type check (mypy)
make type-check

# Security check (bandit)
make security

# Run all quality checks at once
make lint type-check security
```

### Testing

Run tests with pytest:

```bash
# Run all tests
make test

# Run tests with coverage
make test-cov

# Run tests in multiple Python environments
make tox
```

#### Test Categories

You can run specific test categories using pytest markers:

```bash
# Run only fast tests (skip slow ones)
pytest -m "not slow"

# Run only integration tests
pytest -m "integration"
```

### Documentation

Generate documentation:

```bash
# Generate HTML documentation
make docs

# Or use the script directly with options
python scripts/generate_docs.py --format markdown --output-dir docs/markdown
```

### Package Management

```bash
# Build the package
make build

# Publish to TestPyPI
make publish-test

# Publish to PyPI
make publish
```

### Version Management

Automatically bump the package version:

```bash
# Patch version (0.1.0 -> 0.1.1)
make bump-patch

# Minor version (0.1.0 -> 0.2.0)
make bump-minor

# Major version (0.1.0 -> 1.0.0)
make bump-major
```

### Dependency Management

Check and update dependencies:

```bash
# Check for missing or unused dependencies
make check-deps
```

## Continuous Integration

The repository includes GitHub Actions for:

1. **Testing**: Runs the test suite on multiple Python versions
2. **Code Coverage**: Tracks and reports test coverage
3. **Style Checking**: Ensures code follows the project's style guidelines
4. **Security Scanning**: Checks for vulnerabilities in code and dependencies
5. **Version Bumping**: Automatically bumps version on push to main based on commit message:
   - `BREAKING CHANGE` → major version bump
   - `feat:` prefix → minor version bump
   - Otherwise → patch version bump
6. **Dependency Updates**: Weekly PR to update dependency constraints to latest
7. **Release Automation**: Automates PyPI releases when a version tag is pushed

## Project Structure

```text
my_python_package/
├── pyproject.toml            # Project metadata, dependencies
├── README.md                 # Project overview
├── LICENSE                   # MIT license
├── CHANGELOG.md              # Version changelog
├── CONTRIBUTING.md           # Contribution guidelines
├── CONTRIBUTORS.md           # List of contributors
├── .gitignore                # Git ignore rules
├── .pre-commit-config.yaml   # Pre-commit hooks configuration
├── .editorconfig             # Editor configuration
├── setup.cfg                 # Configuration for various tools
├── tox.ini                   # Multi-environment testing
├── Makefile                  # Common development tasks
├── Dockerfile                # Docker container definition
├── docker-compose.yml        # Docker services configuration
├── requirements.txt          # Dependencies for simple installation
├── dev-requirements.txt      # Development dependencies
├── src/
│   └── my_python_package/    # Package source code
│       ├── __init__.py       # Package exports
│       ├── __main__.py       # Module execution entry point
│       ├── core.py           # Core greeting functionality
│       ├── config.py         # Configuration system
│       ├── logging.py        # Logging system
│       └── cli.py            # Command-line interface
├── tests/                    # Test directory
│   ├── test_core.py          # Core tests
│   ├── test_config.py        # Configuration tests
│   ├── test_logging.py       # Logging tests
│   └── test_cli.py           # CLI tests
├── examples/                 # Usage examples
│   └── usage.py              # Basic example
├── scripts/                  # Utility scripts
│   ├── pyproject_editor.py   # Safe pyproject.toml editing
│   ├── pyproject_updater.py  # Dependency upgrade utility
│   ├── check_imports_vs_pyproject.py  # Import checker
│   └── generate_docs.py      # Documentation generator
└── .github/                  # GitHub config
    ├── ISSUE_TEMPLATE/       # Issue templates
    ├── PULL_REQUEST_TEMPLATE.md # PR template
    └── workflows/            # CI/CD workflows
        ├── test.yml          # Run tests on push/PR
        ├── code-coverage.yml # Track code coverage
        ├── style-check.yml   # Check code style
        ├── security-scan.yml # Security scanning
        ├── release.yml       # PyPI release automation
        ├── dependency-scanning.yml # Security scanning
        ├── auto-pyproject-update.yml  # Version bumping
        └── auto-upgrade-pyproject.yml # Dependency upgrades
```

## Tool Configuration

The project includes configuration for several development tools:

### Code Style and Quality

- **Black**: Consistent code formatting with a line length of 100
- **isort**: Import sorting with Black compatibility
- **Ruff**: Fast Python linter that combines multiple tools (flake8, pycodestyle, etc.)
- **mypy**: Static type checking with strict settings
- **Bandit**: Security vulnerability scanning

### Testing

- **pytest**: Test framework with coverage reporting
- **tox**: Multi-environment testing
- **Coverage**: Code coverage tracking and reporting

### CI/CD

- **GitHub Actions**: Automated workflows for testing, linting, and releasing
- **pre-commit**: Automated checks before committing code

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to contribute to this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
