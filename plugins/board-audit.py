#!/usr/bin/env python3
# trello-plugin
# name: Board Audit (Official Plugin)
# description: Comprehensive board audit - exposes structural chaos and workflow inconsistencies
# usage: plugin run board-audit <board_id> [--json] [--pattern "REGEX"]
# author: Trello CLI Team
# version: 1.0.0
# tags: audit, core-mirror, validation, advanced, production-ready

"""
Board Audit Plugin - Official Reference Implementation

This plugin demonstrates how to implement complex CLI logic externally using
the Trello CLI plugin system. It mirrors the core board-audit command and
serves as a reference for building production-ready plugins.

WHAT IT VALIDATES:
==================
🔴 CRITICAL (Workflow Killers):
  1. Cards in "Done" without due dates → No traceability, can't measure velocity
  2. Cards in "Done" with incomplete checklists → False sense of completion
  3. Overdue cards not marked complete → Zombie tasks killing sprint health

🟠 HIGH PRIORITY (Execution Blockers):
  4. Active cards without due dates → No accountability, no planning possible
  5. Execution cards without assigned members → Orphaned work nobody owns

🟡 MEDIUM PRIORITY (Quality Issues):
  6. Empty checklists → Fake productivity signals
  7. Pattern violations → Inconsistent nomenclature
  8. Missing descriptions in critical lists → Team guessing requirements

USAGE:
======
  Basic audit:
    trello plugin run board-audit <board_id>

  JSON output (for CI/CD):
    trello plugin run board-audit <board_id> --json

  With naming pattern validation:
    trello plugin run board-audit <board_id> --pattern "PF-[A-Z]+-\\d+"

ENVIRONMENT VARIABLES:
======================
  TRELLO_API_KEY       - Your Trello API key (required)
  TRELLO_TOKEN         - Your Trello API token (required)
  TRELLO_BASE_URL      - Trello API base URL (optional)

HEALTH SCORE:
=============
  90-100: 🟢 EXCELLENT - Board ready for production
  70-89:  🟡 GOOD - Minor issues, generally healthy
  50-69:  🟠 NEEDS ATTENTION - Significant workflow problems
  0-49:   🔴 CRITICAL - Severe structural problems affecting delivery
"""

import os
import sys
import json
import re
from datetime import datetime
from collections import defaultdict

try:
    import requests
except ImportError:
    print("❌ Error: 'requests' library not installed", file=sys.stderr)
    print("   Install it with: pip install requests", file=sys.stderr)
    sys.exit(1)


class TrelloClient:
    """Simple Trello API client for plugin use"""

    def __init__(self, api_key, token, base_url='https://api.trello.com/1'):
        self.api_key = api_key
        self.token = token
        self.base_url = base_url
        self.session = requests.Session()

    def _request(self, method, endpoint, params=None, data=None):
        """Make authenticated request to Trello API"""
        url = f"{self.base_url}{endpoint}"
        params = params or {}
        params.update({'key': self.api_key, 'token': self.token})

        try:
            response = self.session.request(method, url, params=params, json=data, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ API Error: {e}", file=sys.stderr)
            sys.exit(1)

    def get_board(self, board_id):
        """Get board information"""
        return self._request('GET', f'/boards/{board_id}')

    def get_lists(self, board_id):
        """Get all lists in a board"""
        return self._request('GET', f'/boards/{board_id}/lists', params={'filter': 'open'})

    def get_cards(self, list_id):
        """Get all cards in a list"""
        return self._request('GET', f'/lists/{list_id}/cards', params={
            'fields': 'id,name,desc,due,idMembers,labels',
            'checklists': 'all'
        })


class BoardAuditor:
    """Board audit logic"""

    # List classification keywords
    DONE_KEYWORDS = ['done', 'completed', 'finished', 'closed', 'archive']
    ACTIVE_KEYWORDS = ['sprint', 'doing', 'in progress', 'testing', 'ready', 'wip', 'development']
    EXECUTION_KEYWORDS = ['sprint', 'doing', 'in progress', 'testing', 'development']
    CRITICAL_KEYWORDS = ['sprint', 'testing', 'in progress', 'doing', 'review']

    def __init__(self, client, board_id, pattern=None):
        self.client = client
        self.board_id = board_id
        self.pattern = re.compile(pattern) if pattern else None

        # Issue trackers
        self.done_cards_no_due = []
        self.done_cards_incomplete_checklist = []
        self.active_cards_no_due = []
        self.overdue_not_complete = []
        self.execution_cards_no_members = []
        self.empty_checklists = []
        self.cards_without_pattern = []
        self.cards_without_description_critical = []

        self.total_cards = 0
        self.total_lists = 0

    def run_audit(self):
        """Execute full board audit"""
        # Get board info
        board = self.client.get_board(self.board_id)
        self.board_name = board['name']

        # Get all lists
        lists = self.client.get_lists(self.board_id)
        self.total_lists = len(lists)

        # Audit each list
        for lst in lists:
            self._audit_list(lst)

        return self._calculate_results()

    def _audit_list(self, lst):
        """Audit a single list"""
        list_name = lst['name']
        list_name_lower = list_name.lower()

        # Classify list
        is_done = any(kw in list_name_lower for kw in self.DONE_KEYWORDS)
        is_active = any(kw in list_name_lower for kw in self.ACTIVE_KEYWORDS)
        is_execution = any(kw in list_name_lower for kw in self.EXECUTION_KEYWORDS)
        is_critical = any(kw in list_name_lower for kw in self.CRITICAL_KEYWORDS)

        # Get cards
        cards = self.client.get_cards(lst['id'])
        self.total_cards += len(cards)

        # Audit each card
        for card in cards:
            self._audit_card(card, list_name, is_done, is_active, is_execution, is_critical)

    def _audit_card(self, card, list_name, is_done, is_active, is_execution, is_critical):
        """Audit a single card"""
        # Parse due date
        due_date = None
        is_overdue = False
        days_overdue = 0

        if card.get('due'):
            try:
                due_date = datetime.fromisoformat(card['due'].replace('Z', '+00:00'))
                if due_date < datetime.now():
                    is_overdue = True
                    days_overdue = (datetime.now() - due_date).days
            except:
                pass

        # Check checklists
        has_checklist = 'checklists' in card and len(card.get('checklists', [])) > 0
        checklist_complete = True
        checklist_empty = False
        total_items = 0
        completed_items = 0

        if has_checklist:
            for checklist in card.get('checklists', []):
                items = checklist.get('checkItems', [])
                if len(items) == 0:
                    checklist_empty = True

                for item in items:
                    total_items += 1
                    if item.get('state') == 'complete':
                        completed_items += 1

            if total_items > 0 and completed_items < total_items:
                checklist_complete = False

        # Check members
        has_members = len(card.get('idMembers', [])) > 0

        # VALIDATION 1: Done without due date
        if is_done and not card.get('due'):
            self.done_cards_no_due.append({
                'name': card['name'],
                'id': card['id'],
                'list': list_name
            })

        # VALIDATION 2: Done with incomplete checklists
        if is_done and has_checklist and not checklist_complete:
            self.done_cards_incomplete_checklist.append({
                'name': card['name'],
                'id': card['id'],
                'list': list_name,
                'total': total_items,
                'completed': completed_items
            })

        # VALIDATION 3: Active cards without due dates
        if is_active and not card.get('due'):
            self.active_cards_no_due.append({
                'name': card['name'],
                'id': card['id'],
                'list': list_name
            })

        # VALIDATION 4: Overdue not complete
        if is_overdue and not is_done:
            self.overdue_not_complete.append({
                'name': card['name'],
                'id': card['id'],
                'list': list_name,
                'due_date': due_date,
                'days_overdue': days_overdue
            })

        # VALIDATION 5: Execution without members
        if is_execution and not has_members:
            self.execution_cards_no_members.append({
                'name': card['name'],
                'id': card['id'],
                'list': list_name
            })

        # VALIDATION 6: Empty checklists
        if checklist_empty:
            self.empty_checklists.append({
                'name': card['name'],
                'id': card['id'],
                'list': list_name
            })

        # VALIDATION 7: Pattern violations
        if self.pattern and not self.pattern.search(card['name']):
            self.cards_without_pattern.append({
                'name': card['name'],
                'id': card['id'],
                'list': list_name
            })

        # VALIDATION 8: Critical lists without descriptions
        if is_critical and not card.get('desc', '').strip():
            self.cards_without_description_critical.append({
                'name': card['name'],
                'id': card['id'],
                'list': list_name
            })

    def _calculate_results(self):
        """Calculate audit results and health score"""
        critical_issues = 0
        high_issues = 0
        medium_issues = 0

        if self.done_cards_no_due: critical_issues += 1
        if self.done_cards_incomplete_checklist: critical_issues += 1
        if self.overdue_not_complete: critical_issues += 1
        if self.active_cards_no_due: high_issues += 1
        if self.execution_cards_no_members: high_issues += 1
        if self.empty_checklists: medium_issues += 1
        if self.cards_without_pattern: medium_issues += 1
        if self.cards_without_description_critical: medium_issues += 1

        health_score = max(0, 100 - (critical_issues * 20) - (high_issues * 10) - (medium_issues * 5))

        return {
            'board_name': self.board_name,
            'board_id': self.board_id,
            'total_lists': self.total_lists,
            'total_cards': self.total_cards,
            'critical_issues': critical_issues,
            'high_issues': high_issues,
            'medium_issues': medium_issues,
            'health_score': health_score,
            'findings': {
                'done_no_due': self.done_cards_no_due,
                'done_incomplete_checklist': self.done_cards_incomplete_checklist,
                'active_no_due': self.active_cards_no_due,
                'overdue_not_complete': self.overdue_not_complete,
                'execution_no_members': self.execution_cards_no_members,
                'empty_checklists': self.empty_checklists,
                'pattern_violations': self.cards_without_pattern,
                'critical_no_description': self.cards_without_description_critical
            }
        }


def print_json_report(results):
    """Print results in JSON format"""
    report = {
        'board_id': results['board_id'],
        'board_name': results['board_name'],
        'audit_timestamp': datetime.now().isoformat(),
        'summary': {
            'total_lists': results['total_lists'],
            'total_cards': results['total_cards'],
            'critical_issues': results['critical_issues'],
            'high_issues': results['high_issues'],
            'medium_issues': results['medium_issues'],
            'health_score': results['health_score']
        },
        'critical_findings': {
            'done_no_due': len(results['findings']['done_no_due']),
            'done_incomplete_checklist': len(results['findings']['done_incomplete_checklist']),
            'overdue_not_complete': len(results['findings']['overdue_not_complete'])
        },
        'high_findings': {
            'active_no_due': len(results['findings']['active_no_due']),
            'execution_no_members': len(results['findings']['execution_no_members'])
        },
        'medium_findings': {
            'empty_checklists': len(results['findings']['empty_checklists']),
            'pattern_violations': len(results['findings']['pattern_violations']),
            'critical_no_description': len(results['findings']['critical_no_description'])
        }
    }
    print(json.dumps(report, indent=2))


def print_human_report(results):
    """Print results in human-readable format"""
    print(f"\n{'='*80}")
    print(f"🔍 BOARD AUDIT REPORT - {results['board_name']}")
    print(f"Board ID: {results['board_id']}")
    print(f"Audit Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*80}\n")

    # Summary
    print(f"📊 BOARD SUMMARY:")
    print(f"   Total Lists: {results['total_lists']}")
    print(f"   Total Cards: {results['total_cards']}")
    print(f"   Critical Issues: {results['critical_issues']}")
    print(f"   High Priority Issues: {results['high_issues']}")
    print(f"   Medium Priority Issues: {results['medium_issues']}")
    print()

    # Critical Issues
    print(f"{'='*80}")
    print(f"🔴 CRITICAL ISSUES (Workflow Killers)")
    print(f"{'='*80}\n")

    findings = results['findings']

    if findings['done_no_due']:
        print(f"❌ CARDS IN 'DONE' WITHOUT DUE DATE: {len(findings['done_no_due'])} card(s)")
        print(f"   Problem: No traceability - when was this completed?")
        print(f"   Impact: Cannot measure velocity or predict future work\n")
        for item in findings['done_no_due'][:10]:
            print(f"   • {item['name'][:55]}")
            print(f"     List: {item['list']} | ID: {item['id']}")
        if len(findings['done_no_due']) > 10:
            print(f"   ... and {len(findings['done_no_due']) - 10} more")
        print()
    else:
        print(f"✅ All 'Done' cards have due dates\n")

    if findings['done_incomplete_checklist']:
        print(f"❌ CARDS IN 'DONE' WITH INCOMPLETE CHECKLISTS: {len(findings['done_incomplete_checklist'])} card(s)")
        print(f"   Problem: Marked complete but checklist says otherwise")
        print(f"   Impact: False sense of completion, missing deliverables\n")
        for item in findings['done_incomplete_checklist'][:10]:
            print(f"   • {item['name'][:55]}")
            print(f"     List: {item['list']} | Checklist: {item['completed']}/{item['total']} items")
        if len(findings['done_incomplete_checklist']) > 10:
            print(f"   ... and {len(findings['done_incomplete_checklist']) - 10} more")
        print()
    else:
        print(f"✅ All 'Done' cards have complete checklists\n")

    if findings['overdue_not_complete']:
        print(f"❌ OVERDUE CARDS NOT MARKED COMPLETE: {len(findings['overdue_not_complete'])} card(s)")
        print(f"   Problem: Past due date but still in active workflow")
        print(f"   Impact: Zombie tasks that kill sprint health\n")
        sorted_overdue = sorted(findings['overdue_not_complete'], key=lambda x: x['days_overdue'], reverse=True)
        for item in sorted_overdue[:10]:
            days = item['days_overdue']
            urgency = "🔴 CRITICAL" if days > 7 else "🟠 HIGH" if days > 3 else "🟡 MEDIUM"
            print(f"   {urgency} │ {days} days overdue")
            print(f"           │ {item['name'][:50]}")
            print(f"           │ List: {item['list']}")
            print()
        if len(findings['overdue_not_complete']) > 10:
            print(f"   ... and {len(findings['overdue_not_complete']) - 10} more")
        print()
    else:
        print(f"✅ No overdue cards in active workflow\n")

    # High Priority
    print(f"{'='*80}")
    print(f"🟠 HIGH PRIORITY ISSUES (Execution Blockers)")
    print(f"{'='*80}\n")

    if findings['active_no_due']:
        print(f"⚠️  ACTIVE CARDS WITHOUT DUE DATES: {len(findings['active_no_due'])} card(s)")
        print(f"   Problem: How do you know if they're late?")
        print(f"   Impact: No accountability, no sprint planning possible\n")
        by_list = defaultdict(list)
        for item in findings['active_no_due']:
            by_list[item['list']].append(item)
        for list_name in sorted(by_list.keys()):
            items = by_list[list_name]
            print(f"   📋 {list_name} ({len(items)} card(s)):")
            for item in items[:5]:
                print(f"      • {item['name'][:55]}")
            if len(items) > 5:
                print(f"      ... and {len(items) - 5} more")
            print()
    else:
        print(f"✅ All active cards have due dates\n")

    if findings['execution_no_members']:
        print(f"⚠️  EXECUTION CARDS WITHOUT ASSIGNED MEMBERS: {len(findings['execution_no_members'])} card(s)")
        print(f"   Problem: Who's doing this work?")
        print(f"   Impact: Orphaned tasks that nobody owns\n")
        by_list = defaultdict(list)
        for item in findings['execution_no_members']:
            by_list[item['list']].append(item)
        for list_name in sorted(by_list.keys()):
            items = by_list[list_name]
            print(f"   📋 {list_name} ({len(items)} card(s)):")
            for item in items[:5]:
                print(f"      • {item['name'][:55]}")
            if len(items) > 5:
                print(f"      ... and {len(items) - 5} more")
            print()
    else:
        print(f"✅ All execution cards have assigned members\n")

    # Health Score
    print(f"{'='*80}")
    print(f"📊 BOARD HEALTH SCORE")
    print(f"{'='*80}\n")

    score = results['health_score']
    if score >= 90:
        status = "🟢 EXCELLENT"
        message = "Your board is well-maintained and ready for production"
    elif score >= 70:
        status = "🟡 GOOD"
        message = "Minor issues detected, but generally healthy"
    elif score >= 50:
        status = "🟠 NEEDS ATTENTION"
        message = "Significant workflow issues detected"
    else:
        status = "🔴 CRITICAL"
        message = "Board has severe structural problems affecting delivery"

    print(f"Health Score: {score}/100 - {status}")
    print(f"Assessment: {message}")
    print(f"\n{'='*80}\n")


def main():
    """Main plugin entry point"""
    # Parse arguments
    if len(sys.argv) < 2:
        print("❌ Usage: trello plugin run board-audit <board_id> [--json] [--pattern \"REGEX\"]")
        print("\nExamples:")
        print("  trello plugin run board-audit 68fcf05e481843db13204397")
        print("  trello plugin run board-audit 68fcf05e481843db13204397 --json")
        print('  trello plugin run board-audit 68fcf05e481843db13204397 --pattern "PF-[A-Z]+-\\d+"')
        return 1

    board_id = sys.argv[1]
    json_output = '--json' in sys.argv
    pattern = None

    # Extract pattern if provided
    for i, arg in enumerate(sys.argv):
        if arg == '--pattern' and i + 1 < len(sys.argv):
            pattern = sys.argv[i + 1]
            break

    # Get credentials from environment
    api_key = os.environ.get('TRELLO_API_KEY')
    token = os.environ.get('TRELLO_TOKEN')
    base_url = os.environ.get('TRELLO_BASE_URL', 'https://api.trello.com/1')

    if not api_key or not token:
        print("❌ Missing API credentials", file=sys.stderr)
        print("   Run 'trello config' to set up credentials", file=sys.stderr)
        return 1

    # Initialize client and auditor
    client = TrelloClient(api_key, token, base_url)
    auditor = BoardAuditor(client, board_id, pattern)

    # Run audit
    try:
        results = auditor.run_audit()
    except Exception as e:
        print(f"❌ Audit failed: {e}", file=sys.stderr)
        return 1

    # Print results
    if json_output:
        print_json_report(results)
    else:
        print_human_report(results)

    return 0


if __name__ == '__main__':
    sys.exit(main())
