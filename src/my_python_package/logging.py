"""Logging configuration for my_python_package."""

import logging
import os
import sys
from pathlib import Path
from typing import Optional, Union

# Default log format
DEFAULT_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Package logger
logger = logging.getLogger("my_python_package")


def configure_logging(
    level: Union[int, str] = logging.INFO,
    format_str: Optional[str] = None,
    log_file: Optional[Union[str, Path]] = None,
    propagate: bool = False,
) -> None:
    """
    Configure logging for the package.
    
    Args:
        level: Logging level (default: INFO)
        format_str: Log format string (default: DEFAULT_FORMAT)
        log_file: Optional path to log file
        propagate: Whether to propagate to parent loggers
    """
    # Convert string level to int if needed
    if isinstance(level, str):
        level = getattr(logging, level.upper(), logging.INFO)
    
    # Set format
    formatter = logging.Formatter(format_str or DEFAULT_FORMAT)
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Configure logger
    logger.setLevel(level)
    logger.propagate = propagate
    
    # Add console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Add file handler if specified
    if log_file:
        try:
            file_path = Path(log_file)
            # Create directory if it doesn't exist
            if not file_path.parent.exists():
                file_path.parent.mkdir(parents=True, exist_ok=True)
            
            file_handler = logging.FileHandler(file_path)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except (IOError, OSError) as e:
            logger.warning(f"Failed to configure log file: {e}")


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger for a specific module.
    
    Args:
        name: Module name (relative to package)
        
    Returns:
        Configured logger instance
    """
    return logging.getLogger(f"my_python_package.{name}")


# Configure from environment variables if present
def _configure_from_env() -> None:
    """Configure logging from environment variables."""
    env_level = os.environ.get("MY_PYTHON_PACKAGE_LOG_LEVEL")
    env_file = os.environ.get("MY_PYTHON_PACKAGE_LOG_FILE")
    
    if env_level or env_file:
        configure_logging(
            level=env_level or logging.INFO,
            log_file=env_file,
        )


# Default configuration
configure_logging()
_configure_from_env()
