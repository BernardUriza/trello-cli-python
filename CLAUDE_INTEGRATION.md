# Trello CLI - Claude Code Integration Guide

## Quick Start for Claude Code

This guide helps Claude Code instances understand how to use Trello CLI across all projects.

---

## Installation & Access

### Global Access
Trello CLI is globally accessible via PATH:

```bash
# From ANY directory
trello --version          # → Trello CLI v2.0.0
trello boards             # List boards
```

### Project Location
```
~/Documents/trello-cli-python/
```

### Configuration
```
~/.trello_config.json     # API credentials (DO NOT modify)
```

---

## Common Commands

### Board & List Discovery

```bash
# 1. List all boards
trello boards

# 2. Get lists in a board
trello lists <board_id>

# 3. Get cards in a list
trello cards <list_id>
```

### Card Operations

```bash
# Create card
trello add-card <list_id> "Title" "Description"

# Show card details
trello show-card <card_id>

# Move card between lists
trello move-card <card_id> <destination_list_id>

# Update description
trello update-card <card_id> "New description"
```

### Labels & Metadata

```bash
# Add label (valid colors: red, orange, yellow, green, blue, purple, pink, sky, lime, black)
trello add-label <card_id> "red" "P0"
trello add-label <card_id> "blue" "Backend"

# Set due date (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)
trello set-due <card_id> "2025-11-01"
trello set-due <card_id> "2025-11-01T17:00:00"

# Add comment
trello add-comment <card_id> "Completed implementation"
```

### Checklists

```bash
# Create checklist
trello add-checklist <card_id> "Tasks"

# Add item to checklist
trello add-checkitem <card_id> "Tasks" "Write tests"
```

---

## Project-Specific Board IDs

### Portfolio Project
- **Board ID**: `68fcf05e481843db13204397`
- **Board Name**: AI Portfolio Sprint 1 – Core Development
- **Lists**:
  - Ready: `68fcff45adca2da863178ce6`
  - To Do (Sprint): `68fcff46fa7dbc9cc069eaef`
  - In Progress: `68fcff465168c13a1c3edf87`
  - Testing: `68fcff475ac54cc9b01204af`
  - Done: `68fcff48a96dfec5ea4c4f6d`

### Aurity Project
- **Board ID**: `68fd0294041d84ba28dbe4e8`
- **Board Name**: Aurity Framework - Development Board
- **Lists**:
  - To Prioritize: `68fd02a89aa0ef897d681158`
  - Refinement: `68fd02a9e0f326d7aacff9e8`
  - Ready: `68fd02aa3a4de154fbb36e40`
  - To Do (Sprint): `68fd02ab091980b4ec8f6391`
  - In Progress: `68fd02ab2d8587de405fee22`
  - Testing: `68fd02ac0a1ec7140c542ad3`
  - Done: `68fd02adfbd640d873339572`
  - Philosophy & Architecture: `68fd02ae7ba0e5b4d38d4427`

---

## Agile Workflow Pattern

### Daily Card Management

```bash
# Morning: Check cards to work on
trello cards <sprint_list_id>

# Start work: Move to In Progress
trello move-card <card_id> <in_progress_list_id>
trello add-comment <card_id> "Started implementation"

# During work: Update progress
trello add-comment <card_id> "Completed feature X"
trello add-comment <card_id> "Fixed bug Y"

# After implementation: Move to Testing
trello move-card <card_id> <testing_list_id>
trello add-comment <card_id> "Ready for testing"

# After verification: Move to Done
trello move-card <card_id> <done_list_id>
trello add-comment <card_id> "Verified and deployed"
```

### Creating Structured Cards

```bash
# Create card with metadata
trello add-card <list_id> "PF-FEAT-001: New Feature" \
"**Type:** Feature
**Priority:** High
**Estimate:** 3 days
**Tags:** backend, api

## Description
Implement new API endpoint for user management.

## Acceptance Criteria
- [ ] API endpoint created
- [ ] Tests written
- [ ] Documentation updated"

# Add labels
trello add-label <card_id> "red" "P0"
trello add-label <card_id> "blue" "Backend"

# Set due date
trello set-due <card_id> "2025-11-01"
```

---

## Programmatic Usage (Python)

For batch operations or automation:

```python
#!/usr/bin/env python3
import sys
sys.path.insert(0, '/Users/bernardurizaorozco/Documents/trello-cli-python')

from trello_cli.client import get_client

# Get client
client = get_client()

# List boards
boards = client.list_boards()
for board in boards:
    print(f"Board: {board.name} ({board.id})")

# Get lists
board = client.get_board("68fcf05e481843db13204397")
lists = board.list_lists()

# Create card
lst = client.get_list("68fcff46fa7dbc9cc069eaef")
card = lst.add_card(
    name="PF-FEAT-001: New Feature",
    desc="Implementation details here"
)

# Add label
label = board.add_label("P0", "red")
card.add_label(label)

# Set due date
from datetime import datetime
card.set_due(datetime(2025, 11, 1, 17, 0))

# Add comment
card.comment("Started implementation")
```

---

## Best Practices for Claude Code

### When Creating Cards

1. **Use Structured IDs**
   - Format: `PROJECT-MODULE-TYPE-NUM`
   - Example: `PF-BACKEND-FEAT-001`, `AU-INFRA-TASK-012`

2. **Include Metadata in Description**
   ```markdown
   **Type:** Feature | Bug | Enhancement | Task | Documentation
   **Priority:** P0 | P1 | P2 | P3
   **Estimate:** X days/hours
   **Tags:** backend, frontend, infra, testing, etc.
   ```

3. **Add Relevant Labels**
   - Priority: P0 (red), P1 (orange), P2 (yellow)
   - Area: Backend (blue), Frontend (purple), Infra (sky)
   - Type: Feature (green), Bug (red), Tech-debt (yellow)

### When Moving Cards

1. **Always Add Comments**
   - Document what was done
   - Note any blockers or issues
   - Reference commits or PRs if applicable

2. **Follow Workflow**
   - Ready → To Do (Sprint) → In Progress → Testing → Done
   - Don't skip stages
   - Only one card in "In Progress" at a time

3. **Update Due Dates**
   - Set realistic due dates
   - Update if timeline changes
   - Use end-of-workday (17:00) by default

---

## Error Handling

### Common Errors

```bash
# Configuration not found
❌ Configuration file not found.
   Run 'trello config' to set up API credentials.

# Invalid color
❌ Invalid color: pink
   Valid colors: yellow, purple, blue, red, green, orange, black, sky, pink, lime

# Invalid date
❌ Invalid date format: 2025-13-01
   Expected: YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS
```

### Troubleshooting

```bash
# Check if command is available
which trello
# Should output: /Users/bernardurizaorozco/Documents/trello-cli-python/trello

# Check version
trello --version
# Should output: Trello CLI v2.0.0

# View help
trello --help

# Test connection
trello boards
# Should list all accessible Trello boards
```

---

## Integration with Project CLAUDE.md Files

Each project should include this section in their CLAUDE.md:

```markdown
## 📋 Trello Board Organization

**Trello CLI**: `trello` (globally available)
**Documentation**: `~/Documents/trello-cli-python/CLAUDE_INTEGRATION.md`
**Board ID**: `<project_board_id>`

### Quick Commands
\`\`\`bash
trello boards                     # List all boards
trello lists <board_id>           # Show lists
trello cards <list_id>            # Show cards
trello move-card <card_id> <list_id>  # Move card
trello add-comment <card_id> "text"   # Add comment
\`\`\`

**Board URL**: https://trello.com/b/<short_id>/<board_name>
```

---

## Backward Compatibility

### Old Scripts Using `trello-cli.py`

The alias `trello-cli.py` → `trello` ensures backward compatibility:

```bash
# OLD (still works)
python3 ~/trello-cli.py boards
python3 ~/trello-cli.py add-card <list_id> "Title"

# NEW (recommended)
trello boards
trello add-card <list_id> "Title"
```

### Migration Note

For scripts with hardcoded paths, update:
```python
# OLD:
TRELLO_CLI = "/Users/bernardurizaorozco/trello-cli.py"
subprocess.run(["python3", TRELLO_CLI, "boards"])

# NEW:
subprocess.run(["trello", "boards"])
```

---

## Reference Documentation

- **README.md** - User documentation
- **PROJECT_SUMMARY.md** - Architecture and technical details
- **MIGRATION.md** - v1.0 → v2.0 migration guide
- **CONTRIBUTING.md** - Developer guidelines

---

**Last Updated:** 2025-10-25
**Version:** 2.0.0
**Maintainer:** Bernard Uriza Orozco
