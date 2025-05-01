#!/usr/bin/env python

import click
import os
import importlib
import pkgutil
import logging
from dotenv import load_dotenv
from api import PagerTreeClient

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ContextObject:
    """Context object to hold client and configuration."""
    def __init__(self, client, logger, verbose=False):
        self.client = client
        self.logger = logger
        self.verbose = verbose

@click.group()
@click.option(
    "--config", "-c",
    type=click.Path(exists=True, dir_okay=False, readable=True),
    help="Path to .env file",
    envvar="PAGERTREE_CONFIG",
)
@click.option(
    "--verbose", "-v",
    is_flag=True,
    help="Enable verbose output"
)
@click.pass_context
def cli(ctx, config, verbose):
    """PagerTree CLI Tool - Manage alerts from the command line."""

    # Load .env file if provided or check for default .env
    config = config or ('.env' if os.path.exists('.env') else None)
    logger.info(f"Loading .env from {config}" if config else "No .env file provided; relying on system environment variables")
    load_dotenv(dotenv_path=config, verbose=True)

    # Determine verbose setting: command-line flag takes precedence over env var
    env_verbose = os.getenv("PAGERTREE_VERBOSE", "false").lower() in ("true", "1", "t")
    verbose = verbose or env_verbose

    # Set logging level based on verbose setting
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)
    logger.debug("Verbose mode enabled")

    # Initialize PagerTreeClient
    client = PagerTreeClient()
    
    # Store context object
    ctx.obj = ContextObject(client=client, logger=logger, verbose=verbose)

# Dynamically register all command groups from the 'commands' package
commands_dir = os.path.join(os.path.dirname(__file__), "commands")
for _, module_name, _ in pkgutil.iter_modules([commands_dir]):
    module = importlib.import_module(f"commands.{module_name}")
    if hasattr(module, module_name):  # Check if the module has a group with the same name
        cli.add_command(getattr(module, module_name))

if __name__ == "__main__":
    cli()