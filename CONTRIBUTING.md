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
3. Example code showing how the feature would be used
4. Any potential implementation details

### Pull Requests

1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and linting (`make test lint type-check`)
5. Commit your changes using [Conventional Commits](https://www.conventionalcommits.org/) format
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request using the PR template

## Development Setup

### Local Environment

1. Clone the repository:
   ```bash
   git clone https://github.com/DiogoRibeiro7/my_python_package.git
   cd my_python_package
   ```

2. Set up the development environment:
   ```bash
   # Using Poetry (recommended)
   make setup  # Installs dependencies and pre-commit hooks

   # OR manually
   poetry install
   pre-commit install
   ```

3. Activate the Poetry virtual environment:
   ```bash
   poetry shell
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
   make format  # Format code with black, isort, and ruff
   make lint    # Run linting checks
   make type-check  # Run type checking
   make test    # Run tests
   make security # Run security checks
   ```

2. Update documentation if needed:
   ```bash
   make docs
   ```

3. Update the CHANGELOG.md with your changes under the [Unreleased] section

## Coding Standards

We use several tools to maintain code quality:

- **Black**: For code formatting with line length of 100
- **isort**: For import sorting
- **Ruff**: For linting and code quality checks
- **mypy**: For static type checking
- **Bandit**: For security scanning

Our pre-commit hooks automatically check these when you commit. You can also run them manually with:

```bash
# Format code
make format

# Run all checks
make lint type-check security
```

### Style Guide

- Follow [PEP 8](https://pep8.org/) style guidelines
- Use [Google-style docstrings](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html)
- Include type hints for all function parameters and return values
- Write descriptive, self-documenting code
- Keep functions and methods focused on a single responsibility
- Use descriptive variable names

## Testing

- Write tests for all new functionality
- Maintain or improve test coverage
- Run the full test suite before submitting a PR:
  ```bash
  make test-cov  # Run tests with coverage report
  ```

## Commit Messages

Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

- `feat:` - A new feature
- `fix:` - A bug fix
- `docs:` - Documentation changes
- `style:` - Changes that do not affect code logic (formatting, etc.)
- `refactor:` - Code changes that neither fix a bug nor add a feature
- `perf:` - Performance improvements
- `test:` - Adding or correcting tests
- `build:` - Changes to build system or dependencies
- `ci:` - Changes to CI configuration
- `chore:` - Other changes that don't modify source or test files

Examples:
```
feat: add random greeting generator
fix: correct punctuation in formal greetings
docs: update usage examples in README
test: add test case for empty name validation
```

## Versioning

We follow [Semantic Versioning](https://semver.org/). The version will be automatically updated based on commit messages when merged to main:

- Commits with `BREAKING CHANGE` in the message trigger a major version bump
- Commits starting with `feat:` trigger a minor version bump
- All other commits trigger a patch version bump

## Release Process

1. Update CHANGELOG.md with the release date
2. Create a tag with the version number: `git tag v1.0.0`
3. Push the tag: `git push origin v1.0.0`
4. The CI/CD pipeline will automatically:
   - Run tests
   - Build the package
   - Publish to PyPI
   - Create a GitHub Release

## Documentation

- Update documentation for any new features or changes
- Keep docstrings up-to-date with code changes
- Add examples for new functionality

## Questions?

If you have any questions or need help, please:

1. Check existing issues and discussions
2. Open a new issue with the "question" label
3. Contact the maintainers

Thank you for contributing!
