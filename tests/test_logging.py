"""Tests for the logging module."""

import io
import logging
import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from my_python_package.logging import (
    DEFAULT_FORMAT,
    configure_logging,
    get_logger,
    logger,
)


@pytest.fixture
def reset_logger():
    """Reset logger to default state after each test."""
    # Store original handlers and level
    original_handlers = list(logger.handlers)
    original_level = logger.level
    original_propagate = logger.propagate
    
    yield
    
    # Reset to original state
    logger.handlers.clear()
    for handler in original_handlers:
        logger.addHandler(handler)
    logger.setLevel(original_level)
    logger.propagate = original_propagate


def test_default_logger_configuration():
    """Test the default logger configuration."""
    # Verify the logger exists and has the correct name
    assert logger.name == "my_python_package"
    
    # Verify at least one handler is configured (console output)
    assert len(logger.handlers) > 0
    
    # Verify at least one StreamHandler is present
    assert any(isinstance(h, logging.StreamHandler) for h in logger.handlers)


def test_configure_logging_level(reset_logger):
    """Test configuring the logger with different levels."""
    # Test with integer level
    configure_logging(level=logging.DEBUG)
    assert logger.level == logging.DEBUG
    
    # Test with string level
    configure_logging(level="error")
    assert logger.level == logging.ERROR
    
    # Test with invalid string level (should default to INFO)
    configure_logging(level="invalid")
    assert logger.level == logging.INFO


def test_configure_logging_format(reset_logger):
    """Test configuring the logger with a custom format."""
    # Configure with custom format
    custom_format = "%(levelname)s: %(message)s"
    configure_logging(format_str=custom_format)
    
    # Verify the format is applied to handlers
    for handler in logger.handlers:
        assert handler.formatter is not None
        assert handler.formatter._fmt == custom_format


def test_configure_logging_propagate(reset_logger):
    """Test configuring logger propagation."""
    # Default should be no propagation
    configure_logging()
    assert not logger.propagate
    
    # Test with propagation enabled
    configure_logging(propagate=True)
    assert logger.propagate


def test_configure_logging_file(reset_logger):
    """Test configuring logging to a file."""
    # Create a temporary file for logging
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp_path = tmp.name
    
    try:
        # Configure with file
        configure_logging(log_file=tmp_path)
        
        # Verify a FileHandler was added
        file_handlers = [h for h in logger.handlers if isinstance(h, logging.FileHandler)]
        assert len(file_handlers) > 0
        
        # Verify the file handler has the correct path
        for handler in file_handlers:
            assert handler.baseFilename == tmp_path
        
        # Write a log message
        test_message = "Test log message to file"
        logger.info(test_message)
        
        # Verify the message was written to the file
        with open(tmp_path, "r") as f:
            content = f.read()
            assert test_message in content
    
    finally:
        # Clean up
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


def test_configure_logging_file_directory_creation(reset_logger):
    """Test logging to a file in a non-existent directory."""
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as tmp_dir:
        # Create a path to a subdirectory that doesn't exist
        log_dir = Path(tmp_dir) / "logs"
        log_file = log_dir / "test.log"
        
        # Configure logging to this file
        configure_logging(log_file=log_file)
        
        # Verify the directory was created
        assert log_dir.exists()
        
        # Write a log message
        test_message = "Test log message to file in new directory"
        logger.info(test_message)
        
        # Verify the message was written
        assert log_file.exists()
        content = log_file.read_text()
        assert test_message in content


def test_get_logger():
    """Test getting a logger for a specific module."""
    # Get a logger for a module
    module_name = "test_module"
    module_logger = get_logger(module_name)
    
    # Verify the logger has the correct name
    assert module_logger.name == f"my_python_package.{module_name}"
    
    # Verify it's a proper logger instance
    assert isinstance(module_logger, logging.Logger)


def test_logger_output(reset_logger):
    """Test logger output capture."""
    # Create a custom handler with a StringIO buffer
    string_io = io.StringIO()
    string_handler = logging.StreamHandler(string_io)
    string_handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
    
    # Configure logger with this handler
    logger.handlers.clear()
    logger.addHandler(string_handler)
    logger.setLevel(logging.INFO)
    
    # Write a log message
    test_message = "Test log message"
    logger.info(test_message)
    
    # Verify the message was output with the correct format
    output = string_io.getvalue()
    assert f"INFO: {test_message}" in output


def test_environment_variable_configuration():
    """Test configuring logging from environment variables."""
    # Store original environment
    original_env = os.environ.copy()
    
    try:
        # Create a temporary file for logging
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp_path = tmp.name
        
        # Directly call the function we want to test
        from my_python_package.logging import _configure_from_env
        
        # Set environment variables
        os.environ["MY_PYTHON_PACKAGE_LOG_LEVEL"] = "DEBUG"
        os.environ["MY_PYTHON_PACKAGE_LOG_FILE"] = tmp_path
        
        # Call the function with patching
        with patch("my_python_package.logging.configure_logging") as mock_configure:
            _configure_from_env()
            
            # Verify the function was called with the right parameters
            mock_configure.assert_called_once()
            args, kwargs = mock_configure.call_args
            assert kwargs.get("level") == "DEBUG"
            assert kwargs.get("log_file") == tmp_path
        
    finally:
        # Clean up
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
        # Restore original environment
        os.environ.clear()
        os.environ.update(original_env)


def test_logging_levels(reset_logger):
    """Test different logging levels."""
    # Create a StringIO for capturing output
    string_io = io.StringIO()
    string_handler = logging.StreamHandler(string_io)
    string_handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
    
    # Clear existing handlers and add our capture handler
    logger.handlers.clear()
    logger.addHandler(string_handler)
    
    # Configure with debug level
    logger.setLevel(logging.DEBUG)
    
    # Write messages at different levels
    debug_msg = "Debug message"
    info_msg = "Info message"
    warning_msg = "Warning message"
    error_msg = "Error message"
    critical_msg = "Critical message"
    
    logger.debug(debug_msg)
    logger.info(info_msg)
    logger.warning(warning_msg)
    logger.error(error_msg)
    logger.critical(critical_msg)
    
    # Verify all messages were output
    output = string_io.getvalue()
    assert f"DEBUG: {debug_msg}" in output
    assert f"INFO: {info_msg}" in output
    assert f"WARNING: {warning_msg}" in output
    assert f"ERROR: {error_msg}" in output
    assert f"CRITICAL: {critical_msg}" in output
    
    # Reset for next test
    string_io.truncate(0)
    string_io.seek(0)
    
    # Configure with error level
    logger.setLevel(logging.ERROR)
    
    # Write messages at different levels again
    logger.debug(debug_msg)
    logger.info(info_msg)
    logger.warning(warning_msg)
    logger.error(error_msg)
    logger.critical(critical_msg)
    
    # Verify only error and critical messages were output
    output = string_io.getvalue()
    assert f"DEBUG: {debug_msg}" not in output
    assert f"INFO: {info_msg}" not in output
    assert f"WARNING: {warning_msg}" not in output
    assert f"ERROR: {error_msg}" in output
    assert f"CRITICAL: {critical_msg}" in output


def test_nested_logger():
    """Test getting a logger for a nested module."""
    # Get a logger for a nested module
    nested_logger = get_logger("module.submodule")
    
    # Verify the logger has the correct name
    assert nested_logger.name == "my_python_package.module.submodule"
