"""
Card-related commands
"""

from ..client import get_client
from ..utils import format_table, format_card_details, validate_date


def cmd_cards(list_id):
    """List all cards in a list"""
    client = get_client()
    lst = client.get_list(list_id)
    cards = lst.list_cards()

    if not cards:
        print(f"No cards found in list {lst.name}")
        return

    format_table(
        cards,
        columns=[("ID", "id"), ("Name", "name")],
        widths={"ID": 25, "Name": 40}
    )


def cmd_add_card(list_id, title, description=""):
    """Add a new card to a list"""
    client = get_client()
    lst = client.get_list(list_id)
    card = lst.add_card(name=title, desc=description)

    print(f"✅ Card created: {card.name}")
    print(f"   ID: {card.id}")
    print(f"   List: {lst.name}")


def cmd_show_card(card_id):
    """Show detailed card information"""
    client = get_client()
    card = client.get_card(card_id)
    format_card_details(card)


def cmd_update_card(card_id, description):
    """Update card description"""
    client = get_client()
    card = client.get_card(card_id)
    card.set_description(description)

    print(f"✅ Updated description for: {card.name}")


def cmd_move_card(card_id, list_id):
    """Move card to another list"""
    client = get_client()
    card = client.get_card(card_id)
    target_list = client.get_list(list_id)

    card.change_list(list_id)
    print(f"✅ Moved card '{card.name}' to list '{target_list.name}'")


def cmd_add_checklist(card_id, checklist_name):
    """Add a checklist to a card"""
    client = get_client()
    card = client.get_card(card_id)
    checklist = card.add_checklist(checklist_name, [])

    print(f"✅ Checklist '{checklist_name}' added to card {card.name}")


def cmd_add_checkitem(card_id, checklist_name, item_name):
    """Add an item to a checklist"""
    client = get_client()
    card = client.get_card(card_id)

    # Find or create checklist
    checklist = None
    for cl in card.checklists:
        if cl.name == checklist_name:
            checklist = cl
            break

    if not checklist:
        print(f"ℹ️  Checklist '{checklist_name}' not found. Creating it...")
        checklist = card.add_checklist(checklist_name, [])

    checklist.add_checklist_item(item_name)
    print(f"✅ Added '{item_name}' to checklist '{checklist_name}'")


def cmd_set_due(card_id, due_date):
    """Set due date for a card"""
    client = get_client()
    card = client.get_card(card_id)

    dt = validate_date(due_date)
    card.set_due(dt)

    print(f"✅ Set due date to {dt.strftime('%Y-%m-%d %H:%M')} for card {card.name}")


def cmd_add_comment(card_id, comment):
    """Add a comment to a card"""
    client = get_client()
    card = client.get_card(card_id)
    card.comment(comment)

    print(f"✅ Added comment to card {card.name}")


def cmd_delete_card(card_id):
    """Delete a card permanently"""
    client = get_client()
    card = client.get_card(card_id)
    card_name = card.name

    card.delete()
    print(f"✅ Card deleted: {card_name}")


def cmd_rename_card(card_id, new_name):
    """Rename a card (update title)"""
    client = get_client()
    card = client.get_card(card_id)
    old_name = card.name

    card.set_name(new_name)
    print(f"✅ Card renamed:")
    print(f"   Old: {old_name}")
    print(f"   New: {new_name}")
    print(f"   ID:  {card_id}")
