============
Installation
============

From PyPI
---------

The package is available on `PyPI <https://pypi.org/project/greeting-toolkit/>`_, and you can install it using pip:

.. code-block:: bash

    pip install greeting-toolkit

Using Poetry
-----------

If you use `Poetry <https://python-poetry.org/>`_ for dependency management, you can add the package to your project with:

.. code-block:: bash

    poetry add greeting-toolkit

From Source
----------

To install the package from source, first clone the repository:

.. code-block:: bash

    git clone https://github.com/DiogoRibeiro7/greeting-toolkit.git
    cd greeting-toolkit

Then install it using one of the following methods:

Using Poetry (recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    poetry install

Using pip
~~~~~~~~

.. code-block:: bash

    pip install .

Development Installation
----------------------

If you're planning to contribute to the package, you should install it in development mode with all the development dependencies:

.. code-block:: bash

    # Using Poetry (recommended)
    poetry install

    # Set up pre-commit hooks
    pre-commit install

    # Or use the Makefile for one-step setup
    make setup

This will install all the required development tools like pytest, black, ruff, mypy, etc.

Verify Installation
-----------------

To verify that the package is installed correctly, you can run the following Python code:

.. code-block:: python

    from greeting_toolkit import hello

    print(hello("World"))  # Should output: Hello, World!

Or use the command-line interface:

.. code-block:: bash

    greeting-toolkit hello World

This should output: ``Hello, World!``
