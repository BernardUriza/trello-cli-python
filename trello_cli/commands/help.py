"""
Help and documentation commands
"""

import json


def cmd_help_json():
    """
    Output all available commands in JSON format for Claude Code consumption.
    This helps Claude Code understand what commands are available.
    """
    commands = {
        "cli_name": "trello",
        "description": "Trello CLI - Command-line interface for Trello",
        "commands": {
            "config": {
                "description": "Configure API credentials",
                "usage": "trello config",
                "args": []
            },
            "help-json": {
                "description": "Output all available commands in JSON format",
                "usage": "trello help-json",
                "args": []
            },
            "boards": {
                "description": "List all accessible boards",
                "usage": "trello boards",
                "args": [],
                "output": "Table with board IDs and names"
            },
            "create-board": {
                "description": "Create a new board",
                "usage": "trello create-board \"name\"",
                "args": [
                    {"name": "board_name", "type": "string", "required": True}
                ]
            },
            "board-overview": {
                "description": "Get complete overview of a board with all lists and card counts",
                "usage": "trello board-overview <board_id>",
                "args": [
                    {"name": "board_id", "type": "string", "required": True}
                ],
                "output": "Board details with lists and card counts"
            },
            "board-ids": {
                "description": "Get quick reference of all useful IDs in a board (lists, cards)",
                "usage": "trello board-ids <board_id>",
                "args": [
                    {"name": "board_id", "type": "string", "required": True}
                ],
                "output": "Comprehensive list of IDs for boards, lists, and recent cards"
            },
            "lists": {
                "description": "List all lists in a board",
                "usage": "trello lists <board_id>",
                "args": [
                    {"name": "board_id", "type": "string", "required": True}
                ]
            },
            "create-list": {
                "description": "Create a new list in a board",
                "usage": "trello create-list <board_id> \"name\"",
                "args": [
                    {"name": "board_id", "type": "string", "required": True},
                    {"name": "list_name", "type": "string", "required": True}
                ]
            },
            "archive-list": {
                "description": "Archive (close) a list",
                "usage": "trello archive-list <list_id>",
                "args": [
                    {"name": "list_id", "type": "string", "required": True}
                ]
            },
            "cards": {
                "description": "List all cards in a list",
                "usage": "trello cards <list_id>",
                "args": [
                    {"name": "list_id", "type": "string", "required": True}
                ]
            },
            "search-cards": {
                "description": "Search for cards in a board by title/description with list information",
                "usage": "trello search-cards <board_id> \"query\"",
                "args": [
                    {"name": "board_id", "type": "string", "required": True},
                    {"name": "query", "type": "string", "required": True}
                ],
                "output": "Cards matching query with their list names"
            },
            "add-card": {
                "description": "Add a new card to a list",
                "usage": "trello add-card <list_id> \"title\" [\"description\"]",
                "args": [
                    {"name": "list_id", "type": "string", "required": True},
                    {"name": "title", "type": "string", "required": True},
                    {"name": "description", "type": "string", "required": False}
                ]
            },
            "show-card": {
                "description": "Show detailed card information",
                "usage": "trello show-card <card_id>",
                "args": [
                    {"name": "card_id", "type": "string", "required": True}
                ]
            },
            "update-card": {
                "description": "Update card description",
                "usage": "trello update-card <card_id> \"description\"",
                "args": [
                    {"name": "card_id", "type": "string", "required": True},
                    {"name": "description", "type": "string", "required": True}
                ]
            },
            "move-card": {
                "description": "Move card to another list",
                "usage": "trello move-card <card_id> <list_id>",
                "args": [
                    {"name": "card_id", "type": "string", "required": True},
                    {"name": "list_id", "type": "string", "required": True}
                ]
            },
            "add-label": {
                "description": "Add label to card",
                "usage": "trello add-label <card_id> \"color\" [\"name\"]",
                "args": [
                    {"name": "card_id", "type": "string", "required": True},
                    {"name": "color", "type": "string", "required": True, "values": ["yellow", "purple", "blue", "red", "green", "orange", "black", "sky", "pink", "lime"]},
                    {"name": "name", "type": "string", "required": False}
                ]
            },
            "add-checklist": {
                "description": "Add checklist to card",
                "usage": "trello add-checklist <card_id> \"name\"",
                "args": [
                    {"name": "card_id", "type": "string", "required": True},
                    {"name": "checklist_name", "type": "string", "required": True}
                ]
            },
            "add-checkitem": {
                "description": "Add item to checklist (creates checklist if it doesn't exist)",
                "usage": "trello add-checkitem <card_id> \"checklist\" \"item\"",
                "args": [
                    {"name": "card_id", "type": "string", "required": True},
                    {"name": "checklist_name", "type": "string", "required": True},
                    {"name": "item_name", "type": "string", "required": True}
                ]
            },
            "set-due": {
                "description": "Set due date for a card",
                "usage": "trello set-due <card_id> \"YYYY-MM-DD\"",
                "args": [
                    {"name": "card_id", "type": "string", "required": True},
                    {"name": "due_date", "type": "string", "required": True, "format": "YYYY-MM-DD"}
                ]
            },
            "add-comment": {
                "description": "Add comment to card",
                "usage": "trello add-comment <card_id> \"comment\"",
                "args": [
                    {"name": "card_id", "type": "string", "required": True},
                    {"name": "comment", "type": "string", "required": True}
                ]
            },
            "delete-card": {
                "description": "Delete a card permanently",
                "usage": "trello delete-card <card_id>",
                "args": [
                    {"name": "card_id", "type": "string", "required": True}
                ]
            },
            "board-audit": {
                "description": "Comprehensive board audit: naming patterns, missing members/labels, empty lists, deletion candidates",
                "usage": "trello board-audit <board_id> [\"pattern\"]",
                "args": [
                    {"name": "board_id", "type": "string", "required": True},
                    {"name": "pattern", "type": "string", "required": False, "description": "Regex pattern for card naming validation (e.g., 'PF-[A-Z]+-\\d+')"}
                ]
            },
            "list-audit": {
                "description": "Detailed audit of a specific list with pattern validation",
                "usage": "trello list-audit <list_id> [\"pattern\"]",
                "args": [
                    {"name": "list_id", "type": "string", "required": True},
                    {"name": "pattern", "type": "string", "required": False, "description": "Regex pattern for card naming validation"}
                ]
            },
            "list-snapshot": {
                "description": "Export complete list snapshot to JSON with all card details",
                "usage": "trello list-snapshot <list_id> [\"output_file.json\"]",
                "args": [
                    {"name": "list_id", "type": "string", "required": True},
                    {"name": "output_file", "type": "string", "required": False, "description": "Output JSON file (prints to stdout if not provided)"}
                ]
            },
            "sprint-audit": {
                "description": "Sprint-specific audit: validates sprint labels have due dates, detects overdue cards, checks label consistency",
                "usage": "trello sprint-audit <board_id> [\"sprint_label\"]",
                "args": [
                    {"name": "board_id", "type": "string", "required": True},
                    {"name": "sprint_label", "type": "string", "required": False, "description": "Filter by specific sprint label (e.g., 'Sprint 1'). Auto-detects if not provided."}
                ]
            },
            "rename-card": {
                "description": "Rename a card (update title/name)",
                "usage": "trello rename-card <card_id> \"new_title\"",
                "args": [
                    {"name": "card_id", "type": "string", "required": True},
                    {"name": "new_title", "type": "string", "required": True}
                ]
            },
            "label-audit": {
                "description": "Label audit: detect duplicates, similar names, unused labels, and naming inconsistencies",
                "usage": "trello label-audit <board_id>",
                "args": [
                    {"name": "board_id", "type": "string", "required": True}
                ]
            }
        },
        "usage_notes": [
            "Use 'trello help-json' to get command information in JSON format for programmatic use",
            "Use 'trello board-overview <board_id>' to see all lists and their card counts",
            "Use 'trello board-ids <board_id>' to get a quick reference of all IDs in a board",
            "Use 'trello search-cards <board_id> \"query\"' to find cards across all lists"
        ]
    }

    print(json.dumps(commands, indent=2))


def cmd_help():
    """Display help information in human-readable format"""
    help_text = """
Trello CLI - Command-line interface for Trello

DISCOVERY COMMANDS (useful for Claude Code):
  help-json                         Get all commands in JSON format
  board-overview <board_id>         Complete board overview with lists and counts
  board-ids <board_id>              Quick reference of all IDs in a board
  search-cards <board_id> "query"   Search cards across board

BOARD COMMANDS:
  boards                            List all boards
  create-board "name"               Create a new board

LIST COMMANDS:
  lists <board_id>                  List all lists in a board
  create-list <board_id> "name"     Create a new list
  archive-list <list_id>            Archive (close) a list

CARD COMMANDS:
  cards <list_id>                   List all cards in a list
  add-card <list_id> "title" ["desc"]   Add a new card
  show-card <card_id>               Show card details
  update-card <card_id> "desc"      Update card description
  rename-card <card_id> "title"     Rename card (update title)
  move-card <card_id> <list_id>     Move card to another list
  delete-card <card_id>             Delete a card permanently

CARD ENHANCEMENT COMMANDS:
  add-label <card_id> "color" ["name"]   Add label to card
  add-checklist <card_id> "name"         Add checklist to card
  add-checkitem <card_id> "checklist" "item"   Add item to checklist
  set-due <card_id> "YYYY-MM-DD"         Set due date
  add-comment <card_id> "comment"        Add comment to card

AUDIT & ANALYSIS COMMANDS:
  board-audit <board_id> ["pattern"]     Comprehensive board audit
  list-audit <list_id> ["pattern"]       Detailed list audit
  list-snapshot <list_id> ["file.json"]  Export list to JSON
  sprint-audit <board_id> ["sprint"]     Sprint audit (dates, overdue)
  label-audit <board_id>                 Label audit (duplicates, unused)

CONFIGURATION:
  config                            Configure API credentials

Valid label colors: yellow, purple, blue, red, green, orange, black, sky, pink, lime

Examples:
  trello help-json
  trello board-overview 68fcf05e481843db13204397
  trello board-ids 68fcf05e481843db13204397
  trello search-cards 68fcf05e481843db13204397 "feature"
  trello add-card 68fcff46fa7dbc9cc069eaef "PF-FEAT-001: New Feature"
"""
    print(help_text)
