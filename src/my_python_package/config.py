"""Configuration module for my_python_package."""

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Union, cast

# Default configuration
DEFAULT_CONFIG: Dict[str, Any] = {
    "default_greeting": "Hello",
    "default_punctuation": "!",
    "available_greetings": [
        "Hello", "Hi", "Hey", "Greetings", "Hey there",
        "Howdy", "Welcome", "Good to see you"
    ],
    "max_name_length": 50,
    "formal_title": "Mr./Ms. ",
}


class Config:
    """
    Configuration handler for my_python_package.

    Manages package configuration with defaults and optional loading from file.
    Configuration can be saved to and loaded from JSON files.

    Examples:
        >>> # Create a config with default values
        >>> cfg = Config()
        >>> cfg.default_greeting
        'Hello'

        >>> # Update a configuration value
        >>> cfg.default_greeting = "Howdy"
        >>> cfg.default_greeting
        'Howdy'

        >>> # Get full configuration as dictionary
        >>> config_dict = cfg.as_dict()
        >>> isinstance(config_dict, dict)
        True
        >>> "default_greeting" in config_dict
        True
    """

    def __init__(self, config_path: Optional[Path] = None) -> None:
        """
        Initialize configuration.

        Args:
            config_path: Path to custom config file
                If provided, configuration will be loaded from this file
                If the file doesn't exist or is invalid, defaults will be used

        Examples:
            >>> import tempfile
            >>> import json
            >>> # Create a temporary config file
            >>> with tempfile.NamedTemporaryFile(mode='w+', delete=False) as tmp:
            ...     tmp.write('{"default_greeting": "Hola"}')
            ...     tmp_path = tmp.name
            >>>
            >>> # Load config from file
            >>> cfg = Config(Path(tmp_path))
            >>> cfg.default_greeting
            'Hola'
            >>>
            >>> # Clean up
            >>> import os
            >>> os.unlink(tmp_path)
        """
        self._config: Dict[str, Any] = DEFAULT_CONFIG.copy()
        self._config_path: Optional[Path] = config_path
        self._load_config()

    def _load_config(self) -> None:
        """
        Load configuration from file if exists.

        Checks for a configuration file path either from initialization or
        from the MY_PYTHON_PACKAGE_CONFIG environment variable. If a valid
        JSON file is found, its values are merged with the defaults.
        """
        # Check environment variable first
        env_config = os.environ.get("MY_PYTHON_PACKAGE_CONFIG")
        if env_config:
            try:
                self._config_path = Path(env_config)
            except Exception:
                pass

        # Try loading from file
        if self._config_path and self._config_path.exists():
            try:
                with open(self._config_path, "r") as f:
                    user_config = json.load(f)
                    self._config.update(user_config)
            except (json.JSONDecodeError, IOError, OSError):
                # Fall back to defaults on error
                pass

    def save_config(self, path: Optional[Path] = None) -> None:
        """
        Save current configuration to file.

        Args:
            path: Path to save config (defaults to current config path)
                If None, uses the path provided during initialization

        Raises:
            IOError: If file cannot be written

        Examples:
            >>> import tempfile
            >>> import json
            >>> import os
            >>> from pathlib import Path
            >>>
            >>> # Create a config and modify it
            >>> cfg = Config()
            >>> cfg.default_greeting = "Bonjour"
            >>>
            >>> # Save to a temporary file
            >>> with tempfile.TemporaryDirectory() as tmp_dir:
            ...     tmp_path = Path(tmp_dir) / "config.json"
            ...     cfg.save_config(tmp_path)
            ...
            ...     # Verify saved correctly
            ...     with open(tmp_path, "r") as f:
            ...         saved_data = json.load(f)
            ...     saved_data["default_greeting"] == "Bonjour"
            True
        """
        save_path: Optional[Path] = path or self._config_path
        if save_path:
            with open(save_path, "w") as f:
                json.dump(self._config, f, indent=2)

    @property
    def default_greeting(self) -> str:
        """
        Get default greeting.

        Returns:
            The configured default greeting

        Examples:
            >>> cfg = Config()
            >>> isinstance(cfg.default_greeting, str)
            True
        """
        return cast(str, self._config["default_greeting"])

    @default_greeting.setter
    def default_greeting(self, value: str) -> None:
        """
        Set default greeting.

        Args:
            value: New default greeting

        Examples:
            >>> cfg = Config()
            >>> original = cfg.default_greeting
            >>> cfg.default_greeting = "Aloha"
            >>> cfg.default_greeting
            'Aloha'
            >>> # Reset for other tests
            >>> cfg.default_greeting = original
        """
        self._config["default_greeting"] = value

    @property
    def default_punctuation(self) -> str:
        """
        Get default punctuation.

        Returns:
            The configured default punctuation

        Examples:
            >>> cfg = Config()
            >>> isinstance(cfg.default_punctuation, str)
            True
        """
        return cast(str, self._config["default_punctuation"])

    @default_punctuation.setter
    def default_punctuation(self, value: str) -> None:
        """
        Set default punctuation.

        Args:
            value: New default punctuation

        Examples:
            >>> cfg = Config()
            >>> original = cfg.default_punctuation
            >>> cfg.default_punctuation = "?"
            >>> cfg.default_punctuation
            '?'
            >>> # Reset for other tests
            >>> cfg.default_punctuation = original
        """
        self._config["default_punctuation"] = value

    @property
    def available_greetings(self) -> List[str]:
        """
        Get available greetings for random selection.

        Returns:
            List of greeting strings

        Examples:
            >>> cfg = Config()
            >>> greetings = cfg.available_greetings
            >>> isinstance(greetings, list)
            True
            >>> len(greetings) > 0
            True
            >>> all(isinstance(g, str) for g in greetings)
            True
        """
        return cast(List[str], self._config["available_greetings"])

    @available_greetings.setter
    def available_greetings(self, value: List[str]) -> None:
        """
        Set available greetings.

        Args:
            value: List of greeting strings

        Raises:
            TypeError: If value is not a list of strings

        Examples:
            >>> cfg = Config()
            >>> original = cfg.available_greetings
            >>> cfg.available_greetings = ["Hi", "Hello", "Hey"]
            >>> cfg.available_greetings
            ['Hi', 'Hello', 'Hey']
            >>> # Should raise error for non-string list
            >>> try:
            ...     cfg.available_greetings = [1, 2, 3]  # type: ignore
            ...     assert False, "Should have raised TypeError"
            ... except TypeError:
            ...     True
            True
            >>> # Reset for other tests
            >>> cfg.available_greetings = original
        """
        if not isinstance(value, list) or not all(isinstance(x, str) for x in value):
            raise TypeError("Available greetings must be a list of strings")
        self._config["available_greetings"] = value

    @property
    def max_name_length(self) -> int:
        """
        Get maximum name length.

        Returns:
            Maximum allowed length for names

        Examples:
            >>> cfg = Config()
            >>> isinstance(cfg.max_name_length, int)
            True
            >>> cfg.max_name_length > 0
            True
        """
        return cast(int, self._config["max_name_length"])

    @max_name_length.setter
    def max_name_length(self, value: int) -> None:
        """
        Set maximum name length.

        Args:
            value: New maximum length

        Raises:
            TypeError: If value is not an integer
            ValueError: If value is not positive

        Examples:
            >>> cfg = Config()
            >>> original = cfg.max_name_length
            >>> cfg.max_name_length = 100
            >>> cfg.max_name_length
            100
            >>> # Should raise error for non-positive value
            >>> try:
            ...     cfg.max_name_length = 0
            ...     assert False, "Should have raised ValueError"
            ... except ValueError:
            ...     True
            True
            >>> # Reset for other tests
            >>> cfg.max_name_length = original
        """
        if not isinstance(value, int):
            raise TypeError("Max name length must be an integer")
        if value <= 0:
            raise ValueError("Max name length must be a positive integer")
        self._config["max_name_length"] = value

    @property
    def formal_title(self) -> str:
        """
        Get formal title prefix.

        Returns:
            The configured formal title prefix

        Examples:
            >>> cfg = Config()
            >>> isinstance(cfg.formal_title, str)
            True
        """
        return cast(str, self._config["formal_title"])

    @formal_title.setter
    def formal_title(self, value: str) -> None:
        """
        Set formal title prefix.

        Args:
            value: New formal title prefix

        Examples:
            >>> cfg = Config()
            >>> original = cfg.formal_title
            >>> cfg.formal_title = "Dr. "
            >>> cfg.formal_title
            'Dr. '
            >>> # Reset for other tests
            >>> cfg.formal_title = original
        """
        self._config["formal_title"] = value

    def as_dict(self) -> Dict[str, Any]:
        """
        Get configuration as dictionary.

        Returns:
            A copy of the current configuration dictionary

        Examples:
            >>> cfg = Config()
            >>> cfg_dict = cfg.as_dict()
            >>> isinstance(cfg_dict, dict)
            True
            >>> sorted(cfg_dict.keys()) == sorted(DEFAULT_CONFIG.keys())
            True
            >>> # Verify it's a copy, not the original
            >>> cfg_dict is not cfg._config
            True
        """
        return self._config.copy()


# Global config instance
config = Config()
