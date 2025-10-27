"""
Bulk operations commands for batch processing
"""

import json
import csv
from ..client import get_client
from ..utils import validate_date


def cmd_bulk_move_cards(source_list_id, target_list_id, filter_query=""):
    """
    Move multiple cards from one list to another.
    Optionally filter by query string.
    """
    client = get_client()
    source_list = client.get_list(source_list_id)
    target_list = client.get_list(target_list_id)
    cards = source_list.list_cards()

    if not cards:
        print(f"No cards found in list '{source_list.name}'")
        return

    # Filter cards if query provided
    if filter_query:
        query_lower = filter_query.lower()
        cards = [c for c in cards if query_lower in c.name.lower() or
                 (c.desc and query_lower in c.desc.lower())]

    if not cards:
        print(f"No cards matching '{filter_query}' found")
        return

    print(f"\n{'='*70}")
    print(f"BULK MOVE: {len(cards)} card(s)")
    print(f"FROM: {source_list.name}")
    print(f"TO:   {target_list.name}")
    print(f"{'='*70}\n")

    moved_count = 0
    for card in cards:
        try:
            card.change_list(target_list_id)
            print(f"✅ Moved: {card.name[:60]}")
            moved_count += 1
        except Exception as e:
            print(f"❌ Failed to move '{card.name[:60]}': {str(e)}")

    print(f"\n{'='*70}")
    print(f"✅ Successfully moved {moved_count}/{len(cards)} cards")
    print(f"{'='*70}\n")


def cmd_bulk_add_label(card_ids_file, label_color, label_name=""):
    """
    Add label to multiple cards.
    card_ids_file: File with one card ID per line
    """
    client = get_client()

    # Read card IDs from file
    try:
        with open(card_ids_file, 'r') as f:
            card_ids = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"❌ File not found: {card_ids_file}")
        return

    if not card_ids:
        print(f"❌ No card IDs found in file")
        return

    print(f"\n{'='*70}")
    print(f"BULK ADD LABEL: {len(card_ids)} card(s)")
    print(f"Label: {label_name} ({label_color})")
    print(f"{'='*70}\n")

    success_count = 0
    for card_id in card_ids:
        try:
            card = client.get_card(card_id)
            board = client.get_board(card.board_id)

            # Find or create label
            label = None
            for l in board.get_labels():
                if l.color == label_color and (not label_name or l.name == label_name):
                    label = l
                    break

            if not label:
                label = board.add_label(label_name, label_color)

            card.add_label(label)
            print(f"✅ Added label to: {card.name[:50]}")
            success_count += 1
        except Exception as e:
            print(f"❌ Failed for card {card_id}: {str(e)}")

    print(f"\n{'='*70}")
    print(f"✅ Successfully labeled {success_count}/{len(card_ids)} cards")
    print(f"{'='*70}\n")


def cmd_bulk_set_due(card_ids_file, due_date):
    """
    Set due date for multiple cards.
    card_ids_file: File with one card ID per line
    due_date: Date in YYYY-MM-DD format
    """
    client = get_client()
    dt = validate_date(due_date)

    # Read card IDs from file
    try:
        with open(card_ids_file, 'r') as f:
            card_ids = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"❌ File not found: {card_ids_file}")
        return

    if not card_ids:
        print(f"❌ No card IDs found in file")
        return

    print(f"\n{'='*70}")
    print(f"BULK SET DUE DATE: {len(card_ids)} card(s)")
    print(f"Due Date: {dt.strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*70}\n")

    success_count = 0
    for card_id in card_ids:
        try:
            card = client.get_card(card_id)
            card.set_due(dt)
            print(f"✅ Set due date for: {card.name[:50]}")
            success_count += 1
        except Exception as e:
            print(f"❌ Failed for card {card_id}: {str(e)}")

    print(f"\n{'='*70}")
    print(f"✅ Successfully set due date for {success_count}/{len(card_ids)} cards")
    print(f"{'='*70}\n")


def cmd_bulk_archive_cards(list_id, filter_query=""):
    """
    Archive multiple cards in a list.
    Optionally filter by query string.
    """
    client = get_client()
    lst = client.get_list(list_id)
    cards = lst.list_cards()

    if not cards:
        print(f"No cards found in list '{lst.name}'")
        return

    # Filter cards if query provided
    if filter_query:
        query_lower = filter_query.lower()
        cards = [c for c in cards if query_lower in c.name.lower() or
                 (c.desc and query_lower in c.desc.lower())]

    if not cards:
        print(f"No cards matching '{filter_query}' found")
        return

    print(f"\n{'='*70}")
    print(f"BULK ARCHIVE: {len(cards)} card(s) from '{lst.name}'")
    print(f"{'='*70}\n")

    for card in cards:
        print(f"  • {card.name[:60]}")

    confirm = input(f"\n⚠️  Archive these {len(cards)} cards? (yes/no): ")
    if confirm.lower() != 'yes':
        print("❌ Operation cancelled")
        return

    archived_count = 0
    for card in cards:
        try:
            card.set_closed(True)
            print(f"✅ Archived: {card.name[:60]}")
            archived_count += 1
        except Exception as e:
            print(f"❌ Failed to archive '{card.name[:60]}': {str(e)}")

    print(f"\n{'='*70}")
    print(f"✅ Successfully archived {archived_count}/{len(cards)} cards")
    print(f"{'='*70}\n")


def cmd_bulk_create_cards(list_id, input_file):
    """
    Create multiple cards from CSV or JSON file.

    CSV format: title,description,due_date,labels
    JSON format: [{"title": "...", "description": "...", "due_date": "...", "labels": ["color:name", ...]}, ...]
    """
    client = get_client()
    lst = client.get_list(list_id)

    # Determine file type
    if input_file.endswith('.json'):
        cards_data = _read_json_file(input_file)
    elif input_file.endswith('.csv'):
        cards_data = _read_csv_file(input_file)
    else:
        print("❌ Unsupported file format. Use .csv or .json")
        return

    if not cards_data:
        print("❌ No card data found in file")
        return

    print(f"\n{'='*70}")
    print(f"BULK CREATE: {len(cards_data)} card(s) in '{lst.name}'")
    print(f"{'='*70}\n")

    created_count = 0
    for card_data in cards_data:
        try:
            title = card_data.get('title', '')
            description = card_data.get('description', '')
            due_date = card_data.get('due_date', '')
            labels = card_data.get('labels', [])

            if not title:
                print(f"⚠️  Skipping card with no title")
                continue

            # Create card
            card = lst.add_card(name=title, desc=description)

            # Set due date if provided
            if due_date:
                try:
                    dt = validate_date(due_date)
                    card.set_due(dt)
                except:
                    print(f"⚠️  Invalid due date for '{title[:40]}': {due_date}")

            # Add labels if provided
            if labels:
                board = client.get_board(card.board_id)
                for label_spec in labels:
                    try:
                        if ':' in label_spec:
                            color, name = label_spec.split(':', 1)
                        else:
                            color, name = label_spec, ""

                        # Find or create label
                        label = None
                        for l in board.get_labels():
                            if l.color == color and (not name or l.name == name):
                                label = l
                                break

                        if not label:
                            label = board.add_label(name, color)

                        card.add_label(label)
                    except Exception as e:
                        print(f"⚠️  Failed to add label '{label_spec}' to '{title[:40]}': {str(e)}")

            print(f"✅ Created: {title[:60]}")
            created_count += 1
        except Exception as e:
            print(f"❌ Failed to create card: {str(e)}")

    print(f"\n{'='*70}")
    print(f"✅ Successfully created {created_count}/{len(cards_data)} cards")
    print(f"{'='*70}\n")


def _read_json_file(filepath):
    """Read cards data from JSON file"""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error reading JSON file: {str(e)}")
        return []


def _read_csv_file(filepath):
    """Read cards data from CSV file"""
    try:
        cards = []
        with open(filepath, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                card_data = {
                    'title': row.get('title', ''),
                    'description': row.get('description', ''),
                    'due_date': row.get('due_date', ''),
                    'labels': row.get('labels', '').split(',') if row.get('labels') else []
                }
                cards.append(card_data)
        return cards
    except Exception as e:
        print(f"❌ Error reading CSV file: {str(e)}")
        return []
