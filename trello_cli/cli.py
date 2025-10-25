#!/usr/bin/env python3
"""
Trello CLI - Main command-line interface
"""

import sys
from . import __version__
from .config import configure_interactive
from .commands import (
    cmd_boards, cmd_create_board,
    cmd_lists, cmd_create_list,
    cmd_cards, cmd_add_card, cmd_show_card,
    cmd_update_card, cmd_move_card,
    cmd_add_checklist, cmd_add_checkitem,
    cmd_set_due, cmd_add_comment,
    cmd_add_label
)

HELP_TEXT = """
Trello CLI v{version} - Official Python command-line interface for Trello

Usage:
  trello <command> [arguments]

Configuration:
  config                      Configure API credentials

Board Commands:
  boards                      List all boards
  create-board "name"         Create a new board

List Commands:
  lists <board_id>            List all lists in a board
  create-list <board_id> "name"   Create a new list

Card Commands:
  cards <list_id>             List all cards in a list
  add-card <list_id> "title" ["description"]   Add a new card
  show-card <card_id>         Show card details
  update-card <card_id> "description"   Update card description
  move-card <card_id> <list_id>   Move card to another list

Label Commands:
  add-label <card_id> "color" "name"   Add label to card
    Valid colors: yellow, purple, blue, red, green, orange, black, sky, pink, lime

Checklist Commands:
  add-checklist <card_id> "name"   Add checklist to card
  add-checkitem <card_id> "checklist" "item"   Add item to checklist

Date & Comment Commands:
  set-due <card_id> "YYYY-MM-DD"   Set due date
  add-comment <card_id> "comment"   Add comment to card

Examples:
  trello boards
  trello lists 68fcf05e481843db13204397
  trello add-card 68fcff46fa7dbc9cc069eaef "PF-FEAT-001: New Feature" "Description here"
  trello add-label 68fd24640bf4 "red" "P0"
  trello set-due 68fd24640bf4 "2025-11-01"

For more information, see README.md
""".format(version=__version__)


def main():
    """Main CLI entry point"""
    if len(sys.argv) < 2:
        print(HELP_TEXT)
        sys.exit(1)

    command = sys.argv[1]

    try:
        if command == 'config':
            configure_interactive()

        elif command == 'boards':
            cmd_boards()

        elif command == 'create-board':
            if len(sys.argv) < 3:
                print("❌ Usage: trello create-board \"name\"")
                sys.exit(1)
            cmd_create_board(sys.argv[2])

        elif command == 'lists':
            if len(sys.argv) < 3:
                print("❌ Usage: trello lists <board_id>")
                sys.exit(1)
            cmd_lists(sys.argv[2])

        elif command == 'create-list':
            if len(sys.argv) < 4:
                print("❌ Usage: trello create-list <board_id> \"name\"")
                sys.exit(1)
            cmd_create_list(sys.argv[2], sys.argv[3])

        elif command == 'cards':
            if len(sys.argv) < 3:
                print("❌ Usage: trello cards <list_id>")
                sys.exit(1)
            cmd_cards(sys.argv[2])

        elif command == 'add-card':
            if len(sys.argv) < 4:
                print("❌ Usage: trello add-card <list_id> \"title\" [\"description\"]")
                sys.exit(1)
            description = sys.argv[4] if len(sys.argv) > 4 else ""
            cmd_add_card(sys.argv[2], sys.argv[3], description)

        elif command == 'show-card':
            if len(sys.argv) < 3:
                print("❌ Usage: trello show-card <card_id>")
                sys.exit(1)
            cmd_show_card(sys.argv[2])

        elif command == 'update-card':
            if len(sys.argv) < 4:
                print("❌ Usage: trello update-card <card_id> \"description\"")
                sys.exit(1)
            cmd_update_card(sys.argv[2], sys.argv[3])

        elif command == 'move-card':
            if len(sys.argv) < 4:
                print("❌ Usage: trello move-card <card_id> <list_id>")
                sys.exit(1)
            cmd_move_card(sys.argv[2], sys.argv[3])

        elif command == 'add-label':
            if len(sys.argv) < 4:
                print("❌ Usage: trello add-label <card_id> \"color\" [\"name\"]")
                sys.exit(1)
            label_name = sys.argv[4] if len(sys.argv) > 4 else ""
            cmd_add_label(sys.argv[2], sys.argv[3], label_name)

        elif command == 'add-checklist':
            if len(sys.argv) < 4:
                print("❌ Usage: trello add-checklist <card_id> \"name\"")
                sys.exit(1)
            cmd_add_checklist(sys.argv[2], sys.argv[3])

        elif command == 'add-checkitem':
            if len(sys.argv) < 5:
                print("❌ Usage: trello add-checkitem <card_id> \"checklist\" \"item\"")
                sys.exit(1)
            cmd_add_checkitem(sys.argv[2], sys.argv[3], sys.argv[4])

        elif command == 'set-due':
            if len(sys.argv) < 4:
                print("❌ Usage: trello set-due <card_id> \"YYYY-MM-DD\"")
                sys.exit(1)
            cmd_set_due(sys.argv[2], sys.argv[3])

        elif command == 'add-comment':
            if len(sys.argv) < 4:
                print("❌ Usage: trello add-comment <card_id> \"comment\"")
                sys.exit(1)
            cmd_add_comment(sys.argv[2], sys.argv[3])

        elif command in ['-h', '--help', 'help']:
            print(HELP_TEXT)

        elif command in ['-v', '--version', 'version']:
            print(f"Trello CLI v{__version__}")

        else:
            print(f"❌ Unknown command: {command}")
            print()
            print(HELP_TEXT)
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n⚠️  Operation cancelled by user")
        sys.exit(130)
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()
