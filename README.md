# Trello CLI v2.1

**Official Python CLI for Trello** - Complete Agile/Scrum workflow management with 48 commands.

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-2.1.0-brightgreen.svg)]()

---

## ✨ Features

- 🤖 **Optimized for Claude Code** - AI-first design with discovery commands
- 🏃 **Sprint Planning** - Complete sprint lifecycle management
- 📦 **Bulk Operations** - Process multiple cards efficiently
- 📊 **Board Standardization** - Enforce Agile/Scrum best practices
- 🔍 **Advanced Queries** - Filter and analyze cards
- ⚡ **Quick Workflows** - Shortcuts for common operations
- 🎯 **48 Commands** - Comprehensive board management

---

## 🆕 What's New in v2.1

### 29 New Commands Across 5 Categories!

1. **Quick Commands** (5) - `quick-start`, `quick-test`, `quick-done`, `my-cards`, `card-age`
2. **Sprint Planning** (4) - `sprint-start`, `sprint-status`, `sprint-close`, `sprint-velocity`
3. **Bulk Operations** (5) - `bulk-move-cards`, `bulk-add-label`, `bulk-set-due`, etc.
4. **Advanced Queries** (5) - `cards-by-label`, `cards-due-soon`, `board-health`, etc.
5. **Board Standardization** (4) - `list-templates`, `standardize-lists`, `scrum-check`, `migrate-cards`

See [CLAUDE.md](CLAUDE.md) for complete details.

---

## 📦 Installation

### Prerequisites

```bash
pip3 install py-trello
```

### Setup

1. **Clone or download this repository**

2. **Add to PATH** (already done if using from `~/Documents/trello-cli-python`)

3. **Configure API credentials:**

```bash
trello config
```

Get your credentials from:
- **API Key**: https://trello.com/app-key
- **Token**: Follow the link provided during config

---

## 🚀 Quick Start

### For Claude Code Users

**🎯 Essential Command:**
```bash
trello help-json    # Get ALL commands in JSON format
```

**Key Discovery Commands:**
```bash
trello boards                              # List all boards
trello board-overview <board_id>           # Complete board structure
trello board-ids <board_id>                # Quick ID reference
trello search-cards <board_id> "query"     # Find cards anywhere
```

📖 **Full Guide**: [CLAUDE.md](CLAUDE.md)

---

## 📚 Command Categories

### 1. Discovery & Help (5 commands)

```bash
trello help                    # Show all commands
trello help-json               # Get commands in JSON
trello board-overview <id>     # Board structure + metrics
trello board-ids <id>          # All IDs in one place
trello search-cards <id> "q"   # Find cards by text
```

### 2. Quick Workflows (5 commands)

```bash
trello quick-start <card_id>   # Move to "In Progress" + comment
trello quick-test <card_id>    # Move to "Testing" + comment
trello quick-done <card_id>    # Move to "Done" + comment
trello my-cards <board_id>     # Show all assigned cards
trello card-age <list_id>      # See how old cards are
```

### 3. Sprint Planning (4 commands)

```bash
trello sprint-start <board_id>    # Start sprint (interactive)
trello sprint-status <board_id>   # Sprint progress dashboard
trello sprint-close <board_id>    # Close sprint + cleanup
trello sprint-velocity <board_id> # Calculate team velocity
```

### 4. Bulk Operations (5 commands)

```bash
# Move multiple cards
trello bulk-move-cards <source_list> <target_list> ["filter"]

# Label multiple cards
trello bulk-add-label cards.txt "red" "Priority"

# Set due dates in bulk
trello bulk-set-due cards.txt "2025-12-31"

# Archive multiple cards
trello bulk-archive-cards <list_id> ["filter"]

# Create cards from CSV/JSON
trello bulk-create-cards <list_id> cards.csv
```

### 5. Advanced Queries (5 commands)

```bash
trello cards-by-label <board_id> "red"     # Find by label
trello cards-due-soon <board_id> [days]    # Due soon (default: 7d)
trello cards-overdue <board_id>            # Overdue cards
trello list-metrics <list_id>              # List analytics
trello board-health <board_id>             # Health check (score 0-100)
```

### 6. Board Standardization ⭐ NEW (4 commands)

```bash
trello list-templates                      # Show available templates
trello standardize-lists <id> agile        # Apply template to board
trello scrum-check <board_id>              # Validate Agile conformity
trello migrate-cards <list> <board>        # Move cards between boards
```

### 7. Basic CRUD (15+ commands)

```bash
# Boards
trello boards
trello create-board "Name"

# Lists
trello lists <board_id>
trello create-list <board_id> "Name"
trello archive-list <list_id>

# Cards
trello cards <list_id>
trello add-card <list_id> "Title" ["Description"]
trello show-card <card_id>
trello update-card <card_id> "Description"
trello move-card <card_id> <list_id>

# Enhancements
trello add-label <card_id> "color" ["name"]
trello add-checklist <card_id> "Name"
trello add-checkitem <card_id> "Checklist" "Item"
trello set-due <card_id> "YYYY-MM-DD"
trello add-comment <card_id> "Text"
```

---

## 🎯 Common Use Cases

### Use Case 1: Daily Workflow

```bash
# Morning: Check your cards
trello my-cards <board_id>

# Start working on a card
trello quick-start <card_id>

# Move to testing
trello quick-test <card_id>

# Mark as done
trello quick-done <card_id>
```

### Use Case 2: Sprint Planning

```bash
# Check board health
trello scrum-check <board_id>
trello board-health <board_id>

# Start new sprint
trello sprint-start <board_id>

# Monitor progress
trello sprint-status <board_id>

# Close sprint
trello sprint-close <board_id>
trello sprint-velocity <board_id>
```

### Use Case 3: Board Standardization

```bash
# Standardize all company boards
trello list-templates
trello standardize-lists <board_id> agile --dry-run
trello standardize-lists <board_id> agile

# Validate conformity
trello scrum-check <board_id>
```

### Use Case 4: Bulk Cleanup

```bash
# Find overdue cards
trello cards-overdue <board_id>

# Archive old cards
trello bulk-archive-cards <list_id> "2023"

# Move stale cards to backlog
trello card-age <list_id>
trello bulk-move-cards <source> <backlog>
```

---

## 📖 Documentation

### Essential Docs (in root)
- **[README.md](README.md)** - This file
- **[CLAUDE.md](CLAUDE.md)** - Complete Claude Code integration guide

### Additional Docs (in docs/)
- **[docs/README.md](docs/README.md)** - Documentation index
- **[TESTING_GUIDE.md](docs/TESTING_GUIDE.md)** - Pytest setup
- **[REPORTING_GUIDE.md](docs/REPORTING_GUIDE.md)** - Export reports to HTML/PDF

### Developer Docs
- **[PROJECT_SUMMARY.md](docs/development/PROJECT_SUMMARY.md)** - Architecture
- **[CONTRIBUTING.md](docs/development/CONTRIBUTING.md)** - How to contribute
- **[MIGRATION.md](docs/development/MIGRATION.md)** - v1→v2 migration

---

## 🎨 Board Templates

Three standard templates available:

### 1. Agile/Scrum (Full) - 12 lists
```
💡 Ideas → 📥 Inbox → 📋 Backlog → 📋 To Prioritize → 🔍 Refinement
→ ✅ Ready → 📐 Design → 📝 Sprint → ⚙️ In Progress → 🧪 Testing → ✅ Done → 📚 Architecture
```

### 2. Kanban (Simple) - 3 lists
```
📝 To Do → ⚙️ In Progress → ✅ Done
```

### 3. Basic Workflow - 4 lists
```
📋 Backlog → 📝 To Do → ⚙️ In Progress → ✅ Done
```

Apply with:
```bash
trello standardize-lists <board_id> <template>
```

---

## 🔍 Scrum Conformity Checks

The `scrum-check` command validates:

1. ✅ **Required Lists** - Backlog, Ready, Sprint, In Progress, Testing, Done
2. ⚙️ **WIP Limits** - In Progress should have ≤3-5 cards
3. 📝 **Sprint Size** - Sprint should have 5-15 cards
4. 🧪 **Testing Queue** - Testing should have ≤3-5 cards
5. 📋 **Backlog Health** - Should have 10-50 cards

**Score**: 0-100 with recommendations
- 🟢 EXCELLENT (90-100)
- 🟡 GOOD (70-89)
- 🟠 NEEDS WORK (50-69)
- 🔴 CRITICAL (<50)

```bash
trello scrum-check <board_id>
```

---

## 🛠️ Development

### Project Structure

```
trello-cli-python/
├── trello_cli/
│   ├── commands/         # All command modules
│   │   ├── board.py
│   │   ├── list.py
│   │   ├── card.py
│   │   ├── bulk.py       # Bulk operations
│   │   ├── quick.py      # Quick shortcuts
│   │   ├── sprint.py     # Sprint planning
│   │   ├── query.py      # Advanced queries
│   │   ├── standardize.py # Board standardization
│   │   └── ...
│   ├── utils/            # Utilities
│   └── cli.py            # Main CLI entry
├── tests/                # Test suite
├── docs/                 # Documentation
└── trello                # Executable
```

### Running Tests

```bash
pytest tests/
pytest --cov=trello_cli tests/
```

---

## 🤝 Contributing

See [CONTRIBUTING.md](docs/development/CONTRIBUTING.md)

---

## 📝 Examples

### Example 1: Bulk Card Creation

```csv
# cards.csv
title,description,due_date,labels
Feature A,Description A,2025-12-25,red:P0
Feature B,Description B,2025-12-30,blue:Feature
```

```bash
trello bulk-create-cards <list_id> cards.csv
```

### Example 2: Automated Reports

```bash
#!/bin/bash
# Generate daily report
DATE=$(date +%Y-%m-%d)
trello scrum-check <board_id> > "reports/${DATE}_report.txt"
trello board-health <board_id> >> "reports/${DATE}_report.txt"
```

### Example 3: Sprint Automation

```bash
# Start sprint on Monday
trello sprint-start <board_id>

# Daily standup - check status
trello sprint-status <board_id>

# Friday - close sprint
trello sprint-close <board_id>
trello sprint-velocity <board_id>
```

---

## 🎓 For Claude Code

**Claude Code should always start with:**

```bash
trello help-json
```

This returns all available commands in machine-readable format.

**Key commands for AI:**
- `board-overview` - Understand board structure
- `search-cards` - Find cards without knowing their location
- `scrum-check` - Validate board health
- `bulk-*` commands - Process multiple items efficiently

📖 **Complete Guide**: [CLAUDE.md](CLAUDE.md)

---

## 📊 Statistics

- **Total Commands**: 48
- **Command Categories**: 7
- **Board Templates**: 3
- **Lines of Code**: ~5,000
- **Test Coverage**: Expanding

---

## 🔗 Links

- **GitHub**: [bernardurizaorozco/trello-cli-python](https://github.com/bernardurizaorozco/trello-cli-python)
- **Issues**: [Report bugs](https://github.com/bernardurizaorozco/trello-cli-python/issues)
- **Trello API**: [Documentation](https://developer.atlassian.com/cloud/trello/)

---

## 📄 License

MIT License - See [LICENSE](LICENSE)

---

## 👤 Author

**Bernard Uriza Orozco**

---

## 🙏 Acknowledgments

- Built with [py-trello](https://github.com/sarumont/py-trello)
- Designed for [Claude Code](https://claude.com/claude-code)
- Inspired by Agile/Scrum best practices

---

**Version**: 2.1.0
**Last Updated**: 2025-10-27
