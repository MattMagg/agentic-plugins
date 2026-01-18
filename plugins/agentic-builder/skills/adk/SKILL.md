---
name: Google ADK
description: Patterns, idioms, and gotchas for Google Agent Development Kit. Use when building ADK agents.
---

# Google ADK Patterns

## Key Idioms

### Agent Naming
- Export as `root_agent` in `agent.py` - this is the convention ADK expects
- Use descriptive `name` for logging and debugging

### Agent Types
| Type | Use When |
|------|----------|
| `LlmAgent` | LLM reasoning, conversation, tool use (most common) |
| `BaseAgent` | Custom non-LLM logic, extend and implement `run_async()` |
| `SequentialAgent` | Execute steps in order |
| `ParallelAgent` | Execute steps concurrently |
| `LoopAgent` | Repeat until condition |

### Tool Definitions

**Docstrings are MANDATORY** - the LLM reads them to understand tools:

```python
def my_tool(query: str) -> str:
    """Short description shown to LLM.

    Args:
        query: Description of the parameter

    Returns:
        Description of return value
    """
    return result
```

### ToolContext

`ToolContext` is auto-injected - **NEVER document it**:

```python
from google.adk.tools import ToolContext

def my_tool(query: str, tool_context: ToolContext) -> dict:
    # tool_context NOT in docstring - it's auto-injected
    user = tool_context.state.get("user")
    return {"result": query, "user": user}
```

## Common Gotchas

| Issue | Cause | Fix |
|-------|-------|-----|
| Tool not working | Missing docstring | Add docstring with Args/Returns |
| ToolContext error | In docstring | Remove from docstring |
| Import error | Wrong path | `from google.adk.agents import LlmAgent` |
| Auth error | .env format | `GOOGLE_API_KEY=value` (no quotes!) |
| Sub-agent not called | Bad description | Make description specific for routing |

## Quick Patterns

### Basic Agent
```python
from google.adk.agents import LlmAgent

root_agent = LlmAgent(
    name="my_agent",
    model="gemini-2.0-flash",
    instruction="You are a helpful assistant.",
    tools=[my_tool]
)
```

### With Sub-agents
```python
root_agent = LlmAgent(
    name="coordinator",
    model="gemini-2.0-flash",
    instruction="Route to specialists based on query type.",
    sub_agents=[support_agent, sales_agent]
)
```

### With State
```python
root_agent = LlmAgent(
    name="stateful_agent",
    model="gemini-2.0-flash",
    instruction="Track user preferences.",
    state={"user_name": None, "preferences": {}}
)
```

## When to Use RAG

Query RAG for:
- Full API documentation
- Complex configuration options
- Advanced features (streaming, A2A, visual builder)

```python
mcp__agentic-rag__query_docs("topic", frameworks=["adk"])
mcp__agentic-rag__query_code("pattern", frameworks=["adk"])
```
