"""Tests for the config module."""

import json
import os
from pathlib import Path
from tempfile import NamedTemporaryFile, TemporaryDirectory
from unittest.mock import patch

import pytest

from greeting_toolkit.config import DEFAULT_CONFIG, Config


def test_config_defaults():
    """Test default configuration values."""
    config = Config()
    assert config.default_greeting == DEFAULT_CONFIG["default_greeting"]
    assert config.default_punctuation == DEFAULT_CONFIG["default_punctuation"]
    assert config.available_greetings == DEFAULT_CONFIG["available_greetings"]
    assert config.max_name_length == DEFAULT_CONFIG["max_name_length"]
    assert config.formal_title == DEFAULT_CONFIG["formal_title"]


def test_config_setters():
    """Test configuration setters."""
    config = Config()

    # Test basic setters
    config.default_greeting = "Howdy"
    assert config.default_greeting == "Howdy"

    config.default_punctuation = "?"
    assert config.default_punctuation == "?"

    config.formal_title = "Dr. "
    assert config.formal_title == "Dr. "

    # Test list setter
    new_greetings = ["A", "B", "C"]
    config.available_greetings = new_greetings
    assert config.available_greetings == new_greetings

    # Test integer setter
    config.max_name_length = 100
    assert config.max_name_length == 100


def test_config_validation():
    """Test configuration validation."""
    config = Config()

    # Test available_greetings validation
    with pytest.raises(TypeError):
        config.available_greetings = "not a list"

    with pytest.raises(TypeError):
        config.available_greetings = [1, 2, 3]  # Not strings

    # Test max_name_length validation
    with pytest.raises(ValueError):
        config.max_name_length = 0

    with pytest.raises(ValueError):
        config.max_name_length = -10

    with pytest.raises(TypeError):
        config.max_name_length = "not an int"  # type: ignore


def test_config_as_dict():
    """Test converting config to dictionary."""
    config = Config()
    config_dict = config.as_dict()

    # Check it's a copy, not the original
    assert config_dict is not config._config

    # Check values match
    assert config_dict["default_greeting"] == config.default_greeting
    assert config_dict["default_punctuation"] == config.default_punctuation
    assert config_dict["available_greetings"] == config.available_greetings
    assert config_dict["max_name_length"] == config.max_name_length
    assert config_dict["formal_title"] == config.formal_title


def test_config_load_from_file():
    """Test loading configuration from file."""
    # Create a temporary config file
    with NamedTemporaryFile(mode="w", suffix=".json", delete=False) as tmp:
        custom_config = {
            "default_greeting": "Yo",
            "default_punctuation": "!!",
            "max_name_length": 25,
        }
        json.dump(custom_config, tmp)

    try:
        # Load config from the file
        config = Config(Path(tmp.name))

        # Check custom values were loaded
        assert config.default_greeting == "Yo"
        assert config.default_punctuation == "!!"
        assert config.max_name_length == 25

        # Check defaults for values not in file
        assert config.available_greetings == DEFAULT_CONFIG["available_greetings"]
        assert config.formal_title == DEFAULT_CONFIG["formal_title"]
    finally:
        # Clean up
        os.unlink(tmp.name)


def test_config_load_from_env():
    """Test loading configuration from environment variable."""
    # Create a temporary config file
    with NamedTemporaryFile(mode="w", suffix=".json", delete=False) as tmp:
        custom_config = {
            "default_greeting": "Sup",
            "formal_title": "Professor ",
        }
        json.dump(custom_config, tmp)

    try:
        # Set environment variable
        with patch.dict(os.environ, {"GREETING_TOOLKIT_CONFIG": tmp.name}):
            config = Config()  # No path provided, should use env var

            # Check custom values were loaded
            assert config.default_greeting == "Sup"
            assert config.formal_title == "Professor "

            # Check defaults for values not in file
            assert config.default_punctuation == DEFAULT_CONFIG["default_punctuation"]
            assert config.available_greetings == DEFAULT_CONFIG["available_greetings"]
            assert config.max_name_length == DEFAULT_CONFIG["max_name_length"]
    finally:
        # Clean up
        os.unlink(tmp.name)


def test_config_invalid_file():
    """Test behavior with invalid config file."""
    # Create an invalid JSON file
    with NamedTemporaryFile(mode="w", suffix=".json", delete=False) as tmp:
        tmp.write("This is not valid JSON")

    try:
        # Loading should not raise, should use defaults
        config = Config(Path(tmp.name))

        # Check all defaults were used
        assert config.default_greeting == DEFAULT_CONFIG["default_greeting"]
        assert config.default_punctuation == DEFAULT_CONFIG["default_punctuation"]
        assert config.available_greetings == DEFAULT_CONFIG["available_greetings"]
        assert config.max_name_length == DEFAULT_CONFIG["max_name_length"]
        assert config.formal_title == DEFAULT_CONFIG["formal_title"]
    finally:
        # Clean up
        os.unlink(tmp.name)


def test_config_save():
    """Test saving configuration to file."""
    with TemporaryDirectory() as tmp_dir:
        config_path = Path(tmp_dir) / "config.json"

        # Create and modify config
        config = Config()
        config.default_greeting = "Hola"
        config.max_name_length = 75

        # Save config
        config.save_config(config_path)

        # Check file exists
        assert config_path.exists()

        # Load and verify
        with open(config_path) as f:
            saved_config = json.load(f)

        assert saved_config["default_greeting"] == "Hola"
        assert saved_config["max_name_length"] == 75
        assert saved_config["default_punctuation"] == DEFAULT_CONFIG["default_punctuation"]


def test_config_save_to_current_path():
    """Test saving to the current config path."""
    with TemporaryDirectory() as tmp_dir:
        config_path = Path(tmp_dir) / "config.json"

        # Create config with path
        config = Config(config_path)
        config.default_greeting = "Bonjour"

        # Save without specifying path
        config.save_config()

        # Check file exists
        assert config_path.exists()

        # Verify content
        with open(config_path) as f:
            saved_config = json.load(f)

        assert saved_config["default_greeting"] == "Bonjour"
