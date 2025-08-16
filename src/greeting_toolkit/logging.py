"""Logging configuration for greeting_toolkit."""

import logging
import os
import sys
from pathlib import Path
from typing import Literal, overload

# Default log format
DEFAULT_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Package logger
logger: logging.Logger = logging.getLogger("greeting_toolkit")

# Type alias for log levels
LogLevel = int | str | Literal["debug", "info", "warning", "error", "critical"]


@overload
def configure_logging(
    level: LogLevel = logging.INFO,
    format_str: str | None = None,
    log_file: None = None,
    propagate: bool = False,
) -> None: ...


@overload
def configure_logging(
    level: LogLevel = logging.INFO,
    format_str: str | None = None,
    log_file: str | Path = ...,
    propagate: bool = False,
) -> None: ...


def configure_logging(
    level: LogLevel = logging.INFO,
    format_str: str | None = None,
    log_file: str | Path | None = None,
    propagate: bool = False,
) -> None:
    """Configure logging for the package.

    Args:
        level: Logging level (default: INFO)
            Can be an integer level or string name like "debug", "info", etc.
        format_str: Log format string (default: DEFAULT_FORMAT)
            Uses standard Python logging format strings
        log_file: Optional path to log file within current working directory
            If provided, logs will be written to this file in addition to console
            The path is resolved and must be located inside the current working
            directory to prevent writing to unexpected locations
        propagate: Whether to propagate to parent loggers
            When True, logs will also be sent to parent loggers

    Examples:
        >>> import tempfile
        >>> with tempfile.NamedTemporaryFile(dir=".") as temp:
        ...     # Configure with INFO level and a log file within CWD
        ...     configure_logging(level="info", log_file=temp.name)
        ...     # Get the configured level (20 = INFO)
        ...     logger.level == logging.INFO
        True

        >>> # Configure with DEBUG level
        >>> configure_logging(level=logging.DEBUG)
        >>> logger.level == logging.DEBUG
        True

        >>> # Configure with custom format
        >>> configure_logging(format_str="%(levelname)s: %(message)s")
        >>> len(logger.handlers) > 0  # Ensure handlers are configured
        True
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
            file_path = Path(log_file).expanduser().resolve()
            cwd = Path.cwd().resolve()
            if not file_path.is_relative_to(cwd):
                raise ValueError("log_file must be within the current working directory")

            if not file_path.parent.exists():
                file_path.parent.mkdir(parents=True, exist_ok=True)

            file_handler = logging.FileHandler(file_path)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except (OSError, ValueError) as e:
            logger.warning(f"Failed to configure log file: {e}")


def get_logger(name: str) -> logging.Logger:
    """Get a logger for a specific module.

    Args:
        name: Module name (relative to package)

    Returns:
        Configured logger instance

    Examples:
        >>> # Get a logger for a module
        >>> module_logger = get_logger("core")
        >>> module_logger.name
        'greeting_toolkit.core'

        >>> # Get a logger for a nested module
        >>> nested_logger = get_logger("utils.helpers")
        >>> nested_logger.name
        'greeting_toolkit.utils.helpers'
    """
    return logging.getLogger(f"greeting_toolkit.{name}")


# Configure from environment variables if present
def _configure_from_env() -> None:
    """Configure logging from environment variables.

    Reads:
        GREETING_TOOLKIT_LOG_LEVEL: Logging level (debug, info, etc.)
        GREETING_TOOLKIT_LOG_FILE: Path to log file
    """
    env_level: str | None = os.environ.get("GREETING_TOOLKIT_LOG_LEVEL")
    env_file: str | None = os.environ.get("GREETING_TOOLKIT_LOG_FILE")

    if env_level or env_file:
        configure_logging(
            level=env_level or logging.INFO,
            log_file=env_file,
        )


# Default configuration
configure_logging()
_configure_from_env()
