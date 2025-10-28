"""
Audit commands for board and list analysis
"""

import json
import re
from datetime import datetime, timedelta
from collections import defaultdict, Counter
from ..client import get_client


def cmd_board_audit(board_id, pattern=None):
    """
    Comprehensive board audit:
    - Cards without proper ID naming pattern
    - Cards without members assigned
    - Empty lists
    - Stale lists (no activity in 30+ days)
    - Cards in Done that could be deleted
    - Cards without labels
    - Cards without descriptions
    """
    client = get_client()
    board = client.get_board(board_id)
    lists = board.list_lists()

    print(f"\n{'='*80}")
    print(f"BOARD AUDIT REPORT - {board.name}")
    print(f"Board ID: {board_id}")
    print(f"{'='*80}\n")

    # Compile pattern if provided
    id_pattern = re.compile(pattern) if pattern else None

    # Initialize issue trackers
    cards_without_pattern = []
    cards_without_members = []
    cards_without_labels = []
    cards_without_description = []
    empty_lists = []
    stale_lists = []
    done_cards_to_delete = []

    total_cards = 0
    total_active_lists = 0

    for lst in lists:
        if lst.closed:
            continue

        total_active_lists += 1
        cards = lst.list_cards()

        # Check for empty lists
        if len(cards) == 0:
            empty_lists.append(lst.name)
            continue

        total_cards += len(cards)

        # Check if list is stale (no cards created in last 30 days)
        is_stale = True
        newest_card_age = None

        for card in cards:
            try:
                timestamp = int(card.id[:8], 16)
                created_date = datetime.fromtimestamp(timestamp)
                age_days = (datetime.now() - created_date).days

                if newest_card_age is None or age_days < newest_card_age:
                    newest_card_age = age_days

                if age_days < 30:
                    is_stale = False
            except:
                pass

        if is_stale and newest_card_age and 'done' not in lst.name.lower():
            stale_lists.append((lst.name, newest_card_age))

        # Check cards in Done lists for deletion candidates
        is_done_list = any(keyword in lst.name.lower() for keyword in ['done', 'completed', 'finished', 'closed'])

        for card in cards:
            # Check ID pattern
            if id_pattern and not id_pattern.search(card.name):
                cards_without_pattern.append((card.name, card.id, lst.name))

            # Check for assigned members
            if not card.member_id and not hasattr(card, 'idMembers'):
                cards_without_members.append((card.name, card.id, lst.name))

            # Check for labels
            if not card.labels or len(card.labels) == 0:
                cards_without_labels.append((card.name, card.id, lst.name))

            # Check for description
            if not card.desc or card.desc.strip() == "":
                cards_without_description.append((card.name, card.id, lst.name))

            # Cards in Done to consider for deletion
            if is_done_list:
                try:
                    timestamp = int(card.id[:8], 16)
                    created_date = datetime.fromtimestamp(timestamp)
                    age_days = (datetime.now() - created_date).days

                    # Cards completed more than 7 days ago
                    if age_days > 7:
                        done_cards_to_delete.append((card.name, card.id, lst.name, age_days))
                except:
                    pass

    # Calculate audit score
    issues_found = 0
    max_issues = 6

    # Print summary
    print(f"📊 BOARD SUMMARY:")
    print(f"   Total Active Lists: {total_active_lists}")
    print(f"   Total Cards: {total_cards}")
    print(f"   Empty Lists: {len(empty_lists)}")
    print(f"   Stale Lists: {len(stale_lists)}")
    print()

    # Print issues
    print(f"{'='*80}")
    print(f"AUDIT FINDINGS:")
    print(f"{'='*80}\n")

    # ID Pattern violations
    if id_pattern:
        if cards_without_pattern:
            issues_found += 1
            print(f"⚠️  NAMING PATTERN VIOLATIONS: {len(cards_without_pattern)} card(s)")
            print(f"   Pattern: {pattern}")
            for card_name, card_id, list_name in cards_without_pattern[:10]:
                print(f"   • {card_name[:50]}")
                print(f"     ID: {card_id} | List: {list_name}")
            if len(cards_without_pattern) > 10:
                print(f"   ... and {len(cards_without_pattern) - 10} more")
            print()
        else:
            print(f"✅ All cards follow naming pattern: {pattern}\n")

    # Cards without members
    if cards_without_members:
        issues_found += 1
        print(f"⚠️  CARDS WITHOUT ASSIGNED MEMBERS: {len(cards_without_members)} card(s)")
        for card_name, card_id, list_name in cards_without_members[:10]:
            print(f"   • {card_name[:50]}")
            print(f"     ID: {card_id} | List: {list_name}")
        if len(cards_without_members) > 10:
            print(f"   ... and {len(cards_without_members) - 10} more")
        print()
    else:
        print(f"✅ All cards have assigned members\n")

    # Cards without labels
    if cards_without_labels:
        issues_found += 1
        print(f"⚠️  CARDS WITHOUT LABELS: {len(cards_without_labels)} card(s)")
        for card_name, card_id, list_name in cards_without_labels[:10]:
            print(f"   • {card_name[:50]}")
            print(f"     ID: {card_id} | List: {list_name}")
        if len(cards_without_labels) > 10:
            print(f"   ... and {len(cards_without_labels) - 10} more")
        print()
    else:
        print(f"✅ All cards have labels\n")

    # Cards without description
    if cards_without_description:
        issues_found += 1
        print(f"⚠️  CARDS WITHOUT DESCRIPTION: {len(cards_without_description)} card(s)")
        for card_name, card_id, list_name in cards_without_description[:10]:
            print(f"   • {card_name[:50]}")
            print(f"     ID: {card_id} | List: {list_name}")
        if len(cards_without_description) > 10:
            print(f"   ... and {len(cards_without_description) - 10} more")
        print()
    else:
        print(f"✅ All cards have descriptions\n")

    # Empty lists
    if empty_lists:
        issues_found += 1
        print(f"📭 EMPTY LISTS: {len(empty_lists)} list(s)")
        for list_name in empty_lists:
            print(f"   • {list_name}")
        print()
    else:
        print(f"✅ No empty lists\n")

    # Stale lists
    if stale_lists:
        issues_found += 1
        print(f"⏰ STALE LISTS: {len(stale_lists)} list(s) with no activity in 30+ days")
        for list_name, age in sorted(stale_lists, key=lambda x: x[1], reverse=True):
            print(f"   • {list_name}: {age} days since last card")
        print()
    else:
        print(f"✅ All lists have recent activity\n")

    # Deletion candidates
    print(f"{'='*80}")
    print(f"MAINTENANCE RECOMMENDATIONS:")
    print(f"{'='*80}\n")

    if done_cards_to_delete:
        print(f"🗑️  CARDS READY FOR DELETION: {len(done_cards_to_delete)} card(s) in Done lists")
        print(f"   (Completed more than 7 days ago)\n")

        # Group by list
        by_list = defaultdict(list)
        for card_name, card_id, list_name, age in done_cards_to_delete:
            by_list[list_name].append((card_name, card_id, age))

        for list_name in sorted(by_list.keys()):
            cards = by_list[list_name]
            print(f"   📋 {list_name} ({len(cards)} card(s)):")
            for card_name, card_id, age in sorted(cards, key=lambda x: x[2], reverse=True)[:10]:
                print(f"      • {card_name[:50]}")
                print(f"        ID: {card_id} | Age: {age} days")
                print(f"        Delete command: trello delete-card {card_id}")
            if len(cards) > 10:
                print(f"      ... and {len(cards) - 10} more")
            print()
    else:
        print(f"✅ No old cards in Done lists\n")

    # Audit score
    print(f"{'='*80}")
    audit_score = max(0, 100 - (issues_found * 15))

    if audit_score >= 90:
        status = "🟢 EXCELLENT"
    elif audit_score >= 70:
        status = "🟡 GOOD"
    elif audit_score >= 50:
        status = "🟠 NEEDS ATTENTION"
    else:
        status = "🔴 CRITICAL"

    print(f"Audit Score: {audit_score}/100 - {status}")
    print(f"Issues Found: {issues_found}")
    print(f"{'='*80}\n")


def cmd_list_snapshot(list_id, output_file=None):
    """
    Export complete snapshot of a list to JSON.
    Includes all card details: ID, name, description, labels, members, checklists, etc.
    """
    client = get_client()
    lst = client.get_list(list_id)
    cards = lst.list_cards()

    snapshot = {
        "list_id": lst.id,
        "list_name": lst.name,
        "exported_at": datetime.now().isoformat(),
        "card_count": len(cards),
        "cards": []
    }

    for card in cards:
        # Extract card age
        try:
            timestamp = int(card.id[:8], 16)
            created_date = datetime.fromtimestamp(timestamp)
            age_days = (datetime.now() - created_date).days
        except:
            created_date = None
            age_days = None

        # Extract labels
        labels = []
        for label in card.labels:
            labels.append({
                "name": label.name,
                "color": label.color
            })

        # Extract checklists
        checklists = []
        for checklist in card.checklists:
            items = []
            for item in checklist.items:
                items.append({
                    "name": item.get('name', ''),
                    "checked": item.get('state', 'incomplete') == 'complete'
                })

            checklists.append({
                "name": checklist.name,
                "items": items,
                "completed": sum(1 for item in items if item['checked']),
                "total": len(items)
            })

        # Extract due date
        due_date = None
        if card.due:
            try:
                if isinstance(card.due, str):
                    due_date = card.due
                else:
                    due_date = card.due.isoformat()
            except:
                pass

        card_data = {
            "id": card.id,
            "name": card.name,
            "description": card.desc or "",
            "url": card.url,
            "labels": labels,
            "due_date": due_date,
            "created_date": created_date.isoformat() if created_date else None,
            "age_days": age_days,
            "checklists": checklists,
            "checklist_summary": {
                "total_checklists": len(checklists),
                "total_items": sum(cl['total'] for cl in checklists),
                "completed_items": sum(cl['completed'] for cl in checklists)
            },
            "has_description": bool(card.desc and card.desc.strip()),
            "has_labels": len(labels) > 0,
            "has_due_date": due_date is not None
        }

        snapshot["cards"].append(card_data)

    # Output
    json_output = json.dumps(snapshot, indent=2, ensure_ascii=False)

    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(json_output)
        print(f"✅ List snapshot exported to: {output_file}")
        print(f"   List: {lst.name}")
        print(f"   Cards: {len(cards)}")
    else:
        print(json_output)


def cmd_list_audit(list_id, pattern=None):
    """
    Detailed audit of a specific list.
    Similar to board audit but focused on a single list.
    """
    client = get_client()
    lst = client.get_list(list_id)
    cards = lst.list_cards()

    print(f"\n{'='*80}")
    print(f"LIST AUDIT REPORT - {lst.name}")
    print(f"List ID: {list_id}")
    print(f"{'='*80}\n")

    if not cards:
        print("📭 This list is empty")
        return

    # Compile pattern if provided
    id_pattern = re.compile(pattern) if pattern else None

    # Initialize trackers
    cards_without_pattern = []
    cards_without_members = []
    cards_without_labels = []
    cards_without_description = []
    cards_with_due = 0
    cards_overdue = 0

    # Age statistics
    ages = []

    for card in cards:
        # Check age
        try:
            timestamp = int(card.id[:8], 16)
            created_date = datetime.fromtimestamp(timestamp)
            age_days = (datetime.now() - created_date).days
            ages.append(age_days)
        except:
            pass

        # Check ID pattern
        if id_pattern and not id_pattern.search(card.name):
            cards_without_pattern.append((card.name, card.id))

        # Check for assigned members
        if not card.member_id and not hasattr(card, 'idMembers'):
            cards_without_members.append((card.name, card.id))

        # Check for labels
        if not card.labels or len(card.labels) == 0:
            cards_without_labels.append((card.name, card.id))

        # Check for description
        if not card.desc or card.desc.strip() == "":
            cards_without_description.append((card.name, card.id))

        # Check due dates
        if card.due:
            cards_with_due += 1
            try:
                if isinstance(card.due, str):
                    due_date = datetime.fromisoformat(card.due.replace('Z', '+00:00'))
                else:
                    due_date = card.due

                if due_date < datetime.now():
                    cards_overdue += 1
            except:
                pass

    # Print summary
    print(f"📊 LIST SUMMARY:")
    print(f"   Total Cards: {len(cards)}")
    print(f"   Cards with due dates: {cards_with_due}")
    print(f"   Overdue cards: {cards_overdue}")

    if ages:
        print(f"\n⏱️  AGE STATISTICS:")
        print(f"   Average age: {sum(ages) / len(ages):.1f} days")
        print(f"   Oldest card: {max(ages)} days")
        print(f"   Newest card: {min(ages)} days")

    print()

    # Print issues
    print(f"{'='*80}")
    print(f"AUDIT FINDINGS:")
    print(f"{'='*80}\n")

    issues = 0

    # Pattern violations
    if id_pattern:
        if cards_without_pattern:
            issues += 1
            print(f"⚠️  NAMING PATTERN VIOLATIONS: {len(cards_without_pattern)} card(s)")
            print(f"   Pattern: {pattern}")
            for card_name, card_id in cards_without_pattern[:10]:
                print(f"   • {card_name[:60]}")
                print(f"     ID: {card_id}")
            if len(cards_without_pattern) > 10:
                print(f"   ... and {len(cards_without_pattern) - 10} more")
            print()

    # Missing members
    if cards_without_members:
        issues += 1
        print(f"⚠️  CARDS WITHOUT ASSIGNED MEMBERS: {len(cards_without_members)} card(s)")
        for card_name, card_id in cards_without_members[:10]:
            print(f"   • {card_name[:60]}")
            print(f"     ID: {card_id}")
        if len(cards_without_members) > 10:
            print(f"   ... and {len(cards_without_members) - 10} more")
        print()

    # Missing labels
    if cards_without_labels:
        issues += 1
        print(f"⚠️  CARDS WITHOUT LABELS: {len(cards_without_labels)} card(s)")
        for card_name, card_id in cards_without_labels[:10]:
            print(f"   • {card_name[:60]}")
            print(f"     ID: {card_id}")
        if len(cards_without_labels) > 10:
            print(f"   ... and {len(cards_without_labels) - 10} more")
        print()

    # Missing descriptions
    if cards_without_description:
        issues += 1
        print(f"⚠️  CARDS WITHOUT DESCRIPTION: {len(cards_without_description)} card(s)")
        for card_name, card_id in cards_without_description[:10]:
            print(f"   • {card_name[:60]}")
            print(f"     ID: {card_id}")
        if len(cards_without_description) > 10:
            print(f"   ... and {len(cards_without_description) - 10} more")
        print()

    if issues == 0:
        print("✅ No issues found! This list is well maintained.\n")

    # Score
    print(f"{'='*80}")
    audit_score = max(0, 100 - (issues * 20))

    if audit_score >= 90:
        status = "🟢 EXCELLENT"
    elif audit_score >= 70:
        status = "🟡 GOOD"
    elif audit_score >= 50:
        status = "🟠 NEEDS ATTENTION"
    else:
        status = "🔴 CRITICAL"

    print(f"List Audit Score: {audit_score}/100 - {status}")
    print(f"Issues Found: {issues}")
    print(f"{'='*80}\n")
