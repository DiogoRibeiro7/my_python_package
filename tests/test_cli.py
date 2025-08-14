"""Tests for the CLI module."""

import sys
from io import StringIO
from unittest.mock import patch

import pytest

from my_python_package.cli import main, parse_args


def test_parse_args_hello():
    """Test parsing hello command arguments."""
    args = parse_args(["hello", "World"])
    assert args.command == "hello"
    assert args.name == "World"
    assert args.greeting is None
    
    args = parse_args(["hello", "World", "--greeting", "Hi"])
    assert args.command == "hello"
    assert args.name == "World"
    assert args.greeting == "Hi"


def test_parse_args_random():
    """Test parsing random command arguments."""
    args = parse_args(["random", "World"])
    assert args.command == "random"
    assert args.name == "World"


def test_parse_args_time():
    """Test parsing time command arguments."""
    args = parse_args(["time", "World"])
    assert args.command == "time"
    assert args.name == "World"
    assert not args.formal
    
    args = parse_args(["time", "World", "--formal"])
    assert args.command == "time"
    assert args.name == "World"
    assert args.formal


def test_parse_args_format():
    """Test parsing format command arguments."""
    args = parse_args(["format", "World"])
    assert args.command == "format"
    assert args.name == "World"
    assert args.greeting == "Hello"
    assert args.punctuation == "!"
    assert not args.uppercase
    assert args.max_length is None
    
    args = parse_args([
        "format", "World",
        "--greeting", "Hi",
        "--punctuation", ".",
        "--uppercase",
        "--max-length", "10",
    ])
    assert args.command == "format"
    assert args.name == "World"
    assert args.greeting == "Hi"
    assert args.punctuation == "."
    assert args.uppercase
    assert args.max_length == 10


def test_parse_args_multi():
    """Test parsing multi command arguments."""
    args = parse_args(["multi", "Alice", "Bob"])
    assert args.command == "multi"
    assert args.names == ["Alice", "Bob"]
    assert args.greeting == "Hello"
    
    args = parse_args(["multi", "Alice", "Bob", "--greeting", "Hi"])
    assert args.command == "multi"
    assert args.names == ["Alice", "Bob"]
    assert args.greeting == "Hi"


def test_main_no_command():
    """Test main function with no command."""
    with patch("sys.stdout", new=StringIO()) as fake_out:
        result = main([])
        assert result == 1
        assert "Error: Please specify a command" in fake_out.getvalue()


@pytest.mark.parametrize(
    "command,args,expected_output",
    [
        (
            "hello",
            ["World"],
            "Hello, World!",
        ),
        (
            "hello",
            ["World", "--greeting", "Hi"],
            "Hi, World!",
        ),
        (
            "format",
            ["World", "--uppercase"],
            "HELLO, WORLD!",
        ),
         (
             "format",
             ["World", "--max-length", "10"],
             "Hello, ...",
         ),
        (
            "multi",
            ["Alice", "Bob"],
            "Hello, Alice!\nHello, Bob!",
        ),
    ],
)
def test_main_commands(command, args, expected_output):
    """Test main function with various commands."""
    with patch("sys.stdout", new=StringIO()) as fake_out:
        result = main([command] + args)
        assert result == 0
        assert expected_output in fake_out.getvalue()


@pytest.mark.parametrize(
    "command,args,expected_in_output",
    [
        (
            "random",
            ["World"],
            "World",  # Name should be in output
        ),
        (
            "time",
            ["World"],
            "World",  # Name should be in output
        ),
    ],
)
def test_main_variable_output_commands(command, args, expected_in_output):
    """Test commands with variable output."""
    with patch("sys.stdout", new=StringIO()) as fake_out:
        result = main([command] + args)
        assert result == 0
        assert expected_in_output in fake_out.getvalue()
