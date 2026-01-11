---
name: ADK Behavior
description: This skill should be used when the user asks about "callbacks", "lifecycle hooks", "before_model_call", "after_tool_call", "plugins", "session state", "state management", "artifacts", "file uploads", "events", "EventActions", "human-in-the-loop", "confirmation", "memory", "MemoryService", "long-term memory", "remember across sessions", "RAG", "retrieval augmented generation", "grounding", "knowledge base", "vector search", or needs guidance on customizing agent behavior, intercepting execution, managing state across turns, implementing approval workflows, or implementing persistent memory or grounding agent responses in external knowledge.
version: 2.1.0
---

# ADK Behavior & Memory

Guide for customizing agent behavior through callbacks, state, artifacts, events, memory, and grounding. Enables interception of execution, state persistence (session and long-term), human-in-the-loop workflows, and knowledge grounding.

## When to Use

- Intercepting LLM calls or tool executions
- Persisting data across conversation turns (session state)
- Persisting memories across conversations (MemoryService)
- Implementing human approval workflows
- Handling file uploads and artifacts
- Customizing event flow control
- Grounding responses in knowledge bases (RAG)
- Building agents that learn user preferences
- Connecting to Vertex AI Search datastores

## When NOT to Use

- Creating agents from scratch → Use `@adk-core` instead
- Adding tools → Use `@adk-tools` instead
- Multi-agent orchestration → Use `@adk-multi-agent` instead

## Key Concepts

### Behavior Customization

**Callbacks** intercept lifecycle events: `before_model_callback`, `after_model_callback`, `before_tool_callback`, `after_tool_callback`. Return content to override default behavior.

**Session State** persists data across conversation turns via `ctx.state`. Access with `get()` and update with dictionary assignment.

**Plugins** bundle reusable callbacks. Create custom plugins for logging, security, or monitoring.

**Artifacts** handle binary data and file uploads. Store files via artifact service for multi-turn access.

**EventActions** control flow: skip steps, escalate to parent, terminate session.

**Human-in-the-Loop** requires confirmation before sensitive actions by returning confirmation prompts from callbacks.

### Memory & Grounding

**Session State** persists within a conversation but is lost when session ends. Use `ctx.state` for temporary data.

**MemoryService** provides long-term memory across sessions. Agents can remember facts, preferences, and context over time.

**Grounding (RAG)** connects agents to external knowledge bases. Use Vertex AI Search or custom vector stores to retrieve relevant context before responding.

**Knowledge Attribution** enables agents to cite sources when grounding responses, improving transparency and trust.

## References

Detailed guides with code examples:

### Behavior Customization
- `references/callbacks.md` - Lifecycle callback patterns
- `references/plugins.md` - Reusable callback bundles
- `references/state.md` - Session state management
- `references/artifacts.md` - File/binary handling
- `references/events.md` - EventActions and flow control
- `references/confirmation.md` - Human-in-the-loop patterns

### Memory & Grounding
- `references/memory-service.md` - Long-term memory patterns
- `references/grounding.md` - RAG and knowledge grounding
