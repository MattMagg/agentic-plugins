---
name: Agent Debugging
description: Systematic debugging patterns for all agentic frameworks. Use when troubleshooting agent issues.
---

# Agent Debugging Patterns

## Diagnostic Categories

| Category | Symptoms | First Checks |
|----------|----------|--------------|
| **IMPORT** | ModuleNotFoundError, ImportError | pip list, import paths |
| **TOOL** | "tool not found", wrong args | docstrings, decorators, registration |
| **AUTH** | 401, 403, "invalid key" | .env, env vars, key format |
| **CONFIG** | "missing config", wrong values | .env format, required fields |
| **RUNTIME** | Unexpected behavior, crashes | logs, state, callbacks |
| **MULTI_AGENT** | Wrong routing, delegation fails | descriptions, agent list |
| **STREAMING** | Connection issues, timeouts | SSE config, network |

## Systematic Debug Process

### 1. Reproduce
```bash
# Run with verbose/debug flags
python agent.py --verbose
ADK: adk web --trace_to_cloud
LangChain: LANGCHAIN_TRACING_V2=true
CrewAI: Agent(verbose=True)
```

### 2. Isolate
- Comment out components one by one
- Test tool functions in isolation
- Check agent without tools first

### 3. Diagnose
- Read error message carefully
- Check framework-specific gotchas
- Query RAG for similar errors

### 4. Fix & Verify
- Make minimal fix
- Run verification command
- Document what worked

## Framework Debug Commands

| Framework | Trace | Log Config |
|-----------|-------|------------|
| ADK | `adk web --trace_to_cloud` | LoggingPlugin |
| OpenAI | `DEBUG=1` env var | logging.basicConfig |
| LangChain | LangSmith | set_debug(True) |
| LangGraph | LangSmith | set_debug(True) |
| CrewAI | `verbose=True` | Agent(verbose=True) |

## Quick Diagnostic Scripts

### Check Imports
```python
frameworks = [
    ("google.adk.agents", "LlmAgent", "ADK"),
    ("agents", "Agent", "OpenAI"),
    ("langchain_core.tools", "tool", "LangChain"),
    ("langgraph.graph", "StateGraph", "LangGraph"),
    ("crewai", "Agent", "CrewAI"),
]
for module, attr, name in frameworks:
    try:
        exec(f"from {module} import {attr}")
        print(f"{name}: OK")
    except ImportError as e:
        print(f"{name}: {e}")
```

### Check Environment
```python
import os
keys = ['GOOGLE_API_KEY', 'OPENAI_API_KEY', 'ANTHROPIC_API_KEY']
for k in keys:
    v = os.environ.get(k)
    print(f"{k}: {'SET' if v else 'NOT SET'}")
```

### Validate Agent
```python
from module import root_agent
print(f"Name: {root_agent.name}")
print(f"Tools: {getattr(root_agent, 'tools', [])}")
```

## Common Fixes by Category

### Import Errors
1. `pip install [package]`
2. Check virtual environment is active
3. Verify import path matches package structure

### Tool Errors
1. Add/fix docstring (most frameworks require it)
2. Add `@tool` decorator if needed
3. Verify tool is in agent's tools list
4. Check parameter types match docstring

### Auth Errors
1. Check .env file exists and is loaded
2. Verify key format (no quotes in .env)
3. Check correct env var name
4. Verify key is valid (not expired)

## When to Use RAG

```python
mcp__agentic-rag__query_docs("error: [message]", frameworks=[detected])
mcp__agentic-rag__query_docs("debugging [framework]", frameworks=[detected])
```
