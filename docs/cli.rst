=======================
Command Line Interface
=======================

``my_python_package`` provides a command-line interface (CLI) for easy access to its functionality.

Basic Usage
----------

The basic syntax for the CLI is:

.. code-block:: bash

    my-python-package COMMAND [ARGS] [OPTIONS]

Available Commands
-----------------

hello
~~~~~

Generate a simple greeting:

.. code-block:: bash

    my-python-package hello NAME [--greeting GREETING]

Examples:

.. code-block:: bash

    my-python-package hello World
    # Output: Hello, World!

    my-python-package hello Python --greeting Hi
    # Output: Hi, Python!

random
~~~~~~

Generate a random greeting:

.. code-block:: bash

    my-python-package random NAME

Example:

.. code-block:: bash

    my-python-package random World
    # Output varies with each run

time
~~~~

Generate a time-based greeting:

.. code-block:: bash

    my-python-package time NAME [--formal]

Examples:

.. code-block:: bash

    my-python-package time World
    # Output depends on time of day:
    # Morning: "Good morning, World!"
    # Afternoon: "Good afternoon, World!"
    # Evening: "Good evening, World!"

    my-python-package time Mrs.Smith --formal
    # Output: "Good day, Mr./Ms. Mrs.Smith!"

format
~~~~~~

Format a greeting with various options:

.. code-block:: bash

    my-python-package format NAME 
                       [--greeting GREETING] 
                       [--punctuation PUNCTUATION]
                       [--uppercase]
                       [--max-length MAX_LENGTH]

Examples:

.. code-block:: bash

    my-python-package format World
    # Output: Hello, World!

    my-python-package format World --greeting Welcome --punctuation "!!!" --uppercase
    # Output: WELCOME, WORLD!!!

    my-python-package format "Very Long Name" --max-length 15
    # Output: Hello, Very...

multi
~~~~~

Greet multiple names:

.. code-block:: bash

    my-python-package multi NAME1 NAME2 ... [--greeting GREETING]

Example:

.. code-block:: bash

    my-python-package multi Alice Bob Charlie
    # Output:
    # Hello, Alice!
    # Hello, Bob!
    # Hello, Charlie!

    my-python-package multi Alice Bob --greeting "Greetings"
    # Output:
    # Greetings, Alice!
    # Greetings, Bob!

config
~~~~~~

Manage configuration settings:

.. code-block:: bash

    my-python-package config SUBCOMMAND [OPTIONS]

Subcommands:

- ``show``: Show current configuration
- ``set``: Set configuration values
- ``add-greeting``: Add a greeting to available greetings
- ``save``: Save configuration to file
- ``load``: Load configuration from file

Examples:

.. code-block:: bash

    # Show current configuration
    my-python-package config show

    # Set default greeting
    my-python-package config set --greeting "Howdy"

    # Set default punctuation
    my-python-package config set --punctuation "?"

    # Set formal title
    my-python-package config set --title "Dr. "

    # Set maximum name length
    my-python-package config set --max-name-length 30

    # Add a greeting
    my-python-package config add-greeting "Salutations"

    # Save configuration to file
    my-python-package config save config.json

    # Load configuration from file
    my-python-package config load config.json

Global Options
------------

The following options are available for all commands:

.. code-block:: bash

    --log-level {debug,info,warning,error,critical}
                          Set logging level
    --log-file LOG_FILE   Path to log file
    --version             Show version information and exit
    --help                Show help message and exit

Examples:

.. code-block:: bash

    # Show help for the hello command
    my-python-package hello --help

    # Show version information
    my-python-package --version

    # Set logging level
    my-python-package hello World --log-level debug

    # Log to file
    my-python-package hello World --log-file greeting.log

Advanced Usage
------------

Scripting
~~~~~~~~

You can use the CLI in shell scripts:

.. code-block:: bash

    #!/bin/bash
    
    # Greet all users in a file
    while read name; do
        my-python-package hello "$name" --greeting "Welcome"
    done < users.txt
    
    # Save and load configuration
    my-python-package config set --greeting "Hi" --punctuation "!"
    my-python-package config save my_config.json
    
    # Later, restore the configuration
    my-python-package config load my_config.json

Output Redirection
~~~~~~~~~~~~~~~~

You can redirect the output to files:

.. code-block:: bash

    # Save greetings to a file
    my-python-package multi Alice Bob Charlie > greetings.txt
    
    # Append more greetings
    my-python-package hello Dave >> greetings.txt

Error Handling
~~~~~~~~~~~~

The CLI will return non-zero exit codes on errors:

.. code-block:: bash

    # Script example with error handling
    if ! my-python-package hello ""; then
        echo "Failed to greet empty name"
    fi
