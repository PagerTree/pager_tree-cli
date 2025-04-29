# PagerTree CLI

A command-line interface (CLI) tool for interacting with the PagerTree API. This tool allows users to manage alerts and other resources in PagerTree directly from the terminal. Built with Python and `click`, it supports nested commands, pagination, and table-formatted output.

## Features
- Manage PagerTree objects such as alerts, teams, broadcasts, and users.
- Pagination support with `--limit`, `--offset`, and `--search` options.
- Pretty table output using `tabulate`.
- Environment variable configuration with `.env` file support.
- Support for configuration files `config.ini`.

## Usage
```bash
pagertree [OPTIONS] COMMAND [ARGS...]
```

Run `pagertree --help` to see the list of available commands and options.

### Example Usage
- List all alerts:
    ```bash
    pagertree alerts list
    ```
    OR
    ```bash
    pagertree alerts list --limit 10 --offset 0
    ```
    OR
    ```bash
    pagertree alerts list --search "NEEDLE IN THE HAYSTACK"
    ```
- Create a new alert:
    ```bash
    pagertree alerts create --title "Out of Memory" --alias "oom" --team-ids "01JT13C98M186XA3QTRFC250MT"
    ```
- Show details of a specific alert:
    ```bash
    pagertree alerts show "01JT13CYDAMAJDM0G8HR1X8BMY"
    ```
    OR
    ```bash
    pagertree alerts show --alias "oom"
    ```
- List all teams:
    ```bash
    pagertree teams list
    ```
- List current on-call users for a specific team:
    ```bash
    pagertree teams current-oncall "01JT13C98M186XA3QTRFC250MT"
    ```
- Run a command with a specific configuration file:
    ```bash
    pagertree --config config.ini alerts list
    ```
    OR
    ```bash
    PAGERTREE_CONFIG=config.ini pagertree alerts list
    ```

## Pre-Built Binaries
Pre-built binaries for various platforms are available in the [releases](https://github.com/PagerTree/pager_tree-cli/releases) section. You can download the appropriate binary for your operating system and architecture.

### Source Code Installation & Development
1. Clone the repository:
   ```bash
   git clone
   cd pager_tree-cli
    ```
2. Install dependencies:
    ```bash
    source venv/bin/activate
    pip install -r requirements.txt
    ```
3. Make the script executable:
    ```bash
    chmod +x pagertree.py
    ```
4. Run the script:
    ```bash
    python ./pagertree.py
    ```