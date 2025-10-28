#!/bin/bash
# trello-plugin
# name: Example Bash Plugin
# description: Template for creating Bash-based Trello CLI plugins
# usage: plugin run example-bash <board_id>
# author: Trello CLI
# version: 1.0.0

# Example Bash plugin for Trello CLI
#
# This plugin demonstrates how to:
# - Access Trello API credentials from environment
# - Make API calls using curl
# - Parse command-line arguments
# - Provide helpful output

set -e

# Check for required tools
if ! command -v curl &> /dev/null; then
    echo "❌ curl is required but not installed" >&2
    exit 1
fi

if ! command -v jq &> /dev/null; then
    echo "❌ jq is required but not installed" >&2
    exit 1
fi

# Get credentials from environment
API_KEY="${TRELLO_API_KEY}"
TOKEN="${TRELLO_TOKEN}"
BASE_URL="${TRELLO_BASE_URL:-https://api.trello.com/1}"

if [[ -z "$API_KEY" ]] || [[ -z "$TOKEN" ]]; then
    echo "❌ Missing API credentials" >&2
    echo "   Run 'trello config' to set up credentials" >&2
    exit 1
fi

# Parse arguments
if [[ $# -lt 1 ]]; then
    echo "Usage: plugin run example-bash <board_id>"
    echo ""
    echo "This example plugin shows board members"
    exit 1
fi

BOARD_ID="$1"

# Make API call
URL="${BASE_URL}/boards/${BOARD_ID}/members?key=${API_KEY}&token=${TOKEN}"

response=$(curl -s -w "\n%{http_code}" "$URL")
http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | sed '$d')

if [[ "$http_code" != "200" ]]; then
    echo "❌ API Error: HTTP $http_code" >&2
    echo "$body" | jq '.' >&2
    exit 1
fi

# Parse and display results
member_count=$(echo "$body" | jq '. | length')

echo ""
echo "✅ Found $member_count member(s) in board $BOARD_ID:"
echo ""

echo "$body" | jq -r '.[] | "  • \(.fullName) (@\(.username))"'

exit 0
