"""Tests for the core module."""

import re
from datetime import datetime
from unittest.mock import patch

import pytest

from my_python_package.core import (
    create_greeting_list,
    format_greeting,
    generate_greeting,
    hello,
    random_greeting,
    validate_name,
)


# Fixtures
@pytest.fixture
def sample_names():
    """Fixture for sample names."""
    return ["Alice", "Bob", "Charlie"]


# Basic hello tests
def test_hello_default():
    """Test the default hello greeting."""
    assert hello("Diogo") == "Hello, Diogo!"


def test_hello_custom_greeting():
    """Test hello with a custom greeting."""
    assert hello("World", greeting="Hi") == "Hi, World!"


def test_hello_empty_name():
    """Test hello with an empty name."""
    assert hello("") == "Hello, !"


def test_hello_invalid_type():
    """Test hello with an invalid type."""
    with pytest.raises(TypeError):
        hello(123)  # type: ignore


# Time-based greeting tests
@pytest.mark.parametrize(
    "hour,expected_prefix",
    [
        (8, "Good morning"),
        (13, "Good afternoon"),
        (20, "Good evening"),
    ],
)
def test_generate_greeting_time_based(hour, expected_prefix):
    """Test time-based greetings at different hours."""
    with patch("my_python_package.core.datetime") as mock_datetime:
        mock_datetime.now.return_value = datetime(2025, 1, 1, hour, 0, 0)
        result = generate_greeting("John", time_based=True)
        assert result == f"{expected_prefix}, John!"


@pytest.mark.parametrize(
    "formal,expected",
    [
        (True, "Good day, Mr./Ms. John!"),
        (False, "Hello, John!"),
    ],
)
def test_generate_greeting_formality(formal, expected):
    """Test formal vs informal greetings."""
    result = generate_greeting("John", formal=formal, time_based=False)
    assert result == expected


# Name validation tests
@pytest.mark.parametrize(
    "name,valid,error",
    [
        ("John", True, None),
        ("", False, "Name cannot be empty"),
        ("J", False, "Name must be at least 2 characters"),
        ("John123", False, "Name cannot contain numbers or special characters"),
        ("John@Doe", False, "Name cannot contain numbers or special characters"),
        ("John-Doe", True, None),  # Hyphen is allowed
        ("John Doe", True, None),  # Space is allowed
    ],
)
def test_validate_name(name, valid, error):
    """Test name validation with various inputs."""
    result, message = validate_name(name)
    assert result == valid
    assert message == error


# Multiple greetings test
def test_create_greeting_list(sample_names):
    """Test creating greetings for multiple names."""
    result = create_greeting_list(sample_names)
    assert result == ["Hello, Alice!", "Hello, Bob!", "Hello, Charlie!"]


def test_create_greeting_list_custom(sample_names):
    """Test creating greetings with custom greeting."""
    result = create_greeting_list(sample_names, greeting="Hi")
    assert result == ["Hi, Alice!", "Hi, Bob!", "Hi, Charlie!"]


def test_create_greeting_list_empty():
    """Test creating greetings with empty list."""
    result = create_greeting_list([])
    assert result == []


# Random greeting test
def test_random_greeting():
    """Test random greeting selection."""
    with patch("my_python_package.core.random.choice", return_value="Hi"):
        result = random_greeting("John")
        assert result == "Hi, John!"


def test_random_greeting_contains_name():
    """Test that random greeting always contains the name."""
    name = "SpecialName123"  # Unique name unlikely to be in greetings list
    result = random_greeting(name)
    assert name in result


# Format greeting tests
@pytest.mark.parametrize(
    "kwargs,expected",
    [
        ({}, "Hello, John!"),
        ({"greeting": "Hi"}, "Hi, John!"),
        ({"punctuation": "."}, "Hello, John."),
        ({"uppercase": True}, "HELLO, JOHN!"),
        ({"max_length": 10}, "Hello, Jo..."),
        (
            {
                "greeting": "Welcome",
                "punctuation": "!!!",
                "uppercase": True,
            },
            "WELCOME, JOHN!!!",
        ),
    ],
)
def test_format_greeting(kwargs, expected):
    """Test formatting greetings with various options."""
    result = format_greeting("John", **kwargs)
    assert result == expected


def test_format_greeting_max_length_no_truncation():
    """Test max_length that doesn't require truncation."""
    result = format_greeting("John", max_length=100)
    assert result == "Hello, John!"
    assert "..." not in result


# Integration tests
def test_greeting_chain():
    """Test chaining multiple greeting functions."""
    name = "Test"
    # Validate the name
    is_valid, _ = validate_name(name)
    assert is_valid
    
    # Generate a basic greeting
    greeting = hello(name)
    assert greeting == "Hello, Test!"
    
    # Format the greeting
    formatted = format_greeting(name, uppercase=True)
    assert formatted == "HELLO, TEST!"
