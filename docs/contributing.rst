============
Contributing
============

Thank you for considering contributing to ``my_python_package``! This page provides guidelines for contributing to the project.

Code of Conduct
--------------

Please be respectful and considerate of others when contributing to this project. We aim to foster an inclusive and welcoming community.

For more details, see the :doc:`code_of_conduct`.

Ways to Contribute
-----------------

There are many ways to contribute to the project:

- Reporting bugs
- Suggesting enhancements
- Improving documentation
- Writing code
- Reviewing pull requests

Reporting Bugs
-------------

If you find a bug, please create an issue using the bug report template. Include:

1. A clear title and description
2. Steps to reproduce the behavior
3. Expected behavior
4. Actual behavior
5. Environment details (OS, Python version, package version)

Suggesting Enhancements
----------------------

For feature requests, please use the feature request template. Include:

1. A clear title and description
2. Why this feature would be useful
3. Example code showing how the feature would be used
4. Any potential implementation details

Pull Request Process
------------------

1. Fork the repository
2. Create a new branch (``git checkout -b feature/amazing-feature``)
3. Make your changes
4. Run tests and linting (``make test lint type-check``)
5. Commit your changes using `Conventional Commits <https://www.conventionalcommits.org/>`_ format
6. Push to the branch (``git push origin feature/amazing-feature``)
7. Open a Pull Request using the PR template

Development Environment
---------------------

See the :doc:`development` guide for details on setting up your development environment.

Coding Standards
--------------

We use several tools to maintain code quality:

- **Black**: For code formatting with line length of 100
- **isort**: For import sorting
- **Ruff**: For linting and code quality checks
- **mypy**: For static type checking
- **Bandit**: For security scanning

Our pre-commit hooks automatically check these when you commit.

Style Guide
~~~~~~~~~~

- Follow `PEP 8 <https://pep8.org/>`_ style guidelines
- Use `Google-style docstrings <https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html>`_
- Include type hints for all function parameters and return values
- Write descriptive, self-documenting code
- Keep functions and methods focused on a single responsibility
- Use descriptive variable names

Testing
------

- Write tests for all new functionality
- Maintain or improve test coverage
- Run the full test suite before submitting a PR:

  .. code-block:: bash

      make test-cov  # Run tests with coverage report

Documentation
-----------

- Update documentation for any new features or changes
- Keep docstrings up-to-date with code changes
- Add examples for new functionality

Commit Messages
-------------

Follow the `Conventional Commits <https://www.conventionalcommits.org/>`_ specification:

- ``feat:`` - A new feature
- ``fix:`` - A bug fix
- ``docs:`` - Documentation changes
- ``style:`` - Changes that do not affect code logic (formatting, etc.)
- ``refactor:`` - Code changes that neither fix a bug nor add a feature
- ``perf:`` - Performance improvements
- ``test:`` - Adding or correcting tests
- ``build:`` - Changes to build system or dependencies
- ``ci:`` - Changes to CI configuration
- ``chore:`` - Other changes that don't modify source or test files

Examples:

.. code-block:: text

    feat: add random greeting generator
    fix: correct punctuation in formal greetings
    docs: update usage examples in README
    test: add test case for empty name validation

Getting Help
-----------

If you need help or have questions, you can:

- Open an issue with the "question" label
- Contact the maintainers directly

Thank you for contributing!
