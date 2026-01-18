---
name: CrewAI
description: Workflow patterns and gotchas for CrewAI. Directs to RAG for implementation.
---

# CrewAI Workflow

## When to Choose CrewAI

- Building role-based multi-agent systems
- Need agents with distinct personas
- Want task delegation patterns
- Building "crew" style collaboration

## Decision Framework

### Component Selection

| Need | Component | RAG Query |
|------|-----------|-----------|
| Define specialist | Agent | `"crewai agent role goal"` |
| Define work unit | Task | `"crewai task description"` |
| Coordinate agents | Crew | `"crew process sequential"` |
| Custom capabilities | Tool | `"crewai custom tool"` |
| Structured output | Output schemas | `"crewai output pydantic"` |

**Query RAG**: `mcp__agentic-rag__query_code("component example", frameworks=["crewai"])`

## Critical Gotchas

These define CrewAI success:

1. **Role/Goal/Backstory triad** - All three shape agent behavior significantly
2. **Task descriptions are prompts** - Vague descriptions = vague results
3. **Expected output matters** - Specify format explicitly or get random structure
4. **Process type affects flow** - `sequential` vs `hierarchical` changes everything
5. **Tool names must be clear** - Agent reads tool name to decide usage
6. **Delegation can loop** - Agents may delegate back and forth infinitely
7. **Memory is per-crew** - Not shared across different crew instances

## Workflow: Building a CrewAI System

### Step 1: Define Agents
**RAG Query**: `mcp__agentic-rag__query_code("Agent role goal backstory", frameworks=["crewai"])`

Each agent needs a clear role, specific goal, and relevant backstory.

### Step 2: Create Tools
**RAG Query**: `mcp__agentic-rag__query_code("crewai tool decorator", frameworks=["crewai"])`

### Step 3: Define Tasks
**RAG Query**: `mcp__agentic-rag__query_code("Task description expected_output", frameworks=["crewai"])`

Tasks must specify: description, expected_output, assigned agent.

### Step 4: Assemble Crew
**RAG Query**: `mcp__agentic-rag__query_code("Crew agents tasks process", frameworks=["crewai"])`

### Step 5: Execute
**RAG Query**: `mcp__agentic-rag__query_code("crew kickoff inputs", frameworks=["crewai"])`

## Common Error Patterns

| Symptom | Likely Cause | RAG Query |
|---------|--------------|-----------|
| Agent off-topic | Bad role/goal | `"agent role definition"` |
| Wrong output format | Missing expected_output | `"task expected_output"` |
| Infinite delegation | Allow_delegation loop | `"delegation control"` |
| Tool not used | Unclear tool name | `"tool naming crewai"` |
| Tasks out of order | Wrong process type | `"sequential hierarchical"` |

## Process Types

| Type | When to Use | RAG Query |
|------|-------------|-----------|
| Sequential | Tasks depend on previous output | `"sequential process"` |
| Hierarchical | Manager delegates to workers | `"hierarchical manager"` |

## Crew Patterns

### Research Crew
Researcher → Analyst → Writer pipeline.
**RAG Query**: `mcp__agentic-rag__query_code("research crew example", frameworks=["crewai"])`

### Support Crew
Triage → Specialist routing.
**RAG Query**: `mcp__agentic-rag__query_code("support crew routing", frameworks=["crewai"])`

## Advanced Features

Query RAG when you need:
- Memory: `"crewai memory persistence"`
- Callbacks: `"crewai task callbacks"`
- Async execution: `"crewai async kickoff"`
- Custom LLM: `"crewai custom llm"`
- Output validation: `"crewai pydantic output"`
