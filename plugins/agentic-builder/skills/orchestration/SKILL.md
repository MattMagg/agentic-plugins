---
name: Multi-Agent Orchestration
description: Workflow patterns for multi-agent systems across frameworks. Directs to RAG for implementation.
---

# Multi-Agent Orchestration Workflow

## Pattern Selection

| Pattern | When to Use | Complexity | RAG Query |
|---------|-------------|------------|-----------|
| **Delegation** | Route to specialists by task type | Low | `"agent delegation routing"` |
| **Sequential** | Pipeline with handoffs | Low | `"sequential agent pipeline"` |
| **Parallel** | Independent concurrent tasks | Medium | `"parallel agent execution"` |
| **Hierarchical** | Manager coordinates workers | Medium | `"hierarchical agent manager"` |
| **Mesh** | Peer-to-peer collaboration | High | `"agent mesh communication"` |

## Framework-Specific Patterns

### ADK Multi-Agent
Uses `sub_agents` for delegation.
**RAG Query**: `mcp__agentic-rag__query_sdk("sub_agents delegation", sdk="adk", mode="build")`

Key: Agent `description` drives routing decisions.

### LangGraph Multi-Agent
Uses graph nodes for each agent, conditional edges for routing.
**RAG Query**: `mcp__agentic-rag__query_sdk("multi-agent graph", sdk="langgraph", mode="build")`

Key: State must flow between agent nodes.

### CrewAI Multi-Agent
Uses Crew with agents and tasks.
**RAG Query**: `mcp__agentic-rag__query_sdk("crew agents tasks", sdk="crewai", mode="build")`

Key: Process type (sequential vs hierarchical) changes everything.

### OpenAI Multi-Agent
Uses handoffs between agents.
**RAG Query**: `mcp__agentic-rag__query_sdk("agent handoff", sdk="openai", mode="build")`

Key: Handoff descriptions determine routing.

## Routing Strategy Decision

| Strategy | Best For | Tradeoff | RAG Query |
|----------|----------|----------|-----------|
| **Keyword** | Simple, predictable tasks | Brittle | `"keyword routing"` |
| **LLM-based** | Complex, nuanced routing | Slower, costlier | `"llm routing classification"` |
| **Semantic** | Similar intent detection | Needs embeddings | `"semantic routing embedding"` |
| **Rule-based** | Deterministic, auditable | Manual maintenance | `"rule based routing"` |

## Critical Gotchas

These cause multi-agent failures:

1. **Vague descriptions** - Agents won't be routed correctly if descriptions are generic
2. **Missing state passing** - Context lost between agents
3. **Circular delegation** - Agent A → B → A infinite loop
4. **No termination condition** - Loops forever
5. **Sequential when could parallel** - Unnecessary latency
6. **No error handling** - One agent failure crashes system

## State Sharing Patterns

| Pattern | When to Use | RAG Query |
|---------|-------------|-----------|
| Shared dict/TypedDict | Simple, synchronous | `"shared state dict"` |
| Message history | Conversational | `"message passing agents"` |
| External store | Persistence needed | `"agent state persistence"` |
| Event bus | Decoupled agents | `"event driven agents"` |

## Workflow: Building Multi-Agent System

### Step 1: Define Agent Responsibilities
Each agent needs:
- Clear, specific role
- Well-defined capabilities
- Distinct from other agents

### Step 2: Choose Orchestration Pattern
Use table above to select pattern based on your workflow.

### Step 3: Design Routing Logic
**RAG Query**: `mcp__agentic-rag__search("[routing strategy] [framework]", mode="build")`

### Step 4: Implement State Sharing
**RAG Query**: `mcp__agentic-rag__search("state sharing [framework]", mode="build")`

### Step 5: Add Termination Conditions
- Max iterations
- Goal achievement check
- Timeout

### Step 6: Error Handling
- Fallback agents
- Retry logic
- Graceful degradation

## Common Error Patterns

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| Wrong agent called | Vague description | Make descriptions specific |
| Infinite loop | No termination | Add max iterations, goal check |
| Context lost | No state passing | Implement state sharing |
| Slow response | Sequential unnecessary | Use parallel where possible |
| One failure crashes all | No error handling | Add try/catch, fallbacks |

## Performance Optimization

| Issue | Solution | RAG Query |
|-------|----------|-----------|
| Latency | Parallel where possible | `"parallel agent optimization"` |
| Token usage | Shorter agent contexts | `"agent context optimization"` |
| Routing errors | Better descriptions | `"agent description best practices"` |
| State bloat | Prune old messages | `"state management cleanup"` |
