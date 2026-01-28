"""Configuration management for Agent Forge."""

from pathlib import Path

FORGE_CONFIG_FILE = ".forge.yaml"

DEFAULT_FORGE_CONFIG = """# Agent Forge Configuration
# This file defines the tmux workspace for AI agents

session_name: "forge-session"

windows:
  - window_name: architect
    layout: main-vertical
    panes:
      - shell_command:
          - echo "Architect Pane: High-level design and specs"
        focus: true

  - window_name: implementer
    layout: main-vertical
    panes:
      - shell_command:
          - echo "Implementer Pane: Write code based on specs"

  - window_name: reviewer
    layout: main-vertical
    panes:
      - shell_command:
          - echo "Reviewer Pane: Testing and QA"
"""


def get_config_path(directory: str = ".") -> Path:
    """Get the path to the Forge config file."""
    return Path(directory) / FORGE_CONFIG_FILE


def config_exists(directory: str = ".") -> bool:
    """Check if Forge config file exists in the specified directory."""
    return get_config_path(directory).exists()


def load_config(directory: str = "."):
    """Load Forge config from the specified directory.

    Returns None if config does not exist.
    """
    import yaml

    config_path = get_config_path(directory)
    if not config_path.exists():
        return None

    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def write_default_config(directory: str = ".", overwrite: bool = False):
    """Write the default Forge config to the specified directory.

    Args:
        directory: Target directory path
        overwrite: If False, raises FileExistsError when config exists

    Raises:
        FileExistsError: If config already exists and overwrite is False
    """
    config_path = get_config_path(directory)

    if not overwrite and config_path.exists():
        raise FileExistsError(f"{FORGE_CONFIG_FILE} already exists in {directory}")

    config_path.write_text(DEFAULT_FORGE_CONFIG)
