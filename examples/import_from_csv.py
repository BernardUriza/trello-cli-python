#!/usr/bin/env python3
"""
Example: Import cards from CSV file

This script demonstrates how to use the trello-cli library
programmatically to import cards from a CSV file.
"""

import csv
import sys
import os

# Add parent directory to import trello_cli
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from trello_cli.client import get_client


def import_cards_from_csv(csv_path, list_id):
    """
    Import cards from CSV file

    CSV format:
    Title,Description,Labels,Priority

    Args:
        csv_path: Path to CSV file
        list_id: Trello list ID to add cards to
    """
    client = get_client()
    target_list = client.get_list(list_id)

    print(f"📋 Importing cards to list: {target_list.name}")
    print()

    cards_created = 0

    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)

        for row in reader:
            title = row.get('Title', '')
            description = row.get('Description', '')
            labels_str = row.get('Labels', '')
            priority = row.get('Priority', '')

            if not title:
                continue

            # Create card
            card = target_list.add_card(name=title, desc=description)
            print(f"✅ Created: {title}")

            # Add labels if specified
            if labels_str:
                labels = [l.strip() for l in labels_str.split(',')]
                board = card.board

                for label_name in labels:
                    # Try to find existing label
                    label_obj = None
                    for l in board.get_labels():
                        if l.name == label_name:
                            label_obj = l
                            break

                    # Create if not found (default to blue)
                    if not label_obj:
                        label_obj = board.add_label(label_name, 'blue')

                    card.add_label(label_obj)
                    print(f"   🏷️  Added label: {label_name}")

            cards_created += 1

    print()
    print(f"🎉 Import complete! Created {cards_created} cards.")


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python3 import_from_csv.py <csv_file> <list_id>")
        sys.exit(1)

    csv_file = sys.argv[1]
    list_id = sys.argv[2]

    import_cards_from_csv(csv_file, list_id)
