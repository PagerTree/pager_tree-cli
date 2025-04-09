#!/usr/bin/env python

import click
import os
import importlib
import pkgutil

@click.group()
def cli():
    """PagerTree CLI Tool - Manage alerts from the command line."""
    pass

# Dynamically register all command groups from the 'commands' package
commands_dir = os.path.join(os.path.dirname(__file__), "commands")
for _, module_name, _ in pkgutil.iter_modules([commands_dir]):
    module = importlib.import_module(f"commands.{module_name}")
    if hasattr(module, module_name):  # Check if the module has a group with the same name
        cli.add_command(getattr(module, module_name))

if __name__ == "__main__":
    cli()