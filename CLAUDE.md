# Trello CLI - Claude Code Integration Guide (v2.1)

This CLI is designed to be used by Claude Code for managing Trello boards, lists, and cards programmatically.

## What's New in v2.1

🎉 **Major Update**: 20+ new commands for bulk operations, sprint planning, and advanced queries!

### Quick Commands (Shortcuts)
- `quick-start`, `quick-test`, `quick-done` - Move cards through workflow with one command
- `my-cards` - Show all assigned cards in a board
- `card-age` - See how long cards have been in a list

### Sprint Planning
- `sprint-start` - Interactive sprint planning
- `sprint-status` - Visual sprint progress
- `sprint-close` - Close sprint and handle unfinished work
- `sprint-velocity` - Calculate team velocity

### Bulk Operations
- `bulk-move-cards` - Move multiple cards at once
- `bulk-add-label` - Label multiple cards
- `bulk-set-due` - Set due dates in bulk
- `bulk-archive-cards` - Archive multiple cards
- `bulk-create-cards` - Create cards from CSV/JSON

### Advanced Queries
- `cards-by-label` - Find cards by label
- `cards-due-soon` - Find cards due soon
- `cards-overdue` - Find overdue cards
- `list-metrics` - Get list analytics
- `board-health` - Board health check

### Board Standardization & Agile Conformity
- `list-templates` - Show available board templates (agile, kanban, basic)
- `standardize-lists` - Apply standard list structure to any board
- `scrum-check` - Validate board conformity with Agile/Scrum practices
- `migrate-cards` - Move cards between boards for reorganization

## Quick Start for Claude Code

**IMPORTANT**: Always run `trello help-json` at the beginning of any session to understand all available commands.

## Discovery Commands (Essential for Claude Code)

These commands help you understand the structure and content of Trello boards:

### 1. Get All Available Commands
```bash
trello help-json
```
Returns a JSON object with all available commands, their arguments, and usage information. Use this to understand what operations are possible.

### 2. Board Overview
```bash
trello board-overview <board_id>
```
Get a complete overview of a board including:
- Board name and ID
- All lists with their IDs
- Card count per list
- Active/archived status
- Summary statistics

**Use this when**: You need to understand the structure of a board or find which lists contain cards.

### 3. Quick ID Reference
```bash
trello board-ids <board_id>
```
Get all useful IDs in one place:
- Board ID
- All list IDs with names
- Recent cards in each list with their IDs

**Use this when**: You need to copy IDs for subsequent operations or want a quick reference.

### 4. Search Cards Across Board
```bash
trello search-cards <board_id> "search query"
```
Search for cards by title or description across all lists in a board. Shows:
- Card name and ID
- List name and ID where the card is located
- Card URL

**Use this when**: Looking for specific cards by keyword without knowing which list they're in.

## Common Workflows for Claude Code

### Workflow 1: Exploring a new board
```bash
# Step 1: List all available boards
trello boards

# Step 2: Get overview of a specific board
trello board-overview <board_id>

# Step 3: Get quick ID reference for subsequent operations
trello board-ids <board_id>
```

### Workflow 2: Finding and modifying a card
```bash
# Step 1: Search for the card
trello search-cards <board_id> "feature name"

# Step 2: View full card details
trello show-card <card_id>

# Step 3: Make modifications
trello update-card <card_id> "new description"
trello add-label <card_id> "red" "Priority"
trello set-due <card_id> "2025-11-01"
```

### Workflow 3: Creating and organizing cards
```bash
# Step 1: Get list IDs
trello lists <board_id>

# Step 2: Create card in specific list
trello add-card <list_id> "Task title" "Task description"

# Step 3: Add checklist items
trello add-checklist <card_id> "Implementation"
trello add-checkitem <card_id> "Implementation" "Setup environment"
trello add-checkitem <card_id> "Implementation" "Write tests"
```

## All Available Commands

Run `trello help-json` for complete command reference with arguments and types.

### Board Operations
- `boards` - List all boards
- `create-board` - Create new board
- `board-overview` - Get complete board structure
- `board-ids` - Get all IDs in a board

### List Operations
- `lists <board_id>` - List all lists in a board
- `create-list <board_id> "name"` - Create new list
- `archive-list <list_id>` - Archive a list

### Card Operations
- `cards <list_id>` - List cards in a list
- `search-cards <board_id> "query"` - Search cards across board
- `add-card <list_id> "title" ["desc"]` - Create new card
- `show-card <card_id>` - View card details
- `update-card <card_id> "description"` - Update card
- `move-card <card_id> <list_id>` - Move card to another list

### Card Enhancements
- `add-label <card_id> "color" ["name"]` - Add colored label
- `add-checklist <card_id> "name"` - Add checklist
- `add-checkitem <card_id> "checklist" "item"` - Add checklist item
- `set-due <card_id> "YYYY-MM-DD"` - Set due date
- `add-comment <card_id> "comment"` - Add comment

## Label Colors
Valid colors: `yellow`, `purple`, `blue`, `red`, `green`, `orange`, `black`, `sky`, `pink`, `lime`

## Tips for Claude Code

1. **Always start with discovery**: Use `board-overview` or `board-ids` to understand the board structure before making changes.

2. **Use search instead of listing everything**: `search-cards` is more efficient than listing all cards in all lists.

3. **Check command availability**: Run `trello help-json` at the start of each session to see what's available.

4. **Every command shows help reminder**: After each successful command, you'll see a reminder to run `trello help`.

5. **IDs are persistent**: Once you get an ID (board, list, or card), you can use it for subsequent operations without re-querying.

## Output Formats

- **Tables**: Most list commands output formatted tables
- **JSON**: Use `help-json` for machine-readable command information
- **Details**: Card details show comprehensive information including checklists, labels, and comments

## Error Handling

Commands will show usage information if called with incorrect arguments:
```bash
❌ Usage: trello command <required_arg> ["optional_arg"]
```

## Examples

```bash
# Get all commands in JSON format (do this first!)
trello help-json

# See board structure
trello board-overview 68fcf05e481843db13204397

# Find cards about "authentication"
trello search-cards 68fcf05e481843db13204397 "auth"

# Create a new feature card
trello add-card 68fcff46fa7dbc9cc069eaef "PF-FEAT-001: User Authentication" "Implement OAuth2"

# Add priority label
trello add-label 68fd24640bf4 "red" "P0"

# Set deadline
trello set-due 68fd24640bf4 "2025-11-01"
```

## Configuration

First time setup:
```bash
trello config
```

This will prompt for:
- Trello API Key
- Trello API Token

Credentials are stored in `~/.trello_cli_config.json`
- Build and publish CLI to PyPI, then remove local alias (400-token PhD mode)
cd ~/Documents/trello-cli && \
rm -f ~/.zshrc_alias_backup && \
alias trello="" && \
python3 -m pip install --upgrade build twine && \
python3 -m build && \
python3 -m twine upload dist/* && \
echo "✅ Published to PyPI. CLI is now globally available via pip install trello-cli" && \
sed -i.bak '/alias trello=/d' ~/.zshrc && \
echo "✅ Removed local alias. Restart shell or run 'hash -r' to clear cache." && \
pip install --force-reinstall trello-cli-fi && \
trello --help