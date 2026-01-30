#!/bin/bash
#
# ffs.sh - FZF-based Forge Sender (Human Use)
# Interactive tmux pane selector with message sending capability
#
# Usage: ./ffs.sh [--help] [-b|--broadcast] [message]
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HISTORY_FILE="${HOME}/.config/agent-forge/ffs_history"
HISTORY_LIMIT=12

CURRENT_PANE=$(tmux display-message -p '#{pane_id}')
CURRENT_SESSION=$(tmux display-message -p '#{session_name}')

show_help() {
    cat >&2 << 'EOF'
Usage: ffs.sh [OPTIONS] [message]

FZF-based interactive sender for tmux panes.

OPTIONS:
  -b, --broadcast    Broadcast message to all panes
  --help             Show this help message

MODES:
  1. With message:    ffs.sh "Hello world"
     → Select pane via fzf and send

  2. Without message: ffs.sh
     → Select/enter message via fzf (with history)
     → Select pane via fzf and send

  3. Broadcast:       ffs.sh -b "Hello all"
     → Send to all panes except self

HISTORY:
  Last 12 messages are saved to ~/.config/agent-forge/ffs_history
  When entering message, use UP/DOWN to select from history.
EOF
}

init_history() {
    local history_dir="$(dirname "$HISTORY_FILE")"
    [[ -d "$history_dir" ]] || mkdir -p "$history_dir"
    [[ -f "$HISTORY_FILE" ]] || touch "$HISTORY_FILE"
}

add_to_history() {
    local message="$1"
    init_history

    if [[ -f "$HISTORY_FILE" ]]; then
        grep -vFx "$message" "$HISTORY_FILE" 2>/dev/null > "${HISTORY_FILE}.tmp" || true
        mv "${HISTORY_FILE}.tmp" "$HISTORY_FILE"
    fi

    echo "$message" | cat - "$HISTORY_FILE" 2>/dev/null > "${HISTORY_FILE}.tmp" || echo "$message" > "${HISTORY_FILE}.tmp"
    mv "${HISTORY_FILE}.tmp" "$HISTORY_FILE"

    if [[ -f "$HISTORY_FILE" ]]; then
        head -n "$HISTORY_LIMIT" "$HISTORY_FILE" > "${HISTORY_FILE}.tmp"
        mv "${HISTORY_FILE}.tmp" "$HISTORY_FILE"
    fi
}

select_message_with_history() {
    init_history

    local header_msg="Type message or select from history (UP/DOWN) | Ctrl-C to cancel"
    local selected

    if [[ -s "$HISTORY_FILE" ]]; then
        selected=$(tac "$HISTORY_FILE" 2>/dev/null | fzf \
            --prompt="Message: " \
            --header="$header_msg" \
            --print-query \
            --height=50% \
            --reverse \
            || true)
    else
        selected=$(fzf \
            --prompt="Message: " \
            --header="$header_msg" \
            --print-query \
            --height=20% \
            --reverse \
            < /dev/null \
            || true)
    fi

    if [[ -z "$selected" ]]; then
        return 1
    fi

    echo "$selected" | tail -n1
}

get_pane_list() {
    tmux list-panes -s -F "#{pane_id}|#{session_name}|#{window_index}|#{window_name}|#{pane_index}|#{pane_title}|#{pane_current_command}" | \
    grep -v "^${CURRENT_PANE}|" | \
    while IFS='|' read -r pane_id session window_idx window_name pane_idx title cmd; do
        printf "%-30s | %-20s | %s\n" "${session}:${window_idx}.${pane_idx} (${window_name})" "${title:-no-title}" "${cmd:-none}"
    done
}

get_all_pane_ids() {
    tmux list-panes -s -F "#{pane_id}" | grep -v "^${CURRENT_PANE}$"
}

send_to_pane() {
    local pane_id="$1"
    local message="$2"
    local formatted_msg="you: ${message}"

    tmux send-keys -t "$pane_id" "$formatted_msg"
    tmux send-keys -t "$pane_id" C-m
}

broadcast_message() {
    local message="$1"
    local count=0

    echo "Broadcasting to all panes..."
    while IFS= read -r pane_id; do
        if [[ -n "$pane_id" ]]; then
            send_to_pane "$pane_id" "$message"
            ((count++)) || true
        fi
    done < <(get_all_pane_ids)

    echo "Sent to $count pane(s)"
    add_to_history "$message"
}

select_pane() {
    local selected
    selected=$(get_pane_list | fzf --prompt="Select target pane: " --height=50% --reverse --header="SESSION:WINDOW.PANE | TITLE | COMMAND")

    if [[ -z "$selected" ]]; then
        echo "No pane selected" >&2
        return 1
    fi

    local session_window=$(echo "$selected" | cut -d'|' -f1 | sed 's/ *$//' | cut -d'(' -f1 | sed 's/ *$//')
    local session=$(echo "$session_window" | cut -d':' -f1)
    local window_idx=$(echo "$session_window" | cut -d':' -f2 | cut -d'.' -f1)
    local pane_idx=$(echo "$session_window" | cut -d'.' -f2 | cut -d' ' -f1)

    tmux list-panes -s -F "#{pane_id}|#{session_name}|#{window_index}|#{pane_index}" | \
        grep "|${session}|${window_idx}|${pane_idx}$" | cut -d'|' -f1
}

main() {
    local message=""
    local broadcast_mode=false
    local skip_message_input=false

    while [[ $# -gt 0 ]]; do
        case "$1" in
            -b|--broadcast)
                broadcast_mode=true
                shift
                ;;
            --help)
                show_help
                exit 0
                ;;
            -*)
                echo "Unknown option: $1" >&2
                show_help
                exit 1
                ;;
            *)
                message="$*"
                skip_message_input=true
                break
                ;;
        esac
    done

    if [[ $# -eq 0 ]] && [[ "$skip_message_input" == false ]]; then
        show_help
        exit 1
    fi


    if [[ "$skip_message_input" == false ]]; then
        message=$(select_message_with_history)
        if [[ -z "$message" ]]; then
            echo "No message entered" >&2
            exit 1
        fi
    fi

    if [[ "$broadcast_mode" == true ]]; then
        broadcast_message "$message"
        exit 0
    fi

    local target_pane
    target_pane=$(select_pane)
    if [[ -z "$target_pane" ]]; then
        exit 1
    fi

    local pane_info
    pane_info=$(tmux list-panes -s -F "#{pane_id}|#{session_name}|#{window_name}|#{pane_title}" | grep "^${target_pane}|" || true)
    if [[ -n "$pane_info" ]]; then
        IFS='|' read -r _ session window_name title <<< "$pane_info"
        echo "Sending to ${session}:${window_name} (${title:-no-title}): ${message}"
    fi

    send_to_pane "$target_pane" "$message"
    add_to_history "$message"
}

main "$@"
