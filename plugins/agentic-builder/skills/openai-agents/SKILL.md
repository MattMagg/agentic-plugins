---
name: OpenAI Agents
description: Patterns, idioms, and gotchas for OpenAI Agents SDK. Use when building OpenAI agents.
---

# OpenAI Agents Patterns

## Key Idioms

### Agent Creation
```python
from agents import Agent, tool

agent = Agent(
    name="my_agent",
    model="gpt-4",
    instructions="You are a helpful assistant.",
    tools=[my_tool]
)
```

### Tool Definitions

Use the `@tool` decorator:

```python
from agents import tool

@tool
def search_web(query: str) -> str:
    """Search the web for information.

    Args:
        query: The search query

    Returns:
        Search results as text
    """
    return f"Results for: {query}"
```

### Running Agents

```python
from agents import Runner

runner = Runner()
result = runner.run(agent, "Hello, how are you?")
print(result.final_output)
```

## Common Gotchas

| Issue | Cause | Fix |
|-------|-------|-----|
| Tool not found | Missing `@tool` decorator | Add decorator |
| API error | Wrong key | Check `OPENAI_API_KEY` |
| Model error | Invalid name | Use `gpt-4`, `gpt-4-turbo`, `gpt-3.5-turbo` |
| Import error | Wrong package | `pip install openai-agents` |

## Quick Patterns

### With Handoffs
```python
from agents import Agent, handoff

support_agent = Agent(name="support", ...)
sales_agent = Agent(name="sales", ...)

triage_agent = Agent(
    name="triage",
    handoffs=[
        handoff(support_agent, "Route support questions here"),
        handoff(sales_agent, "Route sales inquiries here")
    ]
)
```

### With Memory
```python
from agents import Agent
from agents.memory import Memory

agent = Agent(
    name="memory_agent",
    memory=Memory()
)
```

## When to Use RAG

```python
mcp__agentic-rag__query_docs("topic", frameworks=["openai"])
mcp__agentic-rag__query_code("pattern", frameworks=["openai"])
```
