---
name: LangGraph
description: Workflow patterns and gotchas for LangGraph. Directs to RAG for implementation.
---

# LangGraph Workflow

## When to Choose LangGraph

- Need stateful, cyclic agent workflows
- Building complex multi-step reasoning
- Want conditional branching and loops
- Require human-in-the-loop checkpoints

## Decision Framework

### Graph Pattern Selection

| Need | Pattern | RAG Query |
|------|---------|-----------|
| Sequential steps | Linear graph | `"simple sequential graph"` |
| Decision branching | Conditional edges | `"conditional edge routing"` |
| Iteration/retry | Cycles | `"graph cycle loop"` |
| Parallel execution | Parallel branches | `"parallel graph execution"` |
| Human approval | Checkpoints | `"human in loop checkpoint"` |
| Agent with tools | ReAct pattern | `"react agent langgraph"` |

**Query RAG**: `mcp__agentic-rag__query_code("pattern example", frameworks=["langgraph"])`

## Critical Gotchas

These cause debugging nightmares:

1. **State must be TypedDict** - Not a regular dict; needs type annotations
2. **Node returns partial state** - Return only keys you're updating, not full state
3. **END is special** - Import it: `from langgraph.graph import END`
4. **Edges define flow** - Forgetting an edge = node never reached
5. **Conditional edges return node names** - Return the string name, not the function
6. **Compile before run** - `graph.compile()` is required before invoke
7. **Checkpointer for memory** - Without it, state resets each run
8. **State channels merge** - Multiple updates to same key need reducer

## Workflow: Building a LangGraph Agent

### Step 1: State Definition
**RAG Query**: `mcp__agentic-rag__query_code("TypedDict state definition", frameworks=["langgraph"])`

Define your state schema with TypedDict and Annotated for reducers.

### Step 2: Node Functions
**RAG Query**: `mcp__agentic-rag__query_code("graph node function", frameworks=["langgraph"])`

Each node takes state, returns partial state update.

### Step 3: Graph Construction
**RAG Query**: `mcp__agentic-rag__query_code("StateGraph add_node add_edge", frameworks=["langgraph"])`

### Step 4: Edge Definition
**RAG Query**: `mcp__agentic-rag__query_code("conditional_edges routing", frameworks=["langgraph"])`

### Step 5: Compilation
**RAG Query**: `mcp__agentic-rag__query_code("graph compile checkpointer", frameworks=["langgraph"])`

### Step 6: Execution
**RAG Query**: `mcp__agentic-rag__query_code("compiled graph invoke stream", frameworks=["langgraph"])`

## Common Error Patterns

| Symptom | Likely Cause | RAG Query |
|---------|--------------|-----------|
| Node never runs | Missing edge | `"graph edge definition"` |
| State not updating | Returning wrong keys | `"node state return"` |
| Infinite loop | No END condition | `"conditional edge END"` |
| Type error | State not TypedDict | `"TypedDict state"` |
| Memory lost | No checkpointer | `"MemorySaver persistence"` |
| Merge conflict | Missing reducer | `"Annotated reducer operator"` |

## Graph Patterns

### Decision Tree
Nodes for each decision point, conditional edges for branching.
**RAG Query**: `mcp__agentic-rag__query_code("decision tree graph", frameworks=["langgraph"])`

### ReAct Agent
Reason-Act-Observe loop with tool calling.
**RAG Query**: `mcp__agentic-rag__query_code("react agent pattern", frameworks=["langgraph"])`

### Plan-and-Execute
Planning node, execution loop, verification.
**RAG Query**: `mcp__agentic-rag__query_code("plan execute pattern", frameworks=["langgraph"])`

## Advanced Features

Query RAG when you need:
- Streaming: `"langgraph streaming events"`
- Subgraphs: `"nested subgraph composition"`
- Human-in-loop: `"interrupt checkpoint approval"`
- Time travel: `"state history replay"`
- Parallel branches: `"parallel node execution"`
