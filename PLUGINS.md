# Trello CLI Plugin Development Guide

**Build production-ready plugins for the Trello CLI**

---

## Table of Contents

1. [Introduction](#introduction)
2. [Quick Start](#quick-start)
3. [Plugin Architecture](#plugin-architecture)
4. [Creating Your First Plugin](#creating-your-first-plugin)
5. [Environment Variables](#environment-variables)
6. [Advanced Examples](#advanced-examples)
7. [Best Practices](#best-practices)
8. [Official Plugins](#official-plugins)

---

## Introduction

The Trello CLI plugin system allows you to extend functionality without modifying core code. Plugins can be written in **any language** and have full access to the Trello API through injected credentials.

### Why Plugins Matter

**Even the board auditor runs as a plugin.**

This isn't a toy feature - it's an architectural statement. If complex workflow analysis can live externally, **anything can**.

The core doesn't need to change for the CLI to evolve.

---

## Quick Start

### Listing Plugins

```bash
# See all available plugins
trello plugin list

# Get detailed info about a plugin
trello plugin info board-audit

# Run a plugin
trello plugin run board-audit <board_id>
```

### Plugin Directory

Plugins are stored in: `~/.trellocli/plugins/`

```bash
# Create plugin directory
mkdir -p ~/.trellocli/plugins/

# Add your plugin
nano ~/.trellocli/plugins/my-plugin.py

# Make it executable
chmod +x ~/.trellocli/plugins/my-plugin.py

# Verify it's detected
trello plugin list
```

---

## Plugin Architecture

### Metadata Header

Every plugin must start with a metadata header:

```python
#!/usr/bin/env python3
# trello-plugin
# name: My Plugin Name
# description: What this plugin does
# usage: plugin run my-plugin [args]
# author: Your Name
# version: 1.0.0
# tags: audit, automation, reporting
```

**Required fields:**
- `trello-plugin` marker (MUST be present)
- `name` - Display name
- `description` - What the plugin does
- `usage` - How to run it
- `author` - Who made it
- `version` - Semantic version (x.y.z)

**Optional fields:**
- `tags` - Comma-separated keywords

### Execution Model

1. User runs: `trello plugin run my-plugin arg1 arg2`
2. CLI injects environment variables (credentials, config paths)
3. CLI executes the plugin with args: `./my-plugin.py arg1 arg2`
4. Plugin output goes directly to terminal
5. Exit code returned to CLI

### Language Support

| Language | Execution Method | Example |
|----------|------------------|---------|
| Python | `python3 plugin.py` | `#!/usr/bin/env python3` |
| Bash | `bash plugin.sh` | `#!/bin/bash` |
| JavaScript | `node plugin.js` | `#!/usr/bin/env node` |
| Ruby | `ruby plugin.rb` | `#!/usr/bin/env ruby` |
| Go | Direct execution | Compile binary, make executable |
| Any other | Direct execution | Make file executable, use shebang |

---

## Creating Your First Plugin

### Example: Card Counter Plugin

Create `~/.trellocli/plugins/card-counter.py`:

```python
#!/usr/bin/env python3
# trello-plugin
# name: Card Counter
# description: Count cards in a specific list
# usage: plugin run card-counter <list_id>
# author: Your Name
# version: 1.0.0

import os
import sys
import requests

def main():
    # Parse arguments
    if len(sys.argv) < 2:
        print("❌ Usage: trello plugin run card-counter <list_id>")
        return 1

    list_id = sys.argv[1]

    # Get credentials from environment
    api_key = os.environ.get('TRELLO_API_KEY')
    token = os.environ.get('TRELLO_TOKEN')
    base_url = os.environ.get('TRELLO_BASE_URL', 'https://api.trello.com/1')

    if not api_key or not token:
        print("❌ Missing API credentials", file=sys.stderr)
        print("   Run 'trello config' to set up credentials", file=sys.stderr)
        return 1

    # Make API call
    try:
        url = f"{base_url}/lists/{list_id}/cards"
        params = {'key': api_key, 'token': token}
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        cards = response.json()

        print(f"✅ List has {len(cards)} card(s)")
        return 0

    except requests.exceptions.RequestException as e:
        print(f"❌ API Error: {e}", file=sys.stderr)
        return 1

if __name__ == '__main__':
    sys.exit(main())
```

Make it executable:

```bash
chmod +x ~/.trellocli/plugins/card-counter.py
```

Run it:

```bash
trello plugin run card-counter 68fcff46fa7dbc9cc069eaef
```

---

## Environment Variables

The CLI injects these variables into every plugin execution:

### Credentials

| Variable | Description | Example |
|----------|-------------|---------|
| `TRELLO_API_KEY` | Your Trello API key | `a1b2c3d4...` |
| `TRELLO_TOKEN` | Your Trello API token | `xyz789...` |
| `TRELLO_USER_ID` | Your Trello user ID | `5a3b1c...` |

### Configuration

| Variable | Description | Value |
|----------|-------------|-------|
| `TRELLO_CONFIG_DIR` | Config directory | `~/.trellocli` |
| `TRELLO_PLUGIN_DIR` | Plugin directory | `~/.trellocli/plugins` |
| `TRELLO_CLI_VERSION` | CLI version | `2.2.0` |
| `TRELLO_BASE_URL` | Trello API base URL | `https://api.trello.com/1` |

### Accessing in Different Languages

**Python:**
```python
import os
api_key = os.environ.get('TRELLO_API_KEY')
token = os.environ.get('TRELLO_TOKEN')
```

**Bash:**
```bash
API_KEY="${TRELLO_API_KEY}"
TOKEN="${TRELLO_TOKEN}"
```

**JavaScript:**
```javascript
const apiKey = process.env.TRELLO_API_KEY;
const token = process.env.TRELLO_TOKEN;
```

**Ruby:**
```ruby
api_key = ENV['TRELLO_API_KEY']
token = ENV['TRELLO_TOKEN']
```

---

## Advanced Examples

### Example: Board Health Reporter

```python
#!/usr/bin/env python3
# trello-plugin
# name: Board Health Reporter
# description: Generate HTML health report for a board
# usage: plugin run board-health <board_id> [output.html]
# author: Your Name
# version: 1.0.0

import os
import sys
import requests
from datetime import datetime

def main():
    if len(sys.argv) < 2:
        print("Usage: trello plugin run board-health <board_id> [output.html]")
        return 1

    board_id = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else 'board-health.html'

    # Get credentials
    api_key = os.environ.get('TRELLO_API_KEY')
    token = os.environ.get('TRELLO_TOKEN')
    base_url = os.environ.get('TRELLO_BASE_URL', 'https://api.trello.com/1')

    if not api_key or not token:
        print("❌ Missing credentials", file=sys.stderr)
        return 1

    # Fetch board data
    try:
        # Get board
        board = requests.get(
            f"{base_url}/boards/{board_id}",
            params={'key': api_key, 'token': token}
        ).json()

        # Get lists
        lists = requests.get(
            f"{base_url}/boards/{board_id}/lists",
            params={'key': api_key, 'token': token, 'filter': 'open'}
        ).json()

        # Count cards
        total_cards = 0
        for lst in lists:
            cards = requests.get(
                f"{base_url}/lists/{lst['id']}/cards",
                params={'key': api_key, 'token': token}
            ).json()
            total_cards += len(cards)

        # Generate HTML report
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Board Health Report - {board['name']}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        h1 {{ color: #0079BF; }}
        .metric {{ background: #f4f5f7; padding: 20px; margin: 10px 0; border-radius: 5px; }}
    </style>
</head>
<body>
    <h1>Board Health Report</h1>
    <h2>{board['name']}</h2>
    <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>

    <div class="metric">
        <h3>Summary</h3>
        <p>Total Lists: {len(lists)}</p>
        <p>Total Cards: {total_cards}</p>
    </div>

    <div class="metric">
        <h3>Lists</h3>
        <ul>
        {''.join([f"<li>{lst['name']}</li>" for lst in lists])}
        </ul>
    </div>
</body>
</html>
"""

        # Write report
        with open(output_file, 'w') as f:
            f.write(html)

        print(f"✅ Health report generated: {output_file}")
        return 0

    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1

if __name__ == '__main__':
    sys.exit(main())
```

### Example: Bash Plugin with curl

```bash
#!/bin/bash
# trello-plugin
# name: Quick Card Creator
# description: Quickly create a card with just a title
# usage: plugin run quick-card <list_id> "Card Title"
# author: Your Name
# version: 1.0.0

set -e

# Check arguments
if [ $# -lt 2 ]; then
    echo "Usage: trello plugin run quick-card <list_id> \"Card Title\""
    exit 1
fi

LIST_ID="$1"
CARD_NAME="$2"

# Get credentials
API_KEY="${TRELLO_API_KEY}"
TOKEN="${TRELLO_TOKEN}"
BASE_URL="${TRELLO_BASE_URL:-https://api.trello.com/1}"

if [ -z "$API_KEY" ] || [ -z "$TOKEN" ]; then
    echo "❌ Missing API credentials" >&2
    exit 1
fi

# Create card
response=$(curl -s -X POST \
    "${BASE_URL}/cards" \
    -d "key=${API_KEY}" \
    -d "token=${TOKEN}" \
    -d "idList=${LIST_ID}" \
    -d "name=${CARD_NAME}")

# Extract card ID
card_id=$(echo "$response" | jq -r '.id')

if [ "$card_id" != "null" ]; then
    echo "✅ Card created: $card_id"
    echo "   Name: $CARD_NAME"
    exit 0
else
    echo "❌ Failed to create card" >&2
    exit 1
fi
```

---

## Best Practices

### 1. Error Handling

```python
# ✅ GOOD: Clear error messages
if not api_key:
    print("❌ Missing API credentials", file=sys.stderr)
    print("   Run 'trello config' to set up", file=sys.stderr)
    return 1

# ❌ BAD: Generic errors
print("Error")
```

### 2. Argument Validation

```python
# ✅ GOOD: Help message with usage
if len(sys.argv) < 2:
    print("❌ Usage: trello plugin run my-plugin <board_id>")
    print("\nExample:")
    print("  trello plugin run my-plugin 68fcf05e481843db13204397")
    return 1

# ❌ BAD: Silent failure
board_id = sys.argv[1] if len(sys.argv) > 1 else ""
```

### 3. Timeouts

```python
# ✅ GOOD: Set timeouts
response = requests.get(url, timeout=30)

# ❌ BAD: No timeout (can hang forever)
response = requests.get(url)
```

### 4. Exit Codes

```python
# ✅ GOOD: Meaningful exit codes
if success:
    return 0  # Success
else:
    return 1  # Generic error

# ❌ BAD: Always return 0
return 0
```

### 5. Output Format

```python
# ✅ GOOD: Structured output
print(f"✅ Found {len(cards)} card(s)")
print(f"   Board: {board['name']}")
print(f"   List: {list_name}")

# ❌ BAD: Unclear output
print(cards)
```

### 6. Documentation

```python
# ✅ GOOD: Complete metadata
# trello-plugin
# name: Card Analyzer
# description: Analyzes card distribution across lists
# usage: plugin run card-analyzer <board_id> [--json]
# author: Your Name
# version: 1.0.0
# tags: analysis, reporting, statistics

# ❌ BAD: Minimal metadata
# trello-plugin
# name: Plugin
```

---

## Official Plugins

### 1. board-audit.py

**Comprehensive workflow auditor (600+ lines)**

**What it validates:**
- 🔴 Cards in Done without due dates
- 🔴 Cards in Done with incomplete checklists
- 🔴 Overdue cards not marked complete
- 🟠 Active cards without due dates
- 🟠 Execution cards without owners
- 🟡 Empty checklists
- 🟡 Pattern violations
- 🟡 Missing descriptions

**Usage:**
```bash
# Run audit
trello plugin run board-audit <board_id>

# JSON output for CI/CD
trello plugin run board-audit <board_id> --json

# With pattern validation
trello plugin run board-audit <board_id> --pattern "PF-[A-Z]+-\\d+"
```

**Why this matters:**
This plugin proves the plugin system can handle complex production logic.
It's not a toy - it's a fully functional auditor with 8 validation rules,
health scoring, and CI/CD integration.

### 2. example-python.py

**Simple Python template showing basic API usage**

```bash
trello plugin run example-python <board_id>
```

### 3. example-bash.sh

**Simple Bash template using curl and jq**

```bash
trello plugin run example-bash <board_id>
```

---

## Plugin Ideas

Here are some plugin ideas to inspire you:

1. **Time Tracker** - Track time spent on cards
2. **Automated Labeler** - Auto-label cards based on patterns
3. **Dependency Checker** - Validate card dependencies
4. **Slack Notifier** - Send Slack notifications for card updates
5. **GitHub Sync** - Sync Trello cards with GitHub issues
6. **Custom Reporter** - Generate custom reports (PDF, Excel, etc.)
7. **Deadline Enforcer** - Warn about approaching deadlines
8. **Card Archiver** - Auto-archive old Done cards
9. **Member Balancer** - Balance workload across team members
10. **Sprint Analyzer** - Analyze sprint metrics and velocity

---

## Troubleshooting

### Plugin Not Found

```bash
# Check if plugin is in correct directory
ls ~/.trellocli/plugins/

# Verify plugin has correct extension or is executable
ls -la ~/.trellocli/plugins/my-plugin.py

# Make it executable
chmod +x ~/.trellocli/plugins/my-plugin.py
```

### Missing trello-plugin Marker

```
⚠️  Warning: Plugin 'my-plugin' is missing trello-plugin marker
```

**Fix:** Add `# trello-plugin` to the beginning of your file

### Credentials Not Working

```bash
# Verify config exists
cat ~/.trello_config.json

# If missing, reconfigure
trello config
```

### Import Errors (Python)

```bash
# Install required libraries
pip3 install requests

# Or use virtual environment
python3 -m venv ~/.trellocli/venv
source ~/.trellocli/venv/bin/activate
pip install requests
```

---

## Contributing Plugins

Want to contribute a plugin to the official collection?

1. Create a well-documented plugin following best practices
2. Test it thoroughly with different boards
3. Add comprehensive metadata
4. Submit a pull request to the repository
5. Include example usage and screenshots

**Quality standards:**
- Complete metadata header
- Error handling for all API calls
- Clear usage examples
- Meaningful exit codes
- Professional output formatting

---

## Conclusion

The plugin system transforms the Trello CLI from a tool into a **platform**.

If the board auditor—the most complex analysis logic—can live as a plugin,
then **anything can**.

Build something useful. Share it with the community. Extend the platform.

**The core doesn't need to change for the CLI to evolve.**

---

**Questions? Issues?**
- GitHub: [trello-cli-python/issues](https://github.com/your-repo/trello-cli-python/issues)
- Documentation: [README.md](README.md)
- Examples: [plugins/](plugins/)
