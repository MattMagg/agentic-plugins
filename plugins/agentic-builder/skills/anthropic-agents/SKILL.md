---
name: Anthropic Agents
description: Workflow patterns and gotchas for Anthropic/Claude agents. Directs to RAG for implementation.
---

# Anthropic Agents Workflow

## When to Choose Anthropic/Claude

- Building with Claude models
- Need computer use capabilities
- Want extended thinking (deep reasoning)
- Require strong safety/alignment features

## Decision Framework

### Pattern Selection

| Need | Pattern | RAG Query |
|------|---------|-----------|
| Basic tool use | Tool definitions | `"claude tool definition"` |
| Agentic loop | Iterative tool calling | `"claude agentic loop"` |
| Computer control | Computer use | `"claude computer use"` |
| Deep reasoning | Extended thinking | `"claude extended thinking"` |
| Conversation | Message history | `"claude conversation history"` |

**Query RAG**: `mcp__agentic-rag__query_sdk("pattern example", sdk="anthropic", mode="build")`

## Critical Gotchas

These are Claude-specific traps:

1. **Tool schemas are strict** - JSON schema format, not Python type hints
2. **`tool_use` vs `tool_result`** - Tool calls are `tool_use`, responses are `tool_result`
3. **Tool IDs must match** - Response must include the exact `tool_use_id`
4. **ANTHROPIC_API_KEY** - Environment variable name is specific
5. **Max tokens required** - Must specify `max_tokens` in API calls
6. **Stop reason matters** - Check `stop_reason` to know if done or needs tool response
7. **Computer use needs beta header** - Requires `anthropic-beta` header

## Workflow: Building a Claude Agent

### Step 1: SDK Setup
**RAG Query**: `mcp__agentic-rag__query_sdk("anthropic python sdk install", sdk="anthropic", mode="explain")`

### Step 2: Tool Schema Definition
**RAG Query**: `mcp__agentic-rag__query_sdk("tool input_schema definition", sdk="anthropic", mode="build")`

Tools need `name`, `description`, `input_schema` (JSON Schema format).

### Step 3: Message Construction
**RAG Query**: `mcp__agentic-rag__query_sdk("messages create tool_choice", sdk="anthropic", mode="build")`

### Step 4: Tool Response Handling
**RAG Query**: `mcp__agentic-rag__query_sdk("tool_result content block", sdk="anthropic", mode="build")`

Match `tool_use_id` exactly in your response.

### Step 5: Agentic Loop
**RAG Query**: `mcp__agentic-rag__query_sdk("agentic loop stop_reason", sdk="anthropic", mode="build")`

Loop until `stop_reason` is not `tool_use`.

## Common Error Patterns

| Symptom | Likely Cause | RAG Query |
|---------|--------------|-----------|
| Tool not called | Bad schema | `"tool input_schema"` |
| Tool response ignored | Wrong tool_use_id | `"tool_result matching"` |
| Loop never ends | Not checking stop_reason | `"stop_reason end_turn"` |
| Rate limit | Too many requests | `"anthropic rate limits"` |
| Schema validation error | Wrong JSON schema format | `"json schema tool"` |

## Computer Use

Special capability for GUI automation:
**RAG Query**: `mcp__agentic-rag__query_sdk("claude computer use setup", sdk="anthropic", mode="explain")`

Requirements:
- Beta header required
- Screenshot handling needed
- Coordinate system understanding

## Extended Thinking

For complex reasoning tasks:
**RAG Query**: `mcp__agentic-rag__query_sdk("claude extended thinking", sdk="anthropic", mode="explain")`

## Advanced Features

Query RAG when you need:
- Streaming: `"claude streaming response"`
- Vision: `"claude image input"`
- PDF processing: `"claude pdf document"`
- Caching: `"claude prompt caching"`
- Batching: `"anthropic batch api"`
