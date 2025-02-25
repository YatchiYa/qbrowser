# Server Command Client

A command-line client to send browser automation commands via a REST API and poll for answers.

## Installation

No installation required. Just make sure you have Python 3.x and the required dependencies installed.

## Dependencies

- requests
- python 3.x

## Usage

Make sure the `API_KEY` environment variable is set before running any commands.

### As an automation command:

```bash
./cli.py --action screenshot [--xpath XPATH] [--text TEXT] [--url URL]
```

### To query a stored answer:

```bash
./cli.py --query <requestId>
```

### To send HTML content:

```bash
./cli.py --html "<html>...</html>"
```

### To get HTML content from current tab:

```bash
./cli.py --get-html
```

## Project Structure

- `__init__.py`: Package initialization
- `cli.py`: Command-line interface and argument parsing
- `client.py`: API client functionality
- `commands.py`: Command-related functions
- `config.py`: Configuration and constants
- `handlers.py`: Response handling and screenshot saving
- `logger.py`: Logging configuration

## Logging

Logs are written to both stdout and `send_command.log`.
