"""Core functionality of my_python_package."""

from __future__ import annotations

import random
import re
from datetime import datetime
from typing import Any, List, Optional, Tuple, Union

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
        TypeError: If name is not a string

    Examples:
        >>> hello("World")
        'Hello, World!'

        >>> hello("Python", greeting="Hi")
        'Hi, Python!'
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
        >>> generate_greeting("John", formal=True)
        'Good day, Mr./Ms. John!'

        >>> # Time-based greeting will vary by time of day
        >>> import re
        >>> bool(re.match(r'(Good (morning|afternoon|evening), John!)',
        ...               generate_greeting("John", time_based=True)))
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
        >>> validate_name("John")
        (True, None)

        >>> validate_name("")
        (False, 'Name cannot be empty')

        >>> validate_name("J")
        (False, 'Name must be at least 2 characters')

        >>> validate_name("John123")
        (False, 'Name cannot contain numbers or special characters')
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
        >>> create_greeting_list(["Alice", "Bob"])
        ['Hello, Alice!', 'Hello, Bob!']

        >>> create_greeting_list(["Alice", "Bob"], greeting="Hi")
        ['Hi, Alice!', 'Hi, Bob!']
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
        >>> import random
        >>> random.seed(42)  # Set seed for reproducible example
        >>> random_greeting("Python")  # Will depend on available_greetings config
        'Hey there, Python!'
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
        >>> format_greeting("World")
        'Hello, World!'

        >>> format_greeting("Python", greeting="Hi", punctuation=".")
        'Hi, Python.'

        >>> format_greeting("Python", uppercase=True)
        'HELLO, PYTHON!'

        >>> format_greeting("Tremendously Long Name", max_length=20)
        'Hello, Tremendou...'
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
    """Set the default greeting in the configuration.

    Args:
        greeting: New default greeting

    """
    config.default_greeting = greeting


def set_default_punctuation(punctuation: str) -> None:
    """
    Sets the default punctuation character used in the configuration.

    Args:
        punctuation (str): The punctuation character to set as default.

    Returns:
        None
    """
    config.default_punctuation = punctuation


def add_greeting(greeting: str) -> None:
    """Add a greeting to the available greetings list.

    Args:
        greeting: Greeting to add

    """
    if greeting not in config.available_greetings:
        greetings = config.available_greetings.copy()
        greetings.append(greeting)
        config.available_greetings = greetings


def get_config() -> dict[str, Any]:
    """Get the current configuration.

    Returns:
        Configuration dictionary
    """
    return config.as_dict()
