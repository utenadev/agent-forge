#!/bin/bash

# Usage: ./send.sh <target_partial_name> <message>

TARGET=$1
shift
MESSAGE="$*"

if [ -z "$TARGET" ] || [ -z "$MESSAGE" ]; then
    echo "Usage: $0 <target_partial_name> <message>"
    exit 1
fi

# Determine Sender Name
# 1. AGENT_NAME env var
# 2. pane_title (cleaned up)
# 3. Default "gemini"
if [ -n "$AGENT_NAME" ]; then
    SENDER="$AGENT_NAME"
else
    RAW_TITLE=$(tmux display-message -p '#{pane_title}')
    # Simple cleanup: take first word if it looks like a name, else default
    SENDER="gemini"
fi

# Find target pane ID by partial title match
# Search all panes in current session
# Output format: %1:My Title
# We use grep to find the line containing the target string (case insensitive)
TARGET_INFO=$(tmux list-panes -s -F "#{pane_id}:#{pane_title}" | grep -i "$TARGET" | head -n1)
TARGET_PANE=$(echo "$TARGET_INFO" | cut -d: -f1)
TARGET_TITLE=$(echo "$TARGET_INFO" | cut -d: -f2-)

if [ -z "$TARGET_PANE" ]; then
    echo "Error: Target pane matching '$TARGET' not found."
    # List available panes
    echo "Available panes:"
    tmux list-panes -s -F " - #{pane_title}"
    exit 1
fi

# Send message
# Format: "sender: message"
FULL_MSG="$SENDER: $MESSAGE"

echo "Sending to '$TARGET_TITLE' ($TARGET_PANE): $FULL_MSG"
tmux send-keys -t "$TARGET_PANE" "$FULL_MSG"
tmux send-keys -t "$TARGET_PANE" C-m
