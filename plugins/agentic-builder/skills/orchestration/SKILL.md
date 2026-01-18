---
name: Multi-Agent Orchestration
description: Patterns for multi-agent systems across frameworks. Use when building agent teams or orchestration.
---

# Multi-Agent Orchestration Patterns

## Orchestration Patterns

| Pattern | Description | Best For |
|---------|-------------|----------|
| **Delegation** | Main agent routes to specialists | Task-based routing |
| **Sequential** | Agents execute in order | Pipelines |
| **Parallel** | Agents execute concurrently | Independent tasks |
| **Hierarchical** | Manager oversees workers | Complex workflows |
| **Mesh** | Agents communicate peer-to-peer | Collaborative tasks |

## Framework Implementations

### ADK Delegation
```python
root_agent = LlmAgent(
    name="coordinator",
    instruction="Route to specialists.",
    sub_agents=[
        researcher,  # Handles research queries
        writer,      # Handles writing tasks
        coder        # Handles coding tasks
    ]
)
```

### LangGraph Multi-Agent
```python
from langgraph.graph import StateGraph

graph = StateGraph(State)
graph.add_node("router", router_node)
graph.add_node("researcher", researcher_node)
graph.add_node("writer", writer_node)

graph.add_conditional_edges("router", route_to_agent)
```

### CrewAI Crew
```python
crew = Crew(
    agents=[researcher, writer, editor],
    tasks=[research_task, writing_task, editing_task],
    process=Process.sequential
)
```

### OpenAI Handoffs
```python
triage = Agent(
    name="triage",
    handoffs=[
        handoff(support, "For support questions"),
        handoff(sales, "For sales inquiries")
    ]
)
```

## Routing Strategies

### Keyword-Based
```python
def route(query: str) -> str:
    if "code" in query.lower():
        return "coder"
    elif "research" in query.lower():
        return "researcher"
    return "default"
```

### LLM-Based
```python
def route(query: str) -> str:
    response = llm.invoke(f"Classify: {query}")
    return response.content  # "coder" | "researcher" | ...
```

### Semantic Similarity
```python
def route(query: str) -> str:
    query_embedding = embed(query)
    # Compare to agent description embeddings
    return most_similar_agent
```

## Common Gotchas

| Issue | Cause | Fix |
|-------|-------|-----|
| Wrong routing | Vague descriptions | Make agent descriptions specific |
| Infinite loops | Circular delegation | Add loop detection |
| Lost context | No state passing | Pass state between agents |
| Slow response | Sequential when could parallel | Use parallel where possible |

## State Sharing Patterns

### Shared Memory
```python
# All agents read/write to shared state
state = {"context": "", "results": []}
```

### Message Passing
```python
# Agents communicate via messages
messages = [
    {"from": "researcher", "content": "..."},
    {"from": "writer", "content": "..."}
]
```

### Event-Based
```python
# Agents emit/listen to events
events.emit("research_complete", data)
events.on("research_complete", writer.process)
```

## When to Use RAG

```python
mcp__agentic-rag__query_docs("multi-agent", frameworks=[fw])
mcp__agentic-rag__search_patterns("delegation", fw)
mcp__agentic-rag__search_patterns("orchestration", fw)
```
