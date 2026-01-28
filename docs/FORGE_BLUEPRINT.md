# Agent Forge: Blueprint

## Project Overview
**Agent Forge** is an OS-level multi-agent orchestration platform leveraging `tmux`. Instead of procedural shell scripts, it uses **tmuxp** (YAML) and **libtmux** (Python) to build declarative and programmable "workspaces" for AI agents.

The core philosophy is **Specification Driven Development (SDD)** coupled with a **"Company" of Agents**, where distinct roles (Architect, Implementer, Reviewer) collaborate within a shared, observable environment.

## Core Concept: "Forge Link" Protocol
The **Forge Link** is the protocol for agent collaboration, enabling bidirectional communication and state awareness.

### 1. Declarative Environment (The Forge)
Defined by `.forge.yaml` (a superset/alias of `.tmuxp.yaml`), this file describes the "office layout" for the agents.

**Standard Roles:**
- **The Architect (Design Pane):**
    - Responsibility: High-level design, writing `docs/specs/*.md`.
    - Tools: File system access, broad context.
- **The Implementer (Code Pane):**
    - Responsibility: Writing code based on specs.
    - Tools: Compiler/Linter, specialized context.
- **The Reviewer (QA Pane):**
    - Responsibility: Running tests, security checks, and providing feedback to the Implementer.

### 2. Reactive Exchange (Communication)
Unlike simple "chat" interfaces, agents interact with the OS and each other's terminals.

- **Stimulus (Input):** `forge send <target_pane> "<command>"`
    - Wraps `tmux send-keys`.
    - Example: The Architect runs `forge send implementer "cat docs/specs/auth.md"` to feed context.
- **Sensation (Observation):** `forge read <target_pane>`
    - Wraps `tmux capture-pane`.
    - Example: The Architect runs `forge read implementer` to see if the build failed.
- **Payload (Data):** Shared file system.
    - Large context is exchanged via files (SDD), not chat bubbles.

## Technical Architecture

### Tech Stack
- **tmuxp:** For declarative session management and layout generation.
- **libtmux:** For runtime control (sending commands, capturing output).
- **Python 3.10+:** The host language for the `forge` CLI.

### Workflow: The "Forge Loop"
1.  **Initialization:** `forge init` creates a scaffold `.forge.yaml` based on a selected template (e.g., "Standard Pair", "Mob Programming", "TDD").
2.  **Departure (出陣):** `forge start` spins up the tmux session. Agents are initialized with their specific system prompts/tools.
3.  **Orchestration:**
    - The User (Shogun) acts as the manager, dispatching high-level goals.
    - Agents use `forge` CLI tools to coordinate.
4.  **Termination:** `forge stop` safely shuts down the session, archiving logs.

## Future Roadmap: "Worktree Parallelism"
Inspired by "Practical Parallel Implementation", future versions will support spinning up ephemeral `git worktree` branches for each agent to work on competing implementations simultaneously.