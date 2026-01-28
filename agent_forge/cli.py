import click

from agent_forge import __version__


@click.group()
@click.version_option(version=__version__)
def main():
    """Agent Forge - Orchestrate AI agents in tmux with Shogun style."""
    pass


@main.command()
def init():
    """Initialize a new Forge workspace."""
    click.echo("Initializing Forge workspace...")


@main.command()
def start():
    """Start the Forge tmux session."""
    click.echo("Starting Forge session...")


@main.command()
@click.argument("target")
@click.argument("message", nargs=-1)
def send(target, message):
    """Send a command to a target pane."""
    click.echo(f"Sending to {target}: {' '.join(message)}")


@main.command()
@click.argument("target")
def read(target):
    """Read output from a target pane."""
    click.echo(f"Reading from {target}...")


@main.command()
def list():
    """List active Forge sessions and panes."""
    click.echo("Listing active sessions...")
