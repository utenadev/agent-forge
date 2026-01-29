# Agent Forge Scripts Manual

This document describes the utility scripts located in `scripts/`.
These scripts act as prototypes for the `forge` CLI commands and are useful for manual interaction between agents (Gemini <-> Claude).

## 1. `send.sh` (Stimulus)

Sends a message to a target pane.
Uses partial matching for the target name (e.g., "claude" matches "✳ Claude Code").
Sender name defaults to `gemini` if not specified via `AGENT_NAME` env var.

**Usage:**
```bash
./scripts/send.sh <target_partial_name> <message>
```

**Example:**
```bash
./scripts/send.sh claude "Please review the latest PR."
```

## 2. `read.sh` (Sensation)

Reads the output (last N lines) of a target pane.
Useful for checking if an agent has finished a task or is waiting for input.

**Usage:**
```bash
./scripts/read.sh <target_partial_name> [lines=20]
```

**Example:**
```bash
# Check the last 50 lines of Claude's output
./scripts/read.sh claude 50
```

## Note for Agents

When you receive a message starting with `gemini: ...`, it was sent using these scripts.
You can use `run_shell_command` to execute these scripts to reply or observe other agents.

**Your Role:**
If you are `claude`, you can reply to `gemini` using:
```bash
./scripts/send.sh gemini "I have received your message."
```
