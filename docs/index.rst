===========================
my_python_package
===========================

A minimal but production-ready Python package scaffold configured for publishing to PyPI.

.. image:: https://img.shields.io/pypi/v/my_python_package.svg
   :target: https://pypi.org/project/my_python_package/
   :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/my_python_package.svg
   :target: https://pypi.org/project/my_python_package/
   :alt: Python Versions

.. image:: https://github.com/DiogoRibeiro7/my_python_package/actions/workflows/test.yml/badge.svg
   :target: https://github.com/DiogoRibeiro7/my_python_package/actions/workflows/test.yml
   :alt: Tests

.. image:: https://img.shields.io/badge/coverage-95%25-brightgreen
   :target: https://codecov.io/gh/DiogoRibeiro7/my_python_package
   :alt: Coverage

.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/licenses/MIT
   :alt: License: MIT

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Code style: black

Features
--------

- 🚀 Modern Python packaging with Poetry
- 🔧 Configurable greeting functions with multiple formatting options
- 🧪 Comprehensive testing suite with 100% coverage
- 📊 Continuous Integration workflows for testing, coverage, and releases
- 🛠️ Code quality tools preconfigured (black, ruff, mypy, isort, pre-commit)
- 📝 Complete documentation with doctests
- 🔄 Automated dependency management and version bumping
- 🔒 Security scanning with Bandit and Trivy
- 🧩 Multi-environment testing with tox

Overview
--------

This package demonstrates a properly structured Python project with modern tooling and configuration.
It provides various greeting functions with configurable options for formatting, randomization, and validation.

.. code-block:: python

    from my_python_package import hello

    # Basic usage
    greeting = hello("World")
    print(greeting)  # Output: Hello, World!

    # With custom greeting
    custom = hello("Python", greeting="Hi")
    print(custom)  # Output: Hi, Python!

Contents
--------

.. toctree::
   :maxdepth: 2
   :caption: User Guide

   installation
   usage
   cli

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   api/modules

.. toctree::
   :maxdepth: 1
   :caption: Development

   contributing
   development
   code_of_conduct
   changelog

Indices and tables
-----------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
