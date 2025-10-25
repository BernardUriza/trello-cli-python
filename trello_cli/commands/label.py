"""
Label-related commands
"""

from ..client import get_client
from ..utils import validate_color


def cmd_add_label(card_id, color, name=""):
    """Add a label to a card"""
    client = get_client()
    card = client.get_card(card_id)

    # Validate color
    validate_color(color)

    # Get board and find or create label
    board = card.board
    label = None

    for l in board.get_labels():
        if l.name == name and l.color == color:
            label = l
            break

    if not label:
        label = board.add_label(name, color)

    card.add_label(label)
    print(f"✅ Label '{name}' ({color}) added to card {card.name}")
