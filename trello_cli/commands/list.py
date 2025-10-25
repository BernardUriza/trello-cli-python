"""
List-related commands
"""

from ..client import get_client
from ..utils import format_table


def cmd_lists(board_id):
    """List all lists in a board"""
    client = get_client()
    board = client.get_board(board_id)
    lists = board.list_lists()

    if not lists:
        print(f"No lists found in board {board.name}")
        return

    format_table(
        lists,
        columns=[("ID", "id"), ("Name", "name")],
        widths={"ID": 25, "Name": 40}
    )


def cmd_create_list(board_id, list_name):
    """Create a new list in a board"""
    client = get_client()
    board = client.get_board(board_id)
    new_list = board.add_list(list_name)

    print(f"✅ List created: {new_list.name}")
    print(f"   ID: {new_list.id}")
    print(f"   Board: {board.name}")
