=======================
Command Line Interface
=======================

``greeting_toolkit`` provides a command-line interface (CLI) for easy access to its functionality.

Basic Usage
----------

The basic syntax for the CLI is:

.. code-block:: bash

    greeting-toolkit COMMAND [ARGS] [OPTIONS]

Available Commands
-----------------

hello
~~~~~

Generate a simple greeting:

.. code-block:: bash

    greeting-toolkit hello NAME [--greeting GREETING]

Examples:

.. code-block:: bash

    greeting-toolkit hello World
    # Output: Hello, World!

    greeting-toolkit hello Python --greeting Hi
    # Output: Hi, Python!

random
~~~~~~

Generate a random greeting:

.. code-block:: bash

    greeting-toolkit random NAME

Example:

.. code-block:: bash

    greeting-toolkit random World
    # Output varies with each run

time
~~~~

Generate a time-based greeting:

.. code-block:: bash

    greeting-toolkit time NAME [--formal]

Examples:

.. code-block:: bash

    greeting-toolkit time World
    # Output depends on time of day:
    # Morning: "Good morning, World!"
    # Afternoon: "Good afternoon, World!"
    # Evening: "Good evening, World!"

    greeting-toolkit time Mrs.Smith --formal
    # Output: "Good day, Mr./Ms. Mrs.Smith!"

format
~~~~~~

Format a greeting with various options:

.. code-block:: bash

    greeting-toolkit format NAME
                       [--greeting GREETING]
                       [--punctuation PUNCTUATION]
                       [--uppercase]
                       [--max-length MAX_LENGTH]

Examples:

.. code-block:: bash

    greeting-toolkit format World
    # Output: Hello, World!

    greeting-toolkit format World --greeting Welcome --punctuation "!!!" --uppercase
    # Output: WELCOME, WORLD!!!

    greeting-toolkit format "Very Long Name" --max-length 15
    # Output: Hello, Very...

multi
~~~~~

Greet multiple names:

.. code-block:: bash

    greeting-toolkit multi NAME1 NAME2 ... [--greeting GREETING]

Example:

.. code-block:: bash

    greeting-toolkit multi Alice Bob Charlie
    # Output:
    # Hello, Alice!
    # Hello, Bob!
    # Hello, Charlie!

    greeting-toolkit multi Alice Bob --greeting "Greetings"
    # Output:
    # Greetings, Alice!
    # Greetings, Bob!

config
~~~~~~

Manage configuration settings:

.. code-block:: bash

    greeting-toolkit config SUBCOMMAND [OPTIONS]

Subcommands:

- ``show``: Show current configuration
- ``set``: Set configuration values
- ``add-greeting``: Add a greeting to available greetings
- ``save``: Save configuration to file
- ``load``: Load configuration from file

Examples:

.. code-block:: bash

    # Show current configuration
    greeting-toolkit config show

    # Set default greeting
    greeting-toolkit config set --greeting "Howdy"

    # Set default punctuation
    greeting-toolkit config set --punctuation "?"

    # Set formal title
    greeting-toolkit config set --title "Dr. "

    # Set maximum name length
    greeting-toolkit config set --max-name-length 30

    # Add a greeting
    greeting-toolkit config add-greeting "Salutations"

    # Save configuration to file
    greeting-toolkit config save config.json

    # Load configuration from file
    greeting-toolkit config load config.json

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
    greeting-toolkit hello --help

    # Show version information
    greeting-toolkit --version

    # Set logging level
    greeting-toolkit hello World --log-level debug

    # Log to file
    greeting-toolkit hello World --log-file greeting.log

Advanced Usage
------------

Scripting
~~~~~~~~

You can use the CLI in shell scripts:

.. code-block:: bash

    #!/bin/bash

    # Greet all users in a file
    while read name; do
        greeting-toolkit hello "$name" --greeting "Welcome"
    done < users.txt

    # Save and load configuration
    greeting-toolkit config set --greeting "Hi" --punctuation "!"
    greeting-toolkit config save my_config.json

    # Later, restore the configuration
    greeting-toolkit config load my_config.json

Output Redirection
~~~~~~~~~~~~~~~~

You can redirect the output to files:

.. code-block:: bash

    # Save greetings to a file
    greeting-toolkit multi Alice Bob Charlie > greetings.txt

    # Append more greetings
    greeting-toolkit hello Dave >> greetings.txt

Error Handling
~~~~~~~~~~~~

The CLI will return non-zero exit codes on errors:

.. code-block:: bash

    # Script example with error handling
    if ! greeting-toolkit hello ""; then
        echo "Failed to greet empty name"
    fi
