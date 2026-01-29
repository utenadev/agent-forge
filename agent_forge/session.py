"""Session management for Agent Forge."""

from typing import Optional

import yaml
from libtmux import Server, Session, Pane
from tmuxp.workspace.builder import WorkspaceBuilder


def get_session(session_name: str) -> Optional[Session]:
    """Get an active tmux session by name.

    Args:
        session_name: Name of the session to find

    Returns:
        Session object if found, None otherwise
    """
    server = Server()
    for session in server.sessions:
        if session.name == session_name:
            return session
    return None


def find_pane(session: Session, target_name: str) -> Optional[Pane]:
    """Find a pane within a session by window name.

    Args:
        session: libtmux Session object
        target_name: Window name to search for (case-insensitive)

    Returns:
        First Pane object of the matching window, None if not found
    """
    target_lower = target_name.lower()
    for window in session.windows:
        if window.window_name.lower() == target_lower:
            # Return the first pane of the window
            return window.panes[0] if window.panes else None
    return None


def start_forge(
    config_path: str, session_name: Optional[str] = None, attach: bool = False
) -> Session:
    """Start a Forge tmux session from a config file.

    Args:
        config_path: Path to the .forge.yaml config file
        session_name: Optional session name (overrides config)
        attach: If True, attach to the session after starting

    Returns:
        The created Session object
    """
    # Load YAML config
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    # Override session name if provided
    if session_name:
        config["session_name"] = session_name

    # Create server and builder
    server = Server()
    builder = WorkspaceBuilder(config, server)

    # Build the session
    builder.build()

    # Return the created session
    return server.find_where({"session_name": config["session_name"]})


def stop_session(session_name: str) -> Optional[Session]:
    """Stop a tmux session by name.

    Args:
        session_name: Name of the session to stop

    Returns:
        Session object if found and stopped, None if not found
    """
    session = get_session(session_name)
    if session:
        session.kill()
    return session
