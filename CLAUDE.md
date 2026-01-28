# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Agent Forge** is an OS-level multi-agent orchestration platform leveraging `tmux`. It uses **tmuxp** (YAML) and **libtmux** (Python) to build declarative, programmable workspaces for AI agents.

The core innovation is the **Forge Link protocol** enabling agent collaboration through:
1. **Declarative Environment** - Workspaces defined via `.forge.yaml` (tmuxp configuration)
2. **Reactive Exchange** - Bidirectional communication via `forge send` (input) and `forge read` (observation)
3. **Payload Exchange** - Shared file system for large context (Specification Driven Development)

## Common Development Commands

```bash
# Setup (creates venv and installs dependencies in editable mode)
task setup

# Run tests
task test
```

Without Taskfile:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -e .
python3 -m unittest discover tests
```

## Architecture

### Core Components

- **`agent_forge/`** - Main Python package (CLI and controller logic)
- **`docs/FORGE_BLUEPRINT.md`** - Architecture definition and Forge Link protocol
- **`docs/PLAN.md`** - Implementation roadmap (in Japanese)

### Standard Agent Roles (The "Company")

Agents collaborate in specialized tmux panes:

- **Architect (Design Pane)** - High-level design, writes `docs/specs/*.md`
- **Implementer (Code Pane)** - Writes code based on specs
- **Reviewer (QA Pane)** - Tests, security checks, provides feedback

### The Forge Loop Workflow

1. **Initialization**: `forge init` creates `.forge.yaml` from template
2. **Departure**: `forge start` launches tmux session with agents
3. **Orchestration**: User (Shogun) dispatches goals; agents coordinate via `forge` CLI
4. **Termination**: `forge stop` safely shuts down session

### Planned CLI Commands

- `init` - Create scaffold `.forge.yaml`
- `start` - Launch tmux session
- `send <target> "<command>"` - Send keys to target pane
- `read <target>` - Capture output from target pane
- `list` - Display active sessions and panes

## Implementation Status

**Current Phase**: Phase 1 - Skeleton & CLI Base

The project is in early planning phase. The structure is established but implementation has not begun.

## Technical Stack

- **Python**: 3.10+
- **Core Dependencies**: `tmuxp` (session management), `libtmux` (tmux control)
- **CLI Framework**: `click` (entry point: `agent_forge.cli:main`)
- **Build Tools**: `Taskfile.yml` (go-task), `pyproject.toml` (setuptools)

## Key Design Philosophy

**Specification Driven Development (SDD)**: Agents exchange context via files, not chat bubbles. Large context is passed through the shared file system as "payload", while `forge send/read` handles real-time interaction.

## Documentation References

- `docs/FORGE_BLUEPRINT.md` - Complete protocol definition
- `docs/PLAN.md` - Detailed implementation phases (Japanese)
- `docs/FORGE_RESOURCES.md` - References and inspirations
