# PagerTree CLI

A command-line interface (CLI) tool for interacting with the PagerTree API. This tool allows users to manage alerts and other resources in PagerTree directly from the terminal. Built with Python and `click`, it supports nested commands, pagination, and table-formatted output.

## Features
- Manage PagerTree alerts (`alerts create`, `alerts list`, `alerts show`).
- Pagination support with `--limit`, `--offset`, and `--all` options.
- Pretty table output using `tabulate`.
- Environment variable configuration with `.env` file support.
- Extensible design with dynamic command registration.