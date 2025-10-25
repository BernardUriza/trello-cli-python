# Trello CLI Python

Official Python CLI for Trello board management - Optimized for agile workflows and automation.

## Features

- 🚀 Fast and lightweight
- 📦 Modular architecture
- 🔐 Secure credential management
- 🎯 Designed for CI/CD and scripting
- 📝 Comprehensive card management
- 🏷️ Labels, checklists, comments, due dates
- 🔄 Card movement across lists
- 📊 Board and list operations

## Installation

### Prerequisites

```bash
pip3 install py-trello
```

### Setup

1. Clone or download this repository
2. Configure Trello API credentials:

```bash
./trello config
```

Get your credentials from:
- API Key: https://trello.com/app-key
- Token: Follow the link provided during config

## Usage

### Basic Commands

```bash
# Configuration
./trello config                          # Setup API credentials

# Boards
./trello boards                          # List all boards
./trello create-board "Board Name"       # Create new board

# Lists
./trello lists <board_id>                # Show lists in board
./trello create-list <board_id> "Name"   # Create new list

# Cards
./trello cards <list_id>                 # Show cards in list
./trello add-card <list_id> "Title" ["Description"]
./trello show-card <card_id>             # Card details
./trello move-card <card_id> <list_id>   # Move card
./trello update-card <card_id> "Desc"    # Update description

# Labels
./trello add-label <card_id> "color" "name"

# Checklists
./trello add-checklist <card_id> "Name"
./trello add-checkitem <card_id> "Checklist" "Item"

# Due Dates & Comments
./trello set-due <card_id> "2025-10-27"
./trello add-comment <card_id> "Comment text"
```

### Advanced Usage

#### Scripting Example

```bash
#!/bin/bash
BOARD_ID="68fcf05e481843db13204397"
LIST_ID="68fcff46fa7dbc9cc069eaef"

# Create card with metadata
./trello add-card $LIST_ID "PF-FEAT-001: New Feature" "**Type:** Feature
**Priority:** High
**Estimate:** 3 days"

# Get card ID from output and add labels
CARD_ID="..."
./trello add-label $CARD_ID "red" "P0"
./trello add-label $CARD_ID "blue" "Backend"
./trello set-due $CARD_ID "2025-11-01"
```

#### CSV Import Pattern

See `examples/import_from_csv.py` for batch card creation from CSV files.

## Project Structure

```
trello-cli-python/
├── trello_cli/
│   ├── __init__.py
│   ├── cli.py              # Main CLI entry point
│   ├── client.py           # Trello API client wrapper
│   ├── config.py           # Configuration management
│   ├── commands/
│   │   ├── __init__.py
│   │   ├── board.py        # Board operations
│   │   ├── list.py         # List operations
│   │   ├── card.py         # Card operations
│   │   └── label.py        # Label operations
│   └── utils/
│       ├── __init__.py
│       ├── formatters.py   # Output formatting
│       └── validators.py   # Input validation
├── tests/
│   └── test_commands.py
├── examples/
│   └── import_from_csv.py
├── trello                  # Main executable
├── setup.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Environment Variables

```bash
# Optional: Set default board
export TRELLO_DEFAULT_BOARD="board_id"

# Optional: Output format
export TRELLO_OUTPUT_FORMAT="table"  # or "json"
```

## Development

### Running Tests

```bash
python3 -m pytest tests/
```

### Adding New Commands

1. Create command module in `trello_cli/commands/`
2. Import and register in `trello_cli/cli.py`
3. Add tests in `tests/`

## Compatibility

- Python 3.7+
- macOS, Linux, Windows (WSL)
- Tested with py-trello 0.19.0+

## License

MIT License - Free for personal and commercial use

## Contributing

Pull requests welcome! Please:
1. Follow existing code style
2. Add tests for new features
3. Update README.md

## Author

Bernard Uriza Orozco
- Portfolio: https://github.com/bernardurizaorozco
- Trello Board: [AI Portfolio Sprint 1](https://trello.com/b/vutLDxX3)

## Changelog

### v2.0.0 (2025-10-25)
- ✨ Modular architecture with separate command modules
- 🔧 Improved error handling and validation
- 📚 Comprehensive documentation
- 🧪 Test suite added
- 🎨 Better output formatting

### v1.0.0 (2025-10-20)
- Initial monolithic implementation
- Core commands: boards, lists, cards, labels
- Basic configuration management
