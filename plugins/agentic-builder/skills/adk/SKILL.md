---
name: Google ADK
description: Workflow patterns and gotchas for Google Agent Development Kit. Directs to RAG for implementation.
---

# Google ADK Workflow

## When to Choose ADK

- Building for Google Cloud / Vertex AI deployment
- Need streaming-first architecture
- Want agent-to-agent (A2A) protocol support
- Gemini model preference

## Decision Framework

### Agent Type Selection

| Need | Agent Type | RAG Query |
|------|------------|-----------|
| LLM reasoning with tools | `LlmAgent` | `"LlmAgent configuration"` |
| Custom non-LLM logic | `BaseAgent` | `"BaseAgent implementation"` |
| Sequential pipeline | `SequentialAgent` | `"SequentialAgent example"` |
| Parallel execution | `ParallelAgent` | `"ParallelAgent concurrent"` |
| Iteration patterns | `LoopAgent` | `"LoopAgent termination"` |

**Query RAG**: `mcp__agentic-rag__query_code("agent type example", frameworks=["adk"])`

## Critical Gotchas

These are NOT in docs or easy to discover:

1. **Export as `root_agent`** - ADK expects this exact name in `agent.py`
2. **Docstrings are MANDATORY for tools** - LLM reads them; missing = tool won't work
3. **NEVER document ToolContext** - It's auto-injected; including it in docstring breaks inference
4. **No quotes in .env** - `GOOGLE_API_KEY=value` not `GOOGLE_API_KEY="value"`
5. **Sub-agent descriptions matter** - Vague descriptions = poor routing decisions

## Workflow: Creating an ADK Agent

### Step 1: Project Setup
**RAG Query**: `mcp__agentic-rag__query_docs("ADK project structure", frameworks=["adk"])`

### Step 2: Agent Definition
**RAG Query**: `mcp__agentic-rag__query_code("LlmAgent basic example", frameworks=["adk"])`

### Step 3: Tool Creation
**RAG Query**: `mcp__agentic-rag__query_code("function tool definition", frameworks=["adk"])`

Remember: Every tool needs a docstring with Args and Returns.

### Step 4: State Management (if needed)
**RAG Query**: `mcp__agentic-rag__query_code("agent state management", frameworks=["adk"])`

### Step 5: Multi-Agent (if needed)
**RAG Query**: `mcp__agentic-rag__query_code("sub_agents routing", frameworks=["adk"])`

### Step 6: Testing
**RAG Query**: `mcp__agentic-rag__query_docs("ADK testing", frameworks=["adk"])`

## Common Error Patterns

| Symptom | Likely Cause | RAG Query |
|---------|--------------|-----------|
| Tool not invoked | Missing/bad docstring | `"tool docstring format"` |
| Import error | Wrong module path | `"ADK imports"` |
| Auth failure | .env formatting | `"ADK authentication"` |
| Sub-agent ignored | Poor description | `"sub_agents description"` |
| State not persisting | Wrong state access | `"ToolContext state"` |

## Advanced Features

Query RAG when you need:
- Streaming: `"ADK streaming response"`
- A2A Protocol: `"agent to agent protocol"`
- Visual Builder: `"ADK visual builder"`
- Callbacks: `"ADK callbacks events"`
- Memory/Sessions: `"ADK session memory"`
