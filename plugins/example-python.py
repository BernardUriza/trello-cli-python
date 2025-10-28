#!/usr/bin/env python3
# trello-plugin
# name: Example Python Plugin
# description: Template for creating Python-based Trello CLI plugins
# usage: plugin run example-python [args]
# author: Trello CLI
# version: 1.0.0

"""
Example Python plugin for Trello CLI

This plugin demonstrates how to:
- Access Trello API credentials from environment
- Make API calls to Trello
- Parse command-line arguments
- Provide helpful output
"""

import os
import sys
import requests


def main():
    # Get credentials from environment
    api_key = os.environ.get('TRELLO_API_KEY')
    token = os.environ.get('TRELLO_TOKEN')
    base_url = os.environ.get('TRELLO_BASE_URL', 'https://api.trello.com/1')

    if not api_key or not token:
        print("❌ Missing API credentials", file=sys.stderr)
        print("   Run 'trello config' to set up credentials", file=sys.stderr)
        return 1

    # Parse arguments
    if len(sys.argv) < 2:
        print("Usage: plugin run example-python <board_id>")
        print("\nThis example plugin lists all lists in a board")
        return 1

    board_id = sys.argv[1]

    # Make API call
    try:
        url = f"{base_url}/boards/{board_id}/lists"
        params = {'key': api_key, 'token': token}
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        lists = response.json()

        print(f"\n✅ Found {len(lists)} list(s) in board {board_id}:\n")
        for lst in lists:
            print(f"  • {lst['name']} (ID: {lst['id']})")

        return 0

    except requests.exceptions.RequestException as e:
        print(f"❌ API Error: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
