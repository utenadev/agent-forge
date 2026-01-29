# Spec 001: Detailed Session List

## Overview
Enhance the `forge list` command to provide rich, tabular information about active sessions, windows, and panes.
This will help users (Shogun) understand the state of their agent workforce at a glance.

## Requirements

### 1. Tabular Output
The output should be formatted as a table with the following columns:
- **SESSION**: Session name.
- **WINDOW**: Window index and name (e.g., `1:architect`).
- **PANE**: Pane index (e.g., `%1`).
- **TITLE**: Pane title (e.g., `Gemini`).
- **CURRENT CMD**: Currently executing command (if available from tmux).

### 2. Grouping
- Group output by Session, then by Window.

### 3. Implementation Details
- Use `libtmux` to fetch pane attributes.
    - Title: `pane_title` (`#{pane_title}`)
    - Command: `pane_current_command` (`#{pane_current_command}`)
    - Path: `pane_current_path` (`#{pane_current_path}`) - *Optional, maybe too long for table*
- Consider using a library like `tabulate` or standard string formatting for alignment.

### 4. Example Output

```text
SESSION        WINDOW          PANE  TITLE              CURRENT CMD
forge-session  1:architect     %1    Gemini             nvim
               1:architect     %2    Implementer        python
               2:reviewer      %3    Reviewer           bash
```

## Tasks (Implementer)
1. Create `tests/test_cli_list.py` to define expected output format.
2. Modify `agent_forge/cli.py` (or create `agent_forge/commands/list.py` if refactoring is needed) to implement the logic.
3. Ensure it handles cases where no sessions exist gracefully.
