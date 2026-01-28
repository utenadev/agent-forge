import click

from agent_forge import __version__
from agent_forge.config import FORGE_CONFIG_FILE, config_exists, write_default_config, load_config
from agent_forge.session import get_session, find_pane, start_forge
from agent_forge.actions import send_command, read_output


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
        click.echo(f"Error: {FORGE_CONFIG_FILE} already exists. Use --force to overwrite.")
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
        raise click.Abort()

    session_name = config.get("session_name", "forge-session")
    session = get_session(session_name)

    if not session:
        click.echo(f"Error: Session '{session_name}' not found. Run 'forge start' first.")
        raise click.Abort()

    pane = find_pane(session, target)
    if not pane:
        click.echo(f"Error: Pane '{target}' not found in session.")
        raise click.Abort()

    cmd = " ".join(message)
    send_command(pane, cmd)
    click.echo(f"Sent to {target}: {cmd}")


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
        click.echo(f"Error: Session '{session_name}' not found. Run 'forge start' first.")
        raise click.Abort()

    pane = find_pane(session, target)
    if not pane:
        click.echo(f"Error: Pane '{target}' not found in session.")
        raise click.Abort()

    output = read_output(pane, lines)
    click.echo("\n".join(output))


@main.command()
def list():
    """List active Forge sessions and panes."""
    server = None
    try:
        from libtmux import Server
        server = Server()
    except Exception:
        click.echo("Error: Could not connect to tmux server.")
        raise click.Abort()

    if not server.sessions:
        click.echo("No active sessions.")
        return

    for session in server.sessions:
        click.echo(f"Session: {session.name}")
        for window in session.windows:
            click.echo(f"  Window: {window.window_name}")
            for i, pane in enumerate(window.panes):
                click.echo(f"    Pane {i}: {pane}")
