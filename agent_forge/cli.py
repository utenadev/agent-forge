import click

from agent_forge import __version__
from agent_forge.config import (
    FORGE_CONFIG_FILE,
    config_exists,
    write_default_config,
    load_config,
)
from agent_forge.session import get_session, find_pane, start_forge, stop_session
from agent_forge.actions import send_command, read_output


def get_available_panes(session):
    """Get list of available window names from a session."""
    return [w.window_name for w in session.windows]


@click.group()
@click.version_option(version=__version__)
def main():
    """Agent Forge - Orchestrate AI agents in tmux with Shogun style."""
    pass


@main.command()
@click.option("--force", is_flag=True, help="Overwrite existing config file")
def init(force):
    """Initialize a new Forge workspace."""
    if config_exists() and not force:
        click.echo(
            f"Error: {FORGE_CONFIG_FILE} already exists. Use --force to overwrite."
        )
        raise click.Abort()

    overwrite = force
    try:
        write_default_config(overwrite=overwrite)
        click.echo(f"Created {FORGE_CONFIG_FILE}")
    except FileExistsError as e:
        click.echo(f"Error: {e}")
        raise click.Abort()


@main.command()
@click.option("--session-name", help="Override session name from config")
@click.option("--attach", is_flag=True, help="Attach to session after starting")
def start(session_name, attach):
    """Start the Forge tmux session."""
    if not config_exists():
        click.echo(f"Error: {FORGE_CONFIG_FILE} not found. Run 'forge init' first.")
        raise click.Abort()

    config = load_config()
    default_session = config.get("session_name", "forge-session")
    name = session_name or default_session

    try:
        session = start_forge(FORGE_CONFIG_FILE, session_name=name, attach=attach)
        click.echo(f"Started session: {session.name}")
    except Exception as e:
        click.echo(f"Error starting session: {e}")
        raise click.Abort()


@main.command()
@click.argument("target")
@click.argument("message", nargs=-1, required=True)
def send(target, message):
    """Send a command to a target pane."""
    # Get default session name from config
    config = load_config()
    if not config:
        click.echo(f"Error: {FORGE_CONFIG_FILE} not found. Run 'forge init' first.")
        return 1

    session_name = config.get("session_name", "forge-session")
    session = get_session(session_name)

    if not session:
        click.echo(
            f"Error: Session '{session_name}' not found. Run 'forge start' first."
        )
        return 1

    pane = find_pane(session, target)
    if not pane:
        # Get available panes for helpful error message
        available = get_available_panes(session)
        click.echo(f"Error: Pane '{target}' not found in session.")
        if available:
            click.echo(f"Available panes: {', '.join(available)}")
        return 0

    cmd = " ".join(message)
    send_command(pane, cmd)
    click.echo(f"Sent to {target}: {cmd}")
    return 0


@main.command()
@click.argument("target")
@click.option("--lines", default=100, help="Number of lines to read")
def read(target, lines):
    """Read output from a target pane."""
    # Get default session name from config
    config = load_config()
    if not config:
        click.echo(f"Error: {FORGE_CONFIG_FILE} not found. Run 'forge init' first.")
        raise click.Abort()

    session_name = config.get("session_name", "forge-session")
    session = get_session(session_name)

    if not session:
        click.echo(
            f"Error: Session '{session_name}' not found. Run 'forge start' first."
        )
        raise click.Abort()

    pane = find_pane(session, target)
    if not pane:
        # Get available panes for helpful error message
        available = get_available_panes(session)
        click.echo(f"Error: Pane '{target}' not found in session.")
        if available:
            click.echo(f"Available panes: {', '.join(available)}")
        return 0

    output = read_output(pane, lines)
    click.echo("\n".join(output))


@main.command()
@click.option("--session-name", help="Override session name from config")
def stop(session_name):
    """Stop the Forge tmux session."""
    if not config_exists():
        click.echo(f"Error: {FORGE_CONFIG_FILE} not found. Run 'forge init' first.")
        raise click.Abort()

    config = load_config()
    default_session = config.get("session_name", "forge-session")
    name = session_name or default_session

    session = stop_session(name)
    if session:
        click.echo(f"Stopped session: {name}")
    else:
        click.echo(f"Session '{name}' not found.")


@main.command()
def list():
    """List active Forge sessions and panes in tabular format."""
    try:
        from libtmux import Server

        server = Server()
    except Exception:
        click.echo("Error: Could not connect to tmux server.")
        raise click.Abort()

    if not server.sessions:
        click.echo("No active sessions.")
        return

    # Table headers
    headers = ["SESSION", "WINDOW", "PANE", "TITLE", "CURRENT CMD"]

    # Calculate column widths
    session_width = max(len(headers[0]), max(len(s.name) for s in server.sessions))
    window_width = max(len(headers[1]), 12)  # "1:architect" format
    pane_width = max(len(headers[2]), 4)  # "%1" format
    title_width = max(len(headers[3]), 18)
    cmd_width = max(len(headers[4]), 10)

    # Print header
    header_format = f"{{:<{session_width}}} {{:<{window_width}}} {{:<{pane_width}}} {{:<{title_width}}} {{:<{cmd_width}}}"
    click.echo(header_format.format(*headers))

    # Collect and print rows
    current_session = None
    for session in server.sessions:
        for window in session.windows:
            for pane in window.panes:
                # Get pane attributes
                pane_title = getattr(pane, "pane_title", "")
                current_cmd = getattr(pane, "current_command", "")

                # Format session name (show once per session)
                session_name = session.name if session.name != current_session else ""
                current_session = session.name

                # Format window (index:name)
                window_str = f"{window.window_index}:{window.window_name}"

                # Format pane (%index)
                pane_str = f"%{pane.pane_index}"

                # Print row
                row_format = f"{{:<{session_width}}} {{:<{window_width}}} {{:<{pane_width}}} {{:<{title_width}}} {{:<{cmd_width}}}"
                click.echo(
                    row_format.format(
                        session_name, window_str, pane_str, pane_title, current_cmd
                    )
                )
