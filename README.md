# PagerTree CLI

![GitHub release](https://img.shields.io/github/v/release/PagerTree/pager_tree-cli)
![Python version](https://img.shields.io/badge/python-3.8%2B-blue)

The PagerTree CLI is a powerful command-line tool for managing incidents, alerts, and on-call schedules in [PagerTree](https://pagertree.com), a modern incident management platform. Designed for sysadmins, DevOps engineers, and IT teams, it lets you interact with PagerTree’s API directly from your terminal, streamlining workflows and automating tasks.

## Features
- Create, view, and manage alerts, teams, broadcasts, and users.
- Filter and search resources with flexible options.
- View results in clean, table-formatted output.
- Configure via environment variables or a simple config file.
- Cross-platform support for macOS, Linux, and Windows.

## Installation

### Prerequisites
- A PagerTree account and API key (get one from the [PagerTree User Settings Page](https://app.pagertree.com/user/settings)).
- Python 3.8+ (optional, only if not using pre-built binaries).

### Option 1: Install Pre-Built Binaries (Recommended)
1. Visit the [releases page](https://github.com/PagerTree/pager_tree-cli/releases).
2. Download the binary for your operating system (e.g., `pagertree`, `pagertree.exe`).
3. Make the binary executable (Linux/macOS):
   ```bash
   chmod +x pagertree
   ```
4. Move the binary to a directory in your PATH (e.g., `/usr/local/bin`):
   ```bash
   mv pagertree /usr/local/bin/
   ```
5. Verify installation:
   ```bash
   pagertree --help
   ```

### Option 2: Install via Python
1. Clone the repository:
   ```bash
   git clone https://github.com/PagerTree/pager_tree-cli.git
   cd pager_tree-cli
   ```
2. Set up a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Run the CLI:
   ```bash
   python pagertree.py --help
   ```

## Configuration

To use the PagerTree CLI, you need to configure your PagerTree API key.

### Option 1: Environment Variable
Set the API key as an environment variable:
```bash
export PAGERTREE_API_KEY=your_api_key_here
```
Add it to your shell profile (e.g., `~/.bashrc`, `~/.zshrc`) for persistence.

### Option 2: Configuration File
Create a `config.ini` file:
```ini
[DEFAULT]
API_KEY = your_api_key_here
```
Specify the config file when running commands:
```bash
pagertree --config config.ini alerts list
```

### Option 3: .env File
Create a `.env` file in the working directory:
```env
PAGERTREE_API_KEY=your_api_key_here
```
The CLI automatically loads the `.env` file.

## Usage

Run `pagertree --help` to see all available commands and options.

### Common Commands
| Command | Description |
|---------|-------------|
| `pagertree alerts list` | List all alerts. |
| `pagertree alerts create --title "Out of Memory" --team-ids "01JT13C98M186XA3QTRFC250MT"` | Create a new alert. |
| `pagertree alerts show "01JT13CYDAMAJDM0G8HR1X8BMY"` | Show details of an alert. |
| `pagertree teams list` | List all teams. |
| `pagertree teams current-oncall "01JT13C98M186XA3QTRFC250MT"` | List current on-call users for a team. |

### Advanced Options
- Filter alerts with search:
  ```bash
  pagertree alerts list --search "NEEDLE IN THE HAYSTACK"
  ```
- Paginate results:
  ```bash
  pagertree alerts list --limit 10 --offset 0
  ```
- Use an alias for alerts:
  ```bash
  pagertree alerts show --alias "oom"
  ```

For more commands, see the [PagerTree CLI Documentation](https://pagertree.com/docs/cli).

## Support

- **Issues**: Report bugs or request features on the [GitHub Issues page](https://github.com/PagerTree/pager_tree-cli/issues).
- **Documentation**: Visit [PagerTree CLI Documentation](https://pagertree.com/docs/cli).
- **Contact**: Email support@pagertree.com for assistance.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
