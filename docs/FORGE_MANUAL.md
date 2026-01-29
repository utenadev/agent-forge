# Agent Forge: AI Implementation Manual

This manual is for AI agents working within the **Agent Forge** environment. It describes how to collaborate with other agents and humans using the **Forge Link** protocol.

## 1. Collaboration Philosophy

Agent Forge follows **Specification Driven Development (SDD)**.
- **Single Source of Truth**: Specs (Markdown files) in `docs/` are the authority.
- **Pay-for-Payload**: Large context is exchanged via files, not chat messages.
- **Reactive Exchange**: Use `send` to notify, and `read` to observe.

## 2. Communication Tools

You have two ways to interact with other agents:

### A. Higher-level CLI: `agent-forge`
Use this for session management and formal commands.
- `forge list`: See who is online.
- `forge send <target> "<command>"`: Dispatch a command.
- `forge read <target>`: Check the logs of another agent.

### B. Utility Scripts: `scripts/` (Recommended for Chat)
Use these for informal messaging between agents.
- `./scripts/send.sh <name> "<message>"`: Send a chat message.
- `./scripts/read.sh <name>`: Peek at another agent's recent terminal output.

## 3. Standard Agent Roles

- **The Architect**: Responsible for `docs/specs/*.md`. Defines *what* to build.
- **The Implementer**: Responsible for `agent_forge/*.py`. Defines *how* to build it.
- **The Reviewer**: Responsible for `tests/*.py`. Verifies the implementation.

## 4. Example Interaction Workflow

1.  **Architect** writes `docs/specs/new_feature.md`.
2.  **Architect** notifies Implementer:
    ```bash
    ./scripts/send.sh implementer "Spec for 'new_feature' is ready in docs/specs/. Please start implementation."
    ```
3.  **Implementer** reads the spec, implements code, and then notifies Reviewer:
    ```bash
    ./scripts/send.sh reviewer "Code for 'new_feature' is ready. Please run tests."
    ```
4.  **Reviewer** runs tests, peeks at logs using `./scripts/read.sh implementer`, and provides feedback.

## 5. Handling Errors

If `./scripts/send.sh` fails because a target name is not found, use `forge list` or check the error message output to find the correct pane title. Agent titles may change dynamically (e.g., "Ready (agent-forge)" instead of "gemini").

## 6. Self-Improvement

As an agent, you are encouraged to:
- Update `CLAUDE.md` to reflect the current development state.
- Use `Taskfile` (e.g., `task test`) to maintain quality.
- Write your thoughts in `docs/WorkingLog.md` or a private diary.
