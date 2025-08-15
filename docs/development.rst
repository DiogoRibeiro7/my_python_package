=================
Development Guide
=================

This guide will help you set up your development environment and understand the workflow for contributing to ``my_python_package``.

Development Environment Setup
---------------------------

Prerequisites
~~~~~~~~~~~~

- Python 3.10 or higher
- `Poetry <https://python-poetry.org/docs/#installation>`_ for dependency management
- Git

Initial Setup
~~~~~~~~~~~~

1. Clone the repository:

   .. code-block:: bash

       git clone https://github.com/DiogoRibeiro7/my_python_package.git
       cd my_python_package

2. Install dependencies and set up pre-commit hooks:

   .. code-block:: bash

       # Using the Makefile (recommended)
       make setup
       
       # Alternatively, manually:
       poetry install
       pre-commit install

3. Activate the virtual environment:

   .. code-block:: bash

       poetry shell

Alternative Setup Methods
~~~~~~~~~~~~~~~~~~~~~~~

Using Docker
^^^^^^^^^^^

The repository includes Docker configuration files:

.. code-block:: bash

    # Build and run the application
    docker-compose up app

    # Run tests
    docker-compose up test

    # Run linting
    docker-compose up lint

    # Run type checking
    docker-compose up type-check

Using pip
^^^^^^^^

If you prefer not to use Poetry:

.. code-block:: bash

    pip install -e ".[dev]"
    # OR
    pip install -r dev-requirements.txt

Development Workflow
------------------

Code Quality Tools
~~~~~~~~~~~~~~~~

The project uses several tools to ensure code quality:

.. code-block:: bash

    # Format code with black, isort, and ruff
    make format

    # Run linting with ruff
    make lint

    # Run type checking with mypy
    make type-check

    # Run security checks with bandit
    make security

    # Run all checks at once
    make lint type-check security

Testing
~~~~~~

.. code-block:: bash

    # Run all tests
    make test

    # Run tests with coverage report
    make test-cov

    # Run tests in multiple environments
    make tox

Documentation
~~~~~~~~~~~

.. code-block:: bash

    # Generate API documentation
    make docs

    # Or use the scripts directly
    python scripts/generate_docs.py
    python scripts/generate_api_docs.py

Pre-commit Hooks
~~~~~~~~~~~~~~

The repository is configured with pre-commit hooks that automatically check your code before committing:

- black: Code formatting
- isort: Import sorting
- ruff: Linting
- mypy: Type checking
- Various file checks (trailing whitespace, YAML/TOML validation, etc.)

If any of these checks fail, your commit will be aborted. You can fix the issues and try again, or use ``git commit --no-verify`` to bypass the checks (not recommended).

Project Structure
---------------

.. code-block:: text

    my_python_package/
    ├── pyproject.toml            # Project metadata, dependencies
    ├── setup.cfg                 # Configuration for various tools
    ├── tox.ini                   # Multi-environment testing
    ├── .pre-commit-config.yaml   # Pre-commit hooks configuration
    ├── .editorconfig             # Editor configuration
    ├── Makefile                  # Common development tasks
    ├── src/
    │   └── my_python_package/    # Package source code
    │       ├── __init__.py       # Package exports
    │       ├── __main__.py       # Module execution entry point
    │       ├── core.py           # Core greeting functionality
    │       ├── config.py         # Configuration system
    │       ├── logging.py        # Logging system
    │       └── cli.py            # Command-line interface
    ├── tests/                    # Test directory
    ├── docs/                     # Documentation
    └── scripts/                  # Utility scripts

Commit Guidelines
---------------

The project follows the `Conventional Commits <https://www.conventionalcommits.org/>`_ specification:

.. code-block:: text

    <type>(<scope>): <description>

    [optional body]

    [optional footer(s)]

Types:

- ``feat``: A new feature
- ``fix``: A bug fix
- ``docs``: Documentation changes
- ``style``: Changes that do not affect code logic
- ``refactor``: Code changes that neither fix a bug nor add a feature
- ``perf``: Performance improvements
- ``test``: Adding or correcting tests
- ``build``: Changes to build system or dependencies
- ``ci``: Changes to CI configuration
- ``chore``: Other changes that don't modify source or test files

Examples:

.. code-block:: text

    feat: add random greeting generator
    fix: correct punctuation in formal greetings
    docs: update usage examples in README

Versioning
---------

The project uses `Semantic Versioning <https://semver.org/>`_. Version numbers are automatically bumped based on commit messages:

- ``BREAKING CHANGE`` in the commit message → major version bump
- ``feat:`` prefix → minor version bump
- Otherwise → patch version bump

Publishing
---------

.. code-block:: bash

    # Bump version (done automatically on merge to main)
    make bump-patch   # 0.1.0 -> 0.1.1
    make bump-minor   # 0.1.0 -> 0.2.0
    make bump-major   # 0.1.0 -> 1.0.0

    # Build the package
    make build

    # Publish to TestPyPI
    make publish-test

    # Publish to PyPI
    make publish

Continuous Integration
-------------------

The repository uses GitHub Actions for CI/CD:

- Running tests on multiple Python versions
- Checking code style and quality
- Generating and uploading coverage reports
- Security scanning
- Automatically bumping version numbers
- Publishing to PyPI on release

.. note::
   The CI pipeline will automatically fail if the code does not pass the tests, linting, or type checking.

Development Tips
--------------

Working with Dependencies
~~~~~~~~~~~~~~~~~~~~~~~

To add a new dependency:

.. code-block:: bash

    # Production dependency
    poetry add package-name

    # Development dependency
    poetry add --group dev package-name

To update dependencies:

.. code-block:: bash

    # Update all dependencies
    poetry update

    # Update a specific dependency
    poetry update package-name

Working with Tests
~~~~~~~~~~~~~~~~

To run a specific test:

.. code-block:: bash

    pytest tests/test_core.py::test_hello_default

To run tests with verbose output:

.. code-block:: bash

    pytest -v

To run tests with coverage and see which lines are not covered:

.. code-block:: bash

    pytest --cov=my_python_package --cov-report=term-missing

Debugging Tips
~~~~~~~~~~~~

For interactive debugging, you can use:

.. code-block:: python

    import pdb; pdb.set_trace()  # Python < 3.7
    breakpoint()  # Python >= 3.7

Additional Resources
------------------

- `Poetry documentation <https://python-poetry.org/docs/>`_
- `Black documentation <https://black.readthedocs.io/>`_
- `Ruff documentation <https://beta.ruff.rs/docs/>`_
- `mypy documentation <https://mypy.readthedocs.io/>`_
- `pytest documentation <https://docs.pytest.org/>`_
- `tox documentation <https://tox.wiki/en/latest/>`_
