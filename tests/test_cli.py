"""Tests for the CLI module."""

from copy import deepcopy
from io import StringIO
from unittest.mock import patch

import pytest

from greeting_toolkit.cli import main, parse_args
from greeting_toolkit.config import DEFAULT_CONFIG
from greeting_toolkit.config import config as global_config

ORIGINAL_DEFAULTS = deepcopy(DEFAULT_CONFIG)


@pytest.fixture(autouse=True)
def reset_config() -> None:
    yield
    DEFAULT_CONFIG.clear()
    DEFAULT_CONFIG.update(deepcopy(ORIGINAL_DEFAULTS))
    global_config._config = deepcopy(ORIGINAL_DEFAULTS)


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

    args = parse_args(
        [
            "format",
            "World",
            "--greeting",
            "Hi",
            "--punctuation",
            ".",
            "--uppercase",
            "--max-length",
            "10",
        ]
    )
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
    ("command", "args", "expected_output"),
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
    ("command", "args", "expected_in_output"),
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


def test_main_config_show():
    """Test showing configuration via CLI."""
    with patch("sys.stdout", new=StringIO()) as fake_out:
        result = main(["config", "show"])
        assert result == 0
        assert "default_greeting" in fake_out.getvalue()


def test_main_config_set():
    """Test setting configuration values via CLI."""
    with patch("sys.stdout", new=StringIO()) as fake_out:
        result = main(
            [
                "config",
                "set",
                "--greeting",
                "Hi",
                "--punctuation",
                ".",
                "--title",
                "Dr. ",
                "--max-name-length",
                "10",
            ]
        )
        output = fake_out.getvalue()
        assert result == 0
        assert "Default greeting set to: Hi" in output
        assert "Default punctuation set to: ." in output
        assert "Formal title set to: Dr. " in output
        assert "Max name length set to: 10" in output


def test_main_config_add_greeting():
    """Test adding a greeting via CLI."""
    with patch("sys.stdout", new=StringIO()) as fake_out:
        result = main(["config", "add-greeting", "Ahoy"])
        output = fake_out.getvalue()
        assert result == 0
        assert "Added greeting: Ahoy" in output


def test_main_config_save_and_load(tmp_path):
    """Test saving and loading configuration via CLI."""
    config_file = tmp_path / "config.json"
    with patch("sys.stdout", new=StringIO()) as fake_out:
        result = main(["config", "save", str(config_file)])
        assert result == 0
        assert config_file.exists()
    with patch("sys.stdout", new=StringIO()) as fake_out:
        result = main(["config", "load", str(config_file)])
        assert result == 0
        assert "Configuration loaded from" in fake_out.getvalue()
