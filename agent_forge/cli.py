import click

from agent_forge import __version__
from agent_forge.config import FORGE_CONFIG_FILE, config_exists, write_default_config


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
