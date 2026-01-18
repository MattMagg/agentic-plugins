---
name: Agent Debugging
description: Systematic debugging workflow for all agentic frameworks. Directs to RAG for solutions.
---

# Agent Debugging Workflow

## Diagnostic Categories

| Category | Symptoms | First Checks |
|----------|----------|--------------|
| **IMPORT** | ModuleNotFoundError, ImportError | pip list, venv active, import paths |
| **TOOL** | "tool not found", wrong args | docstrings, decorators, registration |
| **AUTH** | 401, 403, "invalid key" | .env exists, env vars set, key format |
| **CONFIG** | "missing config", wrong values | .env format (no quotes!), required fields |
| **RUNTIME** | Unexpected behavior, crashes | logs, state inspection, callbacks |
| **MULTI_AGENT** | Wrong routing, delegation fails | agent descriptions, routing logic |
| **STREAMING** | Connection issues, timeouts | SSE config, network, timeout settings |

## Systematic Debug Process

### Step 1: Reproduce
Enable verbose/trace mode for the framework.
**RAG Query**: `mcp__agentic-rag__search("[framework] debugging tracing", mode="explain")`

### Step 2: Isolate
- Comment out components one by one
- Test tool functions in isolation
- Check agent without tools first
- Test with minimal prompt

### Step 3: Categorize
Match symptoms to category above. This determines the fix strategy.

### Step 4: Diagnose
**RAG Query**: `mcp__agentic-rag__search("error: [error message]", mode="explain")`

Check framework-specific gotchas in the relevant @framework skill.

### Step 5: Fix & Verify
- Make ONE minimal change
- Run verification command
- If fails, revert and try next hypothesis

## Quick Diagnostics

### Import Failures
1. Is virtual environment active?
2. Is package installed? (`pip list | grep [package]`)
3. Is import path correct for version?

**RAG Query**: `mcp__agentic-rag__search("[framework] installation imports", mode="explain")`

### Tool Not Working
1. Does tool have a docstring? (Most frameworks require it)
2. Is decorator applied correctly?
3. Is tool registered with agent?
4. Do parameter types match docstring?

**RAG Query**: `mcp__agentic-rag__search("tool definition", mode="build")`

### Auth Failures
1. Does .env file exist and load?
2. Is key format correct? (NO quotes in .env files)
3. Is env var name correct for framework?
4. Is key valid and not expired?

**RAG Query**: `mcp__agentic-rag__search("[framework] authentication", mode="explain")`

### Wrong Routing (Multi-Agent)
1. Are agent descriptions specific enough?
2. Is routing logic correct?
3. Are all agents registered?

**RAG Query**: `mcp__agentic-rag__search("agent routing delegation", mode="build")`

## Framework Debug Commands

| Framework | How to Enable Tracing | RAG Query |
|-----------|----------------------|-----------|
| ADK | Tracing plugins | `"ADK tracing debugging"` |
| OpenAI | Debug env var | `"openai agents debug"` |
| LangChain | LangSmith / set_debug | `"langchain tracing langsmith"` |
| LangGraph | LangSmith | `"langgraph debugging"` |
| CrewAI | verbose=True | `"crewai verbose debugging"` |
| Anthropic | Logging | `"anthropic logging debug"` |

## Common Fix Patterns

| Problem | Typical Fix |
|---------|-------------|
| Missing module | `pip install [package]` + check venv |
| Tool ignored | Add/fix docstring with Args/Returns |
| Auth failure | Check .env format, no quotes |
| Wrong agent called | Make descriptions more specific |
| State lost | Check state passing between nodes/agents |
| Infinite loop | Add termination condition, max iterations |

## When Nothing Works

1. Strip to minimal reproducer
2. Query RAG with exact error: `mcp__agentic-rag__query_docs("exact error message")`
3. Check framework's GitHub issues
4. Verify you're on supported version
