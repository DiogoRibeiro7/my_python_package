"""Core functionality of my_python_package."""

from __future__ import annotations

import random
import re
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple, Union, cast

from .config import config


def hello(name: str, greeting: Optional[str] = None) -> str:
    """
    Return a personalized greeting message.

    Args:
        name: The name to greet
        greeting: Optional custom greeting, defaults to configured default

    Returns:
        A formatted greeting message

    Raises:
        TypeError: If name is not a string or greeting is not a string

    Examples:
        >>> hello("World")
        'Hello, World!'

        >>> hello("Python", greeting="Hi")
        'Hi, Python!'

        >>> hello("")  # Empty name is allowed
        'Hello, !'

        >>> try:
        ...     hello(123)  # type: ignore
        ...     assert False, "Should have raised TypeError"
        ... except TypeError:
        ...     True
        True

        >>> try:
        ...     hello("World", greeting=123)  # type: ignore
        ...     assert False, "Should have raised TypeError"
        ... except TypeError:
        ...     True
        True
    """
    # Add type checking
    if not isinstance(name, str):
        raise TypeError("Name must be a string")
    if greeting is not None and not isinstance(greeting, str):
        raise TypeError("Greeting must be a string")

    greeting = greeting or config.default_greeting
    return f"{greeting}, {name}!"


def generate_greeting(name: str, formal: bool = False, time_based: bool = False) -> str:
    """
    Generate a context-aware greeting.

    Args:
        name: The name to greet
        formal: Whether to use formal language
        time_based: Whether to adjust greeting based on time of day

    Returns:
        A context-aware greeting

    Examples:
        >>> # Formal greeting test
        >>> generate_greeting("John", formal=True)
        'Good day, Mr./Ms. John!'

        >>> # Standard greeting
        >>> generate_greeting("John", formal=False, time_based=False)
        'Hello, John!'

        >>> # Time-based greeting will vary by time of day
        >>> import re
        >>> # This test will pass regardless of the time of day
        >>> bool(re.match(r'(Good (morning|afternoon|evening)|Hello), John!',
        ...               generate_greeting("John", time_based=True)))
        True

        >>> # Both formal and time-based
        >>> with_title = generate_greeting("John", formal=True, time_based=True)
        >>> "Mr./Ms." in with_title
        True
    """
    if time_based:
        hour = datetime.now().hour
        if hour < 12:
            greeting = "Good morning"
        elif hour < 18:
            greeting = "Good afternoon"
        else:
            greeting = "Good evening"
    else:
        greeting = "Good day" if formal else config.default_greeting

    title = config.formal_title if formal else ""
    return f"{greeting}, {title}{name}!"


def validate_name(name: str) -> Tuple[bool, Optional[str]]:
    """
    Validate a name according to basic rules.

    Rules:
    - Must not be empty
    - Must be at least 2 characters
    - Must not contain numbers or special characters
    - Must not exceed configured max length

    Args:
        name: The name to validate

    Returns:
        A tuple of (is_valid, error_message)

    Examples:
        >>> # Valid name
        >>> validate_name("John")
        (True, None)

        >>> # Empty name
        >>> validate_name("")
        (False, 'Name cannot be empty')

        >>> # Too short
        >>> validate_name("J")
        (False, 'Name must be at least 2 characters')

        >>> # Contains numbers
        >>> validate_name("John123")
        (False, 'Name cannot contain numbers or special characters')

        >>> # Contains special characters
        >>> validate_name("John@Doe")
        (False, 'Name cannot contain numbers or special characters')

        >>> # Valid name with hyphen
        >>> validate_name("John-Doe")
        (True, None)

        >>> # Valid name with space
        >>> validate_name("John Doe")
        (True, None)

        >>> # Very long name (depends on config.max_name_length)
        >>> name = "A" * (config.max_name_length + 1)
        >>> result, error = validate_name(name)
        >>> result
        False
        >>> "cannot exceed" in error if error else False
        True
    """
    if not name:
        return False, "Name cannot be empty"

    if len(name) < 2:
        return False, "Name must be at least 2 characters"

    if len(name) > config.max_name_length:
        return False, f"Name cannot exceed {config.max_name_length} characters"

    if not re.match(r"^[A-Za-z\s-]+$", name):
        return False, "Name cannot contain numbers or special characters"

    return True, None


def create_greeting_list(names: List[str], greeting: Optional[str] = None) -> List[str]:
    """
    Create a list of greetings for multiple names.

    Args:
        names: List of names to greet
        greeting: The greeting to use (defaults to configured default)

    Returns:
        List of greeting messages

    Examples:
        >>> # Default greeting
        >>> create_greeting_list(["Alice", "Bob"])
        ['Hello, Alice!', 'Hello, Bob!']

        >>> # Custom greeting
        >>> create_greeting_list(["Alice", "Bob"], greeting="Hi")
        ['Hi, Alice!', 'Hi, Bob!']

        >>> # Empty list
        >>> create_greeting_list([])
        []

        >>> # Mixed names
        >>> create_greeting_list(["Alice", "", "Bob"])
        ['Hello, Alice!', 'Hello, !', 'Hello, Bob!']

        >>> # Single name
        >>> create_greeting_list(["Charlie"])
        ['Hello, Charlie!']
    """
    greeting = greeting or config.default_greeting
    return [f"{greeting}, {name}!" for name in names]


def random_greeting(name: str) -> str:
    """
    Generate a random greeting from a predefined list.

    Args:
        name: The name to greet

    Returns:
        A random greeting message

    Examples:
        >>> # Control randomness with seed
        >>> import random
        >>> random.seed(42)  # Set seed for reproducible example
        >>> # The exact greeting depends on config.available_greetings
        >>> greeting = random_greeting("Python")
        >>> "Python" in greeting  # Name should be in the greeting
        True
        >>> any(g in greeting for g in config.available_greetings)
        True

        >>> # Verify different calls give different results
        >>> # Reset the seed
        >>> random.seed(None)
        >>> # Get multiple greetings
        >>> greetings = [random_greeting("Test") for _ in range(10)]
        >>> # Count unique greetings - should be more than 1 if truly random
        >>> len(set(greetings)) > 1
        True
    """
    greetings = config.available_greetings
    return f"{random.choice(greetings)}, {name}!"


def format_greeting(
    name: str,
    *,
    greeting: Optional[str] = None,
    punctuation: Optional[str] = None,
    uppercase: bool = False,
    max_length: Optional[int] = None,
) -> str:
    """
    Format a greeting with various options.

    Args:
        name: The name to greet
        greeting: The greeting to use (defaults to configured default)
        punctuation: The ending punctuation (defaults to configured default)
        uppercase: Whether to convert to uppercase
        max_length: Optional maximum length (truncates with ...)

    Returns:
        A formatted greeting

    Examples:
        >>> # Default formatting
        >>> format_greeting("World")
        'Hello, World!'

        >>> # Custom greeting and punctuation
        >>> format_greeting("Python", greeting="Hi", punctuation=".")
        'Hi, Python.'

        >>> # Uppercase
        >>> format_greeting("Python", uppercase=True)
        'HELLO, PYTHON!'

        >>> # Length limit with truncation
        >>> format_greeting("Tremendously Long Name", max_length=20)
        'Hello, Tremendou...'

        >>> # Multiple options
        >>> format_greeting("Python",
        ...                 greeting="Welcome",
        ...                 punctuation="!!!",
        ...                 uppercase=True)
        'WELCOME, PYTHON!!!'

        >>> # Very short max_length
        >>> format_greeting("World", max_length=5)
        '...'

        >>> # Max length that doesn't require truncation
        >>> format_greeting("John", max_length=100)
        'Hello, John!'
    """
    greeting = greeting or config.default_greeting
    punctuation = punctuation or config.default_punctuation

    # Build the full greeting first
    result = f"{greeting}, {name}{punctuation}"

    # Apply truncation BEFORE uppercase
    if max_length is not None and len(result) > max_length:
        if max_length <= 3:
            result = "..."
        else:
            # Truncate to max_length-3, then add "..."
            # For "Hello, John!" with max_length=10:
            # Take "Hello, J" (8 chars) + "..." = "Hello, J..."
            truncated_base = result[:max_length - 3]
            result = truncated_base + "..."

    # Apply uppercase after truncation
    if uppercase:
        result = result.upper()

    return result


def set_default_greeting(greeting: str) -> None:
    """
    Set the default greeting in the configuration.

    Args:
        greeting: New default greeting

    Examples:
        >>> # Save original greeting
        >>> original = config.default_greeting
        >>>
        >>> # Set a new greeting
        >>> set_default_greeting("Howdy")
        >>> config.default_greeting
        'Howdy'
        >>>
        >>> # Verify it's used by default
        >>> hello("World")
        'Howdy, World!'
        >>>
        >>> # Reset to original
        >>> set_default_greeting(original)
    """
    config.default_greeting = greeting


def set_default_punctuation(punctuation: str) -> None:
    """Sets the default punctuation character used in the configuration.

    Args:
        punctuation: The punctuation character to set as default.

    Examples:
        >>> # Save original punctuation
        >>> original = config.default_punctuation
        >>>
        >>> # Set new punctuation
        >>> set_default_punctuation("?")
        >>> config.default_punctuation
        '?'
        >>>
        >>> # Verify it's used by default
        >>> format_greeting("World")
        'Hello, World?'
        >>>
        >>> # Reset to original
        >>> set_default_punctuation(original)
    """
    config.default_punctuation = punctuation


def add_greeting(greeting: str) -> None:
    """Add a greeting to the available greetings list.

    Args:
        greeting: Greeting to add

    Examples:
        >>> # Save original greetings
        >>> original = config.available_greetings.copy()
        >>>
        >>> # Add a new greeting
        >>> add_greeting("Greetings")
        >>> "Greetings" in config.available_greetings
        True
        >>>
        >>> # Adding a duplicate does nothing
        >>> original_length = len(config.available_greetings)
        >>> add_greeting("Greetings")
        >>> len(config.available_greetings) == original_length
        True
        >>>
        >>> # Reset to original
        >>> config.available_greetings = original
    """
    if greeting not in config.available_greetings:
        greetings = config.available_greetings.copy()
        greetings.append(greeting)
        config.available_greetings = greetings


def get_config() -> Dict[str, Any]:
    """Get the current configuration.

    Returns:
        Configuration dictionary

    Examples:
        >>> # Get configuration
        >>> cfg = get_config()
        >>> isinstance(cfg, dict)
        True
        >>>
        >>> # Verify keys
        >>> "default_greeting" in cfg
        True
        >>> "default_punctuation" in cfg
        True
        >>> "available_greetings" in cfg
        True
        >>> "max_name_length" in cfg
        True
        >>> "formal_title" in cfg
        True
    """
    return config.as_dict()

