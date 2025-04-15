#!/usr/bin/env python

import click
import os
import importlib
import pkgutil
from dotenv import load_dotenv
from api import PagerTreeClient

load_dotenv()

@click.group()
@click.option(
    "--config",
    type=click.Path(exists=True, dir_okay=False, readable=True),
    help="Path to configuration file (e.g., config.ini)",
    envvar="PAGERTREE_CONFIG",
)
@click.pass_context
def cli(ctx, config):
    """PagerTree CLI Tool - Manage alerts from the command line."""
    # Initialize PagerTreeClient and store it in the context
    ctx.obj = PagerTreeClient(config_file=config)

# Dynamically register all command groups from the 'commands' package
commands_dir = os.path.join(os.path.dirname(__file__), "commands")
for _, module_name, _ in pkgutil.iter_modules([commands_dir]):
    module = importlib.import_module(f"commands.{module_name}")
    if hasattr(module, module_name):  # Check if the module has a group with the same name
        cli.add_command(getattr(module, module_name))

if __name__ == "__main__":
    cli()