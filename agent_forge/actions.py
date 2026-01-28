"""Communication primitives for interacting with tmux panes."""

from typing import List, Optional

from libtmux import Pane


def send_command(pane: Pane, cmd: str) -> None:
    """Send a command to a tmux pane.

    Args:
        pane: libtmux Pane object
        cmd: Command string to send
    """
    pane.send_keys(cmd)


def read_output(pane: Pane, lines: int = 100) -> List[str]:
    """Read output from a tmux pane.

    Args:
        pane: libtmux Pane object
        lines: Number of lines to capture from the bottom

    Returns:
        List of captured lines
    """
    return pane.capture_pane(start=-lines)
