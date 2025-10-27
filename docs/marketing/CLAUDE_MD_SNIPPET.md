# Trello CLI Section for CLAUDE.md Files

Add this section to any project's CLAUDE.md file:

```markdown
## 📋 Trello Board Management

### Trello CLI Tool v2.0

**Global Command**: `trello` (available from any directory)
**Project Location**: `~/Documents/trello-cli-python/`
**Full Documentation**: `~/Documents/trello-cli-python/CLAUDE_INTEGRATION.md`
**Backward Compatible**: `trello-cli.py` alias works for old scripts

### Quick Reference

\`\`\`bash
# Board & List Discovery
trello boards                          # List all boards
trello lists <board_id>                # Show lists in board
trello cards <list_id>                 # Show cards in list

# Card Operations
trello show-card <card_id>             # Show card details
trello add-card <list_id> "Title" "Description"
trello move-card <card_id> <list_id>   # Move to another list
trello update-card <card_id> "New description"

# Metadata
trello add-label <card_id> "red" "P0"  # Add colored label
trello set-due <card_id> "2025-11-01"  # Set due date
trello add-comment <card_id> "Progress update"

# Checklists
trello add-checklist <card_id> "Tasks"
trello add-checkitem <card_id> "Tasks" "Write tests"
\`\`\`

### Valid Label Colors
`red`, `orange`, `yellow`, `green`, `blue`, `purple`, `pink`, `sky`, `lime`, `black`

### Agile Workflow Pattern

1. **Start Work**: `trello move-card <card_id> <in_progress_list_id>`
2. **Update Progress**: `trello add-comment <card_id> "Completed X"`
3. **Complete**: `trello move-card <card_id> <done_list_id>`

### For This Project

**Board ID**: `<PROJECT_BOARD_ID>`
**Board URL**: `<PROJECT_BOARD_URL>`

**Key Lists**:
- Ready: `<ready_list_id>`
- To Do (Sprint): `<sprint_list_id>`
- In Progress: `<in_progress_list_id>`
- Testing: `<testing_list_id>`
- Done: `<done_list_id>`
```

---

## Usage Instructions

1. Copy the section above
2. Replace placeholders:
   - `<PROJECT_BOARD_ID>` - Board ID from `trello boards`
   - `<PROJECT_BOARD_URL>` - Trello board URL
   - `<*_list_id>` - List IDs from `trello lists <board_id>`
3. Paste into project's CLAUDE.md
4. Adjust workflow steps if needed for project-specific lists
