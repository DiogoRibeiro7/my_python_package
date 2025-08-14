"""Configuration module for my_python_package."""

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

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
    """Configuration handler for my_python_package."""
    
    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize configuration.
        
        Args:
            config_path: Path to custom config file
        """
        self._config = DEFAULT_CONFIG.copy()
        self._config_path = config_path
        self._load_config()
    
    def _load_config(self) -> None:
        """Load configuration from file if exists."""
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
        
        Raises:
            IOError: If file cannot be written
        """
        save_path = path or self._config_path
        if save_path:
            with open(save_path, "w") as f:
                json.dump(self._config, f, indent=2)
    
    @property
    def default_greeting(self) -> str:
        """Get default greeting."""
        return self._config["default_greeting"]
    
    @default_greeting.setter
    def default_greeting(self, value: str) -> None:
        """Set default greeting."""
        self._config["default_greeting"] = value
    
    @property
    def default_punctuation(self) -> str:
        """Get default punctuation."""
        return self._config["default_punctuation"]
    
    @default_punctuation.setter
    def default_punctuation(self, value: str) -> None:
        """Set default punctuation."""
        self._config["default_punctuation"] = value
    
    @property
    def available_greetings(self) -> List[str]:
        """Get available greetings for random selection."""
        return self._config["available_greetings"]
    
    @available_greetings.setter
    def available_greetings(self, value: List[str]) -> None:
        """Set available greetings."""
        if not isinstance(value, list) or not all(isinstance(x, str) for x in value):
            raise TypeError("Available greetings must be a list of strings")
        self._config["available_greetings"] = value
    
    @property
    def max_name_length(self) -> int:
        """Get maximum name length."""
        return self._config["max_name_length"]
    
    @max_name_length.setter
    def max_name_length(self, value: int) -> None:
        """Set maximum name length."""
        if not isinstance(value, int):
            raise TypeError("Max name length must be an integer")
        if value <= 0:
            raise ValueError("Max name length must be a positive integer")
        self._config["max_name_length"] = value
    
    @property
    def formal_title(self) -> str:
        """Get formal title prefix."""
        return self._config["formal_title"]
    
    @formal_title.setter
    def formal_title(self, value: str) -> None:
        """Set formal title prefix."""
        self._config["formal_title"] = value
    
    def as_dict(self) -> Dict[str, Any]:
        """Get configuration as dictionary."""
        return self._config.copy()


# Global config instance
config = Config()
