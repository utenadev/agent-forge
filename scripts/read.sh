#!/bin/bash
# Usage: ./read.sh <target_partial_name> [lines]

TARGET=$1
LINES=${2:-20}

if [ -z "$TARGET" ]; then
    echo "Usage: $0 <target_partial_name> [lines]"
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