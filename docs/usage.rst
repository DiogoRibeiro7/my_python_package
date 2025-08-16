=====
Usage
=====

This page demonstrates how to use the various features of ``my_python_package``.

Basic Greeting
-------------

The most basic function is ``hello()``, which returns a simple greeting:

.. code-block:: python

    from my_python_package import hello

    # Basic usage
    greeting = hello("World")
    print(greeting)  # Output: Hello, World!

    # With custom greeting
    custom = hello("Python", greeting="Hi")
    print(custom)  # Output: Hi, Python!

Formatted Greetings
------------------

For more control over the output, use ``format_greeting()``:

.. code-block:: python

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

Multiple Greetings
-----------------

To greet multiple people at once, use ``create_greeting_list()``:

.. code-block:: python

    from my_python_package import create_greeting_list

    # Greet multiple people
    greetings = create_greeting_list(["Alice", "Bob", "Charlie"])
    for greeting in greetings:
        print(greeting)

    # Output:
    # Hello, Alice!
    # Hello, Bob!
    # Hello, Charlie!

Context-Aware Greetings
----------------------

The ``generate_greeting()`` function can adjust the greeting based on the time of day or formality:

.. code-block:: python

    from my_python_package import generate_greeting

    # Time-based greeting (morning/afternoon/evening)
    print(generate_greeting("World", time_based=True))
    # Output varies based on time of day:
    # Morning: "Good morning, World!"
    # Afternoon: "Good afternoon, World!"
    # Evening: "Good evening, World!"

    # Formal greeting
    print(generate_greeting("Mrs. Smith", formal=True))
    # Output: "Good day, Mr./Ms. Mrs. Smith!"

    # Both formal and time-based
    print(generate_greeting("Mrs. Smith", formal=True, time_based=True))
    # Output depends on time of day, but includes formal title

Random Greetings
---------------

For variety, use ``random_greeting()`` to get a different greeting each time:

.. code-block:: python

    from my_python_package import random_greeting

    # Get a random greeting
    print(random_greeting("World"))  # Different greeting each time

Name Validation
--------------

To validate names before using them in greetings, use ``validate_name()``:

.. code-block:: python

    from my_python_package import validate_name

    # Check if a name is valid
    valid, error = validate_name("John")
    if valid:
        print("Name is valid!")
    else:
        print(f"Invalid name: {error}")

    # Invalid examples:
    validate_name("")  # (False, "Name cannot be empty")
    validate_name("J")  # (False, "Name must be at least 2 characters")
    validate_name("John123")  # (False, "Name cannot contain numbers or special characters")

Configuration
------------

You can configure default settings for the package:

.. code-block:: python

    from my_python_package.core import set_default_greeting, set_default_punctuation, add_greeting
    from my_python_package.config import config

    # Set default greeting
    set_default_greeting("Howdy")

    # Set default punctuation
    set_default_punctuation("?")

    # Add a new greeting to the available list
    add_greeting("Salutations")

    # Set maximum name length
    config.max_name_length = 30

    # Set formal title
    config.formal_title = "Dr. "

    # Get the current configuration
    import json
    print(json.dumps(config.as_dict(), indent=2))

Advanced Examples
---------------

Combining Multiple Features
~~~~~~~~~~~~~~~~~~~~~~~~~

You can combine multiple features for more complex behavior:

.. code-block:: python

    from my_python_package import validate_name, format_greeting, hello

    def greet_user(name, formal=False, uppercase=False):
        # First validate the name
        is_valid, error = validate_name(name)
        if not is_valid:
            return f"Cannot greet: {error}"

        # Choose appropriate greeting
        greeting = "Dear" if formal else "Hi"

        # Format the greeting
        return format_greeting(
            name,
            greeting=greeting,
            uppercase=uppercase,
            max_length=20
        )

    # Example usage
    print(greet_user("John"))  # Output: Hi, John!
    print(greet_user("John", formal=True))  # Output: Dear, John!
    print(greet_user("John", uppercase=True))  # Output: HI, JOHN!
    print(greet_user("J"))  # Output: Cannot greet: Name must be at least 2 characters

Creating a Custom Greeting System
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For more advanced use cases, you can create a custom greeting system:

.. code-block:: python

    from my_python_package import format_greeting, random_greeting, generate_greeting
    import random

    class GreetingSystem:
        def __init__(self, default_greeting="Hello"):
            self.default_greeting = default_greeting
            self.greetings_history = {}

        def greet(self, name, greeting_type="standard"):
            # Track greetings per user
            if name not in self.greetings_history:
                self.greetings_history[name] = []

            # Generate greeting based on type
            if greeting_type == "standard":
                result = format_greeting(name, greeting=self.default_greeting)
            elif greeting_type == "random":
                result = random_greeting(name)
            elif greeting_type == "time":
                result = generate_greeting(name, time_based=True)
            elif greeting_type == "formal":
                result = generate_greeting(name, formal=True)
            else:
                result = format_greeting(name, greeting=greeting_type)

            # Record this greeting
            self.greetings_history[name].append(result)

            return result

        def get_greeting_history(self, name):
            return self.greetings_history.get(name, [])

    # Example usage
    greeter = GreetingSystem()
    print(greeter.greet("Alice"))  # Standard: Hello, Alice!
    print(greeter.greet("Alice", "random"))  # Random greeting
    print(greeter.greet("Alice", "time"))  # Time-based greeting
    print(greeter.greet("Bob", "formal"))  # Formal: Good day, Mr./Ms. Bob!
    print(greeter.greet("Bob", "Welcome"))  # Custom: Welcome, Bob!

    # Get history for a user
    print(greeter.get_greeting_history("Alice"))  # List of all greetings for Alice
