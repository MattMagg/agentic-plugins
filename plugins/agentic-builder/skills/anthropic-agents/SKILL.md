---
name: Anthropic Agents
description: Patterns, idioms, and gotchas for Anthropic/Claude Agent SDK. Use when building Claude-native agents.
---

# Anthropic Agents Patterns

## Key Idioms

### Tool Definitions
```python
import anthropic

tools = [
    {
        "name": "search",
        "description": "Search for information",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query"}
            },
            "required": ["query"]
        }
    }
]
```

### Using Tools with Claude
```python
client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    tools=tools,
    messages=[{"role": "user", "content": "Search for Python tutorials"}]
)
```

### Handling Tool Use
```python
for block in response.content:
    if block.type == "tool_use":
        tool_name = block.name
        tool_input = block.input
        # Execute tool and continue conversation
```

## Common Gotchas

| Issue | Cause | Fix |
|-------|-------|-----|
| Tool not called | Bad description | Make description clear and specific |
| Schema error | Invalid JSON schema | Validate input_schema format |
| Rate limit | Too many requests | Add retry with backoff |
| Model error | Wrong name | Use `claude-sonnet-4-20250514`, `claude-opus-4-20250514` |

## Quick Patterns

### Agentic Loop
```python
while True:
    response = client.messages.create(...)

    if response.stop_reason == "end_turn":
        break

    for block in response.content:
        if block.type == "tool_use":
            result = execute_tool(block.name, block.input)
            messages.append({"role": "user", "content": [
                {"type": "tool_result", "tool_use_id": block.id, "content": result}
            ]})
```

### With Computer Use
```python
tools = [
    {"type": "computer_20241022", "name": "computer", "display_width_px": 1024, "display_height_px": 768},
    {"type": "text_editor_20241022", "name": "str_replace_editor"},
    {"type": "bash_20241022", "name": "bash"}
]
```

## When to Use RAG

```python
mcp__agentic-rag__query_docs("topic", frameworks=["anthropic"])
mcp__agentic-rag__query_code("pattern", frameworks=["anthropic"])
```
