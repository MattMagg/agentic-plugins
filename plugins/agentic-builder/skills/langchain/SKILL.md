---
name: LangChain
description: Workflow patterns and gotchas for LangChain. Directs to RAG for implementation.
---

# LangChain Workflow

## When to Choose LangChain

- Need composable chains with many integrations
- Building RAG/retrieval applications
- Want broad LLM provider support
- Need document processing pipelines

## Decision Framework

### Component Selection

| Need | Component | RAG Query |
|------|-----------|-----------|
| Basic LLM call | ChatModel | `"ChatOpenAI initialization"` |
| Prompt templating | PromptTemplate | `"prompt template variables"` |
| Composable steps | LCEL chains | `"LCEL chain composition"` |
| Tool execution | Tool/StructuredTool | `"langchain tool definition"` |
| Document retrieval | Retriever | `"retriever vector store"` |
| Conversation memory | Memory classes | `"conversation buffer memory"` |

**Query RAG**: `mcp__agentic-rag__query_sdk("component example", sdk="langchain", mode="build")`

## Critical Gotchas

These trip up everyone:

1. **LCEL is the pattern** - Use `chain = prompt | llm | parser`, not legacy chains
2. **RunnablePassthrough for context** - Pass data through the chain explicitly
3. **Output parsers matter** - Without one, you get raw text not structured data
4. **Invoke vs stream vs batch** - Different methods for different use cases
5. **Async needs `ainvoke`** - Sync methods block; use async for concurrency
6. **Memory isn't automatic** - You must explicitly add and manage it
7. **API keys via env vars** - Each provider has its own key format

## Workflow: Building a LangChain Application

### Step 1: Dependencies
**RAG Query**: `mcp__agentic-rag__query_sdk("langchain installation packages", sdk="langchain", mode="explain")`

### Step 2: LLM Setup
**RAG Query**: `mcp__agentic-rag__query_sdk("ChatOpenAI ChatAnthropic setup", sdk="langchain", mode="build")`

### Step 3: Prompt Design
**RAG Query**: `mcp__agentic-rag__query_sdk("ChatPromptTemplate messages", sdk="langchain", mode="build")`

### Step 4: Chain Composition
**RAG Query**: `mcp__agentic-rag__query_sdk("LCEL chain pipe operator", sdk="langchain", mode="build")`

### Step 5: Tool Integration (if needed)
**RAG Query**: `mcp__agentic-rag__query_sdk("StructuredTool from_function", sdk="langchain", mode="build")`

### Step 6: Retrieval (if RAG)
**RAG Query**: `mcp__agentic-rag__query_sdk("vector store retriever", sdk="langchain", mode="build")`

## Common Error Patterns

| Symptom | Likely Cause | RAG Query |
|---------|--------------|-----------|
| Chain doesn't work | Wrong pipe order | `"LCEL chain debugging"` |
| Output is raw text | Missing parser | `"output parser structured"` |
| Context lost | Missing passthrough | `"RunnablePassthrough"` |
| Async timeout | Using sync method | `"langchain async ainvoke"` |
| Memory not working | Not connected | `"memory chain integration"` |

## LangChain vs LangGraph

| Use Case | Choose |
|----------|--------|
| Linear pipelines | LangChain LCEL |
| Conditional branching | LangGraph |
| Cycles/loops | LangGraph |
| Simple retrieval | LangChain |
| Complex agent workflows | LangGraph |

## Advanced Features

Query RAG when you need:
- Streaming: `"langchain streaming callback"`
- Callbacks/tracing: `"langchain callbacks tracing"`
- Custom chains: `"custom runnable class"`
- Caching: `"langchain caching responses"`
- Fallbacks: `"chain fallback retry"`
