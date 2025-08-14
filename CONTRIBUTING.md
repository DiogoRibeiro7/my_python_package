# Contributing to my_python_package

Thank you for considering contributing to my_python_package! This document provides guidelines and instructions for contributing.

## Code of Conduct

Please be respectful and considerate of others when contributing to this project. We aim to foster an inclusive and welcoming community.

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue using the bug report template. Include:

1. A clear title and description
2. Steps to reproduce the behavior
3. Expected behavior
4. Actual behavior
5. Environment details (OS, Python version, package version)

### Suggesting Enhancements

For feature requests, please use the feature request template. Include:

1. A clear title and description
2. Why this feature would be useful
3. Any potential implementation details

### Pull Requests

1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`make test`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Development Setup

### Local Environment

1. Clone the repository:
   ```bash
   git clone https://github.com/DiogoRibeiro7/my_python_package.git
   cd my_python_package
   ```

2. Install dependencies with Poetry:
   ```bash
   poetry install
   ```

3. Set up pre-commit hooks:
   ```bash
   pre-commit install
   ```

### Using Docker

Alternatively, you can use Docker:

```bash
docker-compose up app  # Run the application
docker-compose up test  # Run tests
docker-compose up lint  # Run linting
docker-compose up type-check  # Run type checking
```

## Development Workflow

1. Make sure your code passes all checks:
   ```bash
   make lint
   make type-check
   make test
   ```

2. Update documentation if needed:
   ```bash
   python scripts/generate_docs.py
   ```

3. Update the CHANGELOG.md with your changes under the [Unreleased] section

## Coding Standards

- Follow PEP 8 style guidelines
- Include docstrings for all functions, classes, and modules
- Add type hints to all function parameters and return values
- Write tests for all new functionality
- Ensure test coverage is maintained or improved

## Commit Messages

Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

- `feat:` - A new feature
- `fix:` - A bug fix
- `docs:` - Documentation changes
- `style:` - Changes that do not affect code logic
- `refactor:` - Code changes that neither fix a bug nor add a feature
- `perf:` - Performance improvements
- `test:` - Adding or correcting tests
- `build:` - Changes to build system or dependencies
- `ci:` - Changes to CI configuration
- `chore:` - Other changes that don't modify source or test files

## Release Process

1. Update version number in pyproject.toml
2. Update CHANGELOG.md with release date
3. Create a tag with the version number
4. Push the tag to GitHub
5. Build and publish to PyPI:
   ```bash
   make publish
   ```

## Questions?

If you have any questions, feel free to open an issue or contact the maintainers.

Thank you for contributing!
