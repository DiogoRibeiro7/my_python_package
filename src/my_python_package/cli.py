"""Command-line interface for my_python_package."""

import argparse
import json
import sys
from pathlib import Path
from typing import List, Optional

from . import __version__
from .config import config
from .core import (
    add_greeting,
    create_greeting_list,
    format_greeting,
    generate_greeting,
    get_config,
    hello,
    random_greeting,
    set_default_greeting,
    set_default_punctuation,
)
from .logging import configure_logging, logger


def parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        prog="my-python-package",
        description="A simple greeting package",
    )

    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )

    parser.add_argument(
        "--log-level",
        choices=["debug", "info", "warning", "error", "critical"],
        help="Set logging level",
    )

    parser.add_argument(
        "--log-file",
        type=str,
        help="Path to log file",
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Basic hello command
    hello_parser = subparsers.add_parser("hello", help="Generate a simple greeting")
    hello_parser.add_argument("name", help="Name to greet")
    hello_parser.add_argument("--greeting", help="Custom greeting")

    # Random greeting command
    random_parser = subparsers.add_parser("random", help="Generate a random greeting")
    random_parser.add_argument("name", help="Name to greet")

    # Time-based greeting command
    time_parser = subparsers.add_parser(
        "time", help="Generate a time-based greeting"
    )
    time_parser.add_argument("name", help="Name to greet")
    time_parser.add_argument(
        "--formal", action="store_true", help="Use formal language"
    )

    # Format greeting command
    format_parser = subparsers.add_parser(
        "format", help="Format a greeting with options"
    )
    format_parser.add_argument("name", help="Name to greet")
    format_parser.add_argument(
        "--greeting", default="Hello", help="Custom greeting"
    )
    format_parser.add_argument(
        "--punctuation", default="!", help="Ending punctuation"
    )
    format_parser.add_argument(
        "--uppercase", action="store_true", help="Convert to uppercase"
    )
    format_parser.add_argument(
        "--max-length", type=int, help="Maximum length (truncates with ...)"
    )

    # Multiple names command
    multi_parser = subparsers.add_parser(
        "multi", help="Greet multiple names"
    )
    multi_parser.add_argument(
        "names", nargs="+", help="Names to greet"
    )
    multi_parser.add_argument(
        "--greeting", default="Hello", help="Custom greeting"
    )

    # Config commands
    config_parser = subparsers.add_parser(
        "config", help="Manage configuration"
    )
    config_subparsers = config_parser.add_subparsers(
        dest="config_command", help="Configuration command"
    )

    # Show config
    config_subparsers.add_parser(
        "show", help="Show current configuration"
    )

    # Set config values
    set_parser = config_subparsers.add_parser(
        "set", help="Set configuration values"
    )
    set_parser.add_argument(
        "--greeting", help="Set default greeting"
    )
    set_parser.add_argument(
        "--punctuation", help="Set default punctuation"
    )
    set_parser.add_argument(
        "--title", help="Set formal title"
    )
    set_parser.add_argument(
        "--max-name-length", type=int, help="Set maximum name length"
    )

    # Add greeting
    add_parser = config_subparsers.add_parser(
        "add-greeting", help="Add a greeting to available greetings"
    )
    add_parser.add_argument(
        "greeting", help="Greeting to add"
    )

    # Save config
    save_parser = config_subparsers.add_parser(
        "save", help="Save configuration to file"
    )
    save_parser.add_argument(
        "path", type=str, help="Path to save configuration"
    )

    # Load config
    load_parser = config_subparsers.add_parser(
        "load", help="Load configuration from file"
    )
    load_parser.add_argument(
        "path", type=str, help="Path to load configuration from"
    )

    return parser.parse_args(args)


def main(args: Optional[List[str]] = None) -> int:
    """
    Run the CLI application.

    Args:
        args: Command line arguments

    Returns:
        Exit code
    """
    parsed_args = parse_args(args)

    # Configure logging if requested
    if parsed_args.log_level or parsed_args.log_file:
        configure_logging(
            level=parsed_args.log_level or "info",
            log_file=parsed_args.log_file,
        )

    # If no command, show help
    if not parsed_args.command:
        print("Error: Please specify a command.")
        return 1

    # Basic greeting commands
    if parsed_args.command == "hello":
        # Add type checking
        if not isinstance(parsed_args.name, str):
            raise TypeError("Name must be a string")

        logger.debug(f"Running hello command for name: {parsed_args.name}")
        result = hello(parsed_args.name, greeting=parsed_args.greeting)
        print(result)

    elif parsed_args.command == "random":
        logger.debug(f"Running random command for name: {parsed_args.name}")
        result = random_greeting(parsed_args.name)
        print(result)

    elif parsed_args.command == "time":
        logger.debug(f"Running time command for name: {parsed_args.name}")
        result = generate_greeting(
            parsed_args.name,
            formal=parsed_args.formal,
            time_based=True,
        )
        print(result)

    elif parsed_args.command == "format":
        logger.debug(f"Running format command for name: {parsed_args.name}")
        result = format_greeting(
            parsed_args.name,
            greeting=parsed_args.greeting,
            punctuation=parsed_args.punctuation,
            uppercase=parsed_args.uppercase,
            max_length=parsed_args.max_length,
        )
        print(result)

    elif parsed_args.command == "multi":
        logger.debug(f"Running multi command for names: {parsed_args.names}")
        results = create_greeting_list(
            parsed_args.names,
            greeting=parsed_args.greeting,
        )
        for greeting in results:
            print(greeting)

    # Config commands
    elif parsed_args.command == "config":
        if not parsed_args.config_command:
            print("Error: Please specify a config command.")
            return 1

        # Show config
        if parsed_args.config_command == "show":
            logger.debug("Running config show command")
            cfg = get_config()
            print(json.dumps(cfg, indent=2))

        # Set config values
        elif parsed_args.config_command == "set":
            logger.debug("Running config set command")
            changed = False

            if parsed_args.greeting is not None:
                set_default_greeting(parsed_args.greeting)
                print(f"Default greeting set to: {parsed_args.greeting}")
                changed = True

            if parsed_args.punctuation is not None:
                set_default_punctuation(parsed_args.punctuation)
                print(f"Default punctuation set to: {parsed_args.punctuation}")
                changed = True

            if parsed_args.title is not None:
                config.formal_title = parsed_args.title
                print(f"Formal title set to: {parsed_args.title}")
                changed = True

            if parsed_args.max_name_length is not None:
                config.max_name_length = parsed_args.max_name_length
                print(f"Max name length set to: {parsed_args.max_name_length}")
                changed = True

            if not changed:
                print("No configuration values were changed.")

        # Add greeting
        elif parsed_args.config_command == "add-greeting":
            logger.debug(f"Adding greeting: {parsed_args.greeting}")
            add_greeting(parsed_args.greeting)
            print(f"Added greeting: {parsed_args.greeting}")
            print("Available greetings:")
            for greeting in config.available_greetings:
                print(f"- {greeting}")

        # Save config
        elif parsed_args.config_command == "save":
            logger.debug(f"Saving config to: {parsed_args.path}")
            try:
                config.save_config(Path(parsed_args.path))
                print(f"Configuration saved to: {parsed_args.path}")
            except (IOError, OSError) as e:
                print(f"Error saving configuration: {e}")
                return 1

        # Load config
        elif parsed_args.config_command == "load":
            logger.debug(f"Loading config from: {parsed_args.path}")
            try:
                new_config = config.__class__(Path(parsed_args.path))
                # Update global config values
                config.default_greeting = new_config.default_greeting
                config.default_punctuation = new_config.default_punctuation
                config.available_greetings = new_config.available_greetings
                config.max_name_length = new_config.max_name_length
                config.formal_title = new_config.formal_title
                print(f"Configuration loaded from: {parsed_args.path}")
            except (IOError, OSError, json.JSONDecodeError) as e:
                print(f"Error loading configuration: {e}")
                return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
