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
# Setup with uv (recommended)
uv venv
uv pip install -e .

# Run tests
uv run python3 -m unittest discover tests -v

# Run CLI
uv run agent-forge --help
```

With Taskfile:
```bash
task setup  # Creates venv and installs dependencies
task test   # Runs tests
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

## Development Workflow

### TDD Approach (Red-Green-Refactor)

Follow t_wada's TDD style:

1. **Write failing test first (RED)**
   - Create/update test file in `tests/`
   - Run tests to confirm failure

2. **Implement minimal code to pass (GREEN)**
   - Write just enough code to make tests pass
   - Run tests to confirm success

3. **Commit after each GREEN**
   - Use conventional commit format
   - Update `docs/WorkingLog.md` with progress

### Development Steps

```bash
# 1. Create feature branch
git checkout -b feature/<name>

# 2. Write test (RED)
# Create tests/test_<feature>.py

# 3. Run tests - expect failure
uv run python3 -m unittest discover tests -v

# 4. Implement (GREEN)
# Create agent_forge/<feature>.py

# 5. Run tests - expect success
uv run python3 -m unittest discover tests -v

# 6. Update WorkingLog
# Edit docs/WorkingLog.md

# 7. Commit
git add .
git commit -m "feat: description

Co-Authored-By: Claude (GLM-4.7) <noreply@anthropic.com>"
```

### Commit Message Format

```
<type>: <description>

<optional detailed description>

Co-Authored-By: Claude (GLM-4.7) <noreply@anthropic.com>
```

Types: `feat`, `fix`, `test`, `docs`, `refactor`, `chore`

### Language Convention

- **Communication**: Japanese (with user)
- **Source code comments**: English
- **Commit messages**: English
- **Documentation**: English (unless Japanese-specific like PLAN.md)

## Implementation Status

| Phase | Description | Status |
|-------|-------------|--------|
| 1 | CLI Base | ✅ Completed - Basic command structure with tests |
| 2 | Forge Generator (init) | 🚧 In Progress |
| 3 | Controller (Runtime) | ⏳ Pending |
| 4 | CLI Commands | ⏳ Pending |
| 5 | Agent Skills | ⏳ Pending |
| 6 | Testing & Polish | ⏳ Pending |

### Completed
- Phase 1: CLI base with 5 commands (init, start, send, read, list)
- Test suite with 6 passing tests
- Project structure and documentation

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
