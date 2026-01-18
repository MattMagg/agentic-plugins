---
name: OpenAI Agents
description: Workflow patterns and gotchas for OpenAI Agents SDK. Directs to RAG for implementation.
---

# OpenAI Agents Workflow

## When to Choose OpenAI Agents

- Already using OpenAI API and models
- Need handoff patterns between specialized agents
- Want function calling with type safety
- Building conversational assistants

## Decision Framework

### Architecture Patterns

| Need | Pattern | RAG Query |
|------|---------|-----------|
| Single specialist | Basic Agent | `"Agent basic example"` |
| Route to specialists | Handoffs | `"agent handoff routing"` |
| Sequential steps | Agent chains | `"agent chain pattern"` |
| Persistent context | Memory | `"agent memory conversation"` |
| Background processing | Async runner | `"async agent runner"` |

**Query RAG**: `mcp__agentic-rag__query_code("pattern name", frameworks=["openai"])`

## Critical Gotchas

These cause silent failures or confusion:

1. **Use `@tool` decorator** - Functions without it won't be recognized
2. **Type hints are required** - Parameters need type annotations for schema generation
3. **Docstrings define the schema** - LLM uses docstring for understanding, not just comments
4. **OPENAI_API_KEY env var** - Must be set; SDK doesn't prompt for it
5. **Model names are specific** - `gpt-5.2`, `gpt-5.2-codex` (not `gpt5` or `GPT-5.2`)
6. **Handoff descriptions drive routing** - Vague = poor decisions

## Workflow: Creating an OpenAI Agent

### Step 1: Environment Setup
**RAG Query**: `mcp__agentic-rag__query_docs("openai agents installation", frameworks=["openai"])`

### Step 2: Basic Agent
**RAG Query**: `mcp__agentic-rag__query_code("Agent class definition", frameworks=["openai"])`

### Step 3: Tool Definition
**RAG Query**: `mcp__agentic-rag__query_code("@tool decorator example", frameworks=["openai"])`

Type hints + docstring = working tool.

### Step 4: Running the Agent
**RAG Query**: `mcp__agentic-rag__query_code("Runner execution", frameworks=["openai"])`

### Step 5: Handoffs (if multi-agent)
**RAG Query**: `mcp__agentic-rag__query_code("handoff between agents", frameworks=["openai"])`

### Step 6: Memory (if conversational)
**RAG Query**: `mcp__agentic-rag__query_code("agent memory persistence", frameworks=["openai"])`

## Common Error Patterns

| Symptom | Likely Cause | RAG Query |
|---------|--------------|-----------|
| Tool not found | Missing @tool decorator | `"tool decorator usage"` |
| Schema error | Missing type hints | `"tool type annotations"` |
| API error | Invalid API key | `"openai authentication"` |
| Model error | Wrong model name | `"supported models"` |
| Handoff fails | Bad description | `"handoff description"` |

## Advanced Features

Query RAG when you need:
- Streaming responses: `"streaming agent output"`
- Parallel tool calls: `"parallel tool execution"`
- Custom runners: `"custom Runner implementation"`
- Guardrails: `"agent guardrails safety"`
- Tracing: `"agent tracing debugging"`
