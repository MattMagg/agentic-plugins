---
name: CrewAI
description: Patterns, idioms, and gotchas for CrewAI. Use when building multi-agent crews.
---

# CrewAI Patterns

## Key Idioms

### Agent Definition
```python
from crewai import Agent

researcher = Agent(
    role="Research Analyst",
    goal="Find and analyze information",
    backstory="You are an expert researcher with years of experience.",
    tools=[search_tool],
    verbose=True
)
```

### Task Definition
```python
from crewai import Task

research_task = Task(
    description="Research the topic: {topic}",
    expected_output="A comprehensive research report",
    agent=researcher
)
```

### Crew Assembly
```python
from crewai import Crew, Process

crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, writing_task],
    process=Process.sequential,
    verbose=True
)

result = crew.kickoff(inputs={"topic": "AI agents"})
```

## Common Gotchas

| Issue | Cause | Fix |
|-------|-------|-----|
| Agent not working | Missing fields | Include role, goal, backstory |
| Task error | No agent | Assign agent to task |
| Crew error | Circular dependency | Check task order |
| Tool error | Wrong format | Use CrewAI tool decorators |

## Quick Patterns

### Tool Creation
```python
from crewai.tools import tool

@tool
def search_tool(query: str) -> str:
    """Search the web for information."""
    return f"Results for: {query}"
```

### Hierarchical Process
```python
crew = Crew(
    agents=[manager, researcher, writer],
    tasks=[research_task, writing_task],
    process=Process.hierarchical,
    manager_agent=manager
)
```

### With Memory
```python
crew = Crew(
    agents=[...],
    tasks=[...],
    memory=True,
    embedder={
        "provider": "openai",
        "config": {"model": "text-embedding-3-small"}
    }
)
```

## When to Use RAG

```python
mcp__agentic-rag__query_docs("topic", frameworks=["crewai"])
mcp__agentic-rag__query_code("pattern", frameworks=["crewai"])
```
