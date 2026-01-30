#!/bin/bash
#
# read.sh - Read output from AI agents in tmux panes
#

show_help() {
    cat >&2 << 'EOF'
Usage: read.sh <target_partial_name> [lines]

Read recent output from an AI agent running in another tmux pane.
Useful for checking what another agent is doing or has completed.

ARGUMENTS:
  target_partial_name    Partial match of the target pane title
  lines                  Number of lines to read (default: 20)

USE CASES:
  1. Check implementer's recent output:
     read.sh implementer

  2. Read more lines from architect pane:
     read.sh architect 50

  3. Monitor test results in reviewer pane:
     read.sh reviewer 100

  4. Quick peek at any agent's current activity:
     read.sh gemini

NOTES:
  - Captures the last N lines of the pane's visible content
  - Preserves colors and escape sequences
  - Output is printed to stdout
EOF
}

TARGET=${1:-}
LINES=${2:-20}

if [ -z "$TARGET" ]; then
    show_help
    exit 1
fi

# Find target pane
TARGET_INFO=$(tmux list-panes -s -F "#{pane_id}:#{pane_title}" | grep -i "$TARGET" | head -n1)
TARGET_PANE=$(echo "$TARGET_INFO" | cut -d: -f1)
TARGET_TITLE=$(echo "$TARGET_INFO" | cut -d: -f2-)

if [ -z "$TARGET_PANE" ]; then
    echo "Error: Target pane matching '$TARGET' not found."
    exit 1
fi

echo "--- Reading from '$TARGET_TITLE' ($TARGET_PANE) [Last $LINES lines] ---"
# -e captures escape sequences (colors)
tmux capture-pane -t "$TARGET_PANE" -pe -S -"$LINES"
echo "--- End of output ---"