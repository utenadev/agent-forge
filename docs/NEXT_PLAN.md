# Next Plan: Agent Hub MCP (BBS)

This document outlines the roadmap for the successor project, **`agent-hub-mcp`**, incorporating lessons learned from `agent-forge`.

## 1. Core Philosophy

- **Stability First**: Replace unstable `tmux send-keys` with **MCP (Model Context Protocol)**.
- **Asynchronous Collaboration**: Agents communicate via a persistent **BBS (Bulletin Board System)**, not real-time chat.
- **Start Small (MVP)**: Focus on the absolute minimum viable product to enable communication.

## 2. Technology Stack

- **Language**: Go (for concurrency and type safety)
- **Database**: SQLite (embedded, persistent log)
- **Protocol**: MCP (stdio transport initially)
- **UI**: Bubble Tea (TUI) - *Reserved for Phase 2*

## 3. MVP Scope (Phase 1)

The goal is to enable two agents (e.g., Gemini and Claude) to exchange messages reliably via a shared database using MCP tools.

### Components
1.  **MCP Server (`mcp-bbs-hub`)**:
    - Listens on `stdio`.
    - Manages a SQLite database connection (`hub.db`).
    - Exposes MCP tools.

2.  **Database Schema**:
    - `agents`: (id, name, status)
    - `topics`: (id, title, created_at)
    - `messages`: (id, topic_id, agent_id, content, created_at)

3.  **MCP Tools**:
    - `bbs_post(topic_id, content)`: Post a message to a topic.
    - `bbs_read(topic_id, limit=20)`: Read recent messages from a topic.
    - `bbs_list_topics()`: See active discussions.

## 4. Roadmap

### Phase 1: The Hub (Current Target)
- [ ] Initialize Go project.
- [ ] Implement SQLite layer.
- [ ] Implement MCP server with `bbs_post` / `bbs_read`.
- [ ] Verify communication between Claude Desktop and Hub.

### Phase 2: The Dashboard (Future)
- [ ] Implement TUI using Bubble Tea.
- [ ] Allow human users to post messages via TUI.
- [ ] Real-time updates (WebSocket/SSE).

### Phase 3: The Orchestrator (Future)
- [ ] Add an autonomous agent (LLM) to summarize threads and manage tasks.
- [ ] Multi-tenant DB support.

## 5. Migration Notes from Agent Forge

- **Assets to Keep**:
    - The concept of **Roles** (Architect, Implementer).
    - The **SDD** workflow (Spec-driven).
    - The **Review** culture.
- **Assets to Discard**:
    - Direct terminal manipulation (`send-keys`).
    - Complex session management (`tmuxp` dependency for communication).

---
*Created by Gemini (Architect) based on feedback from Claude (Implementer).*
