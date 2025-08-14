# my_python_package

[![PyPI version](https://img.shields.io/pypi/v/my_python_package.svg)](https://pypi.org/project/my_python_package/) 
[![Python Versions](https://img.shields.io/pypi/pyversions/my_python_package.svg)](https://pypi.org/project/my_python_package/) 
[![Tests](https://github.com/DiogoRibeiro7/my_python_package/actions/workflows/test.yml/badge.svg)](https://github.com/DiogoRibeiro7/my_python_package/actions/workflows/test.yml) 
[![Coverage](https://img.shields.io/badge/coverage-95%25-brightgreen)](https://codecov.io/gh/DiogoRibeiro7/my_python_package)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

A minimal but production-ready Python package scaffold configured for publishing to [PyPI](https://pypi.org).

## Features

- 🚀 Modern Python packaging with Poetry
- 🔧 Configurable greeting functions with multiple formatting options
- 🧪 Comprehensive testing suite with 100% coverage
- 📊 Continuous Integration workflows for testing, coverage, and releases
- 🛠️ Code quality tools preconfigured (ruff, mypy, pre-commit)
- 📝 Complete documentation with doctests
- 🔄 Automated dependency management and version bumping

## Installation

```bash
# From PyPI
pip install my_python_package

# Or with Poetry
poetry add my_python_package
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

### Setup

1. Clone the repository
   ```bash
   git clone https://github.com/DiogoRibeiro7/my_python_package.git
   cd my_python_package
   ```

2. Install dependencies with Poetry
   ```bash
   poetry install
   ```

3. Set up pre-commit hooks
   ```bash
   pre-commit install
   ```

### Testing

Run tests with pytest:

```bash
# Run all tests
poetry run pytest

# Run tests with coverage
poetry run pytest --cov=my_python_package

# Run doctests
poetry run pytest --doctest-modules src/
```

### Documentation

Generate documentation:

```bash
# Generate HTML documentation
poetry run python scripts/generate_docs.py

# Generate Markdown documentation
poetry run python scripts/generate_docs.py --format markdown
```

### Code Quality

Run linting and type checking:

```bash
# Format code
poetry run ruff format .

# Lint code
poetry run ruff check .

# Type check
poetry run mypy src tests
```

You can also use the included Makefile:

```bash
# Format and lint
make format
make lint

# Type check
make type-check

# Run tests with coverage
make test-cov
```

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
├── Makefile                  # Common development tasks
├── Dockerfile                # Docker container definition
├── docker-compose.yml        # Docker services configuration
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
        ├── release.yml       # PyPI release automation
        ├── dependency-scanning.yml # Security scanning
        ├── auto-pyproject-update.yml  # Version bumping
        └── auto-upgrade-pyproject.yml # Dependency upgrades
```

## Automated Workflows

The repository includes GitHub Actions for:

1. **Testing**: Runs the test suite on multiple Python versions
2. **Code Coverage**: Tracks and reports test coverage
3. **Version Bumping**: Automatically bumps version on push to main based on commit message:
   - `BREAKING CHANGE` → major version bump
   - `feat:` prefix → minor version bump
   - Otherwise → patch version bump
4. **Dependency Updates**: Weekly PR to update dependency constraints to latest
5. **Security Scanning**: Regular checks for vulnerable dependencies
6. **Release Automation**: Automates PyPI releases when a version tag is pushed

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to contribute to this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
