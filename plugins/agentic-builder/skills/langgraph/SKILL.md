---
name: LangGraph
description: Patterns, idioms, and gotchas for LangGraph. Use when building graph-based agents.
---

# LangGraph Patterns

## Key Idioms

### State Definition
```python
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages

class State(TypedDict):
    messages: Annotated[list, add_messages]
    context: str
```

### Graph Construction
```python
from langgraph.graph import StateGraph, START, END

graph = StateGraph(State)
graph.add_node("agent", agent_node)
graph.add_node("tools", tool_node)

graph.add_edge(START, "agent")
graph.add_conditional_edges("agent", should_continue)
graph.add_edge("tools", "agent")
```

### Node Functions
```python
def agent_node(state: State) -> dict:
    response = llm.invoke(state["messages"])
    return {"messages": [response]}
```

## Common Gotchas

| Issue | Cause | Fix |
|-------|-------|-----|
| State not updating | Wrong return type | Return dict with state keys |
| Infinite loop | Bad condition | Check `should_continue` logic |
| Missing edge | Forgot START/END | Add all required edges |
| Type error | Wrong annotation | Use `Annotated[list, add_messages]` |

## Quick Patterns

### Conditional Routing
```python
def should_continue(state: State) -> str:
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tools"
    return END
```

### With Memory
```python
from langgraph.checkpoint.memory import MemorySaver

checkpointer = MemorySaver()
app = graph.compile(checkpointer=checkpointer)

# Invoke with thread_id for persistence
result = app.invoke(input, config={"configurable": {"thread_id": "1"}})
```

### Human-in-the-Loop
```python
graph.add_node("human", human_node)
graph.add_edge("agent", "human")
# Human node waits for input
```

## When to Use RAG

```python
mcp__agentic-rag__query_docs("topic", frameworks=["langgraph"])
mcp__agentic-rag__query_code("pattern", frameworks=["langgraph"])
```
