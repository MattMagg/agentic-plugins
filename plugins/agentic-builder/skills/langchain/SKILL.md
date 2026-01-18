---
name: LangChain
description: Patterns, idioms, and gotchas for LangChain. Use when building LangChain chains and agents.
---

# LangChain Patterns

## Key Idioms

### Tool Definitions
```python
from langchain_core.tools import tool

@tool
def search_tool(query: str) -> str:
    """Search for information.

    Args:
        query: The search query
    """
    return f"Results for {query}"
```

### Chain Composition
```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("human", "{input}")
])

llm = ChatOpenAI(model="gpt-4")
chain = prompt | llm
```

### Agent Creation
```python
from langchain.agents import create_tool_calling_agent, AgentExecutor

agent = create_tool_calling_agent(llm, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools)
```

## Common Gotchas

| Issue | Cause | Fix |
|-------|-------|-----|
| Chain error | Wrong key | Match input/output variable names |
| Tool error | Missing decorator | Add `@tool` decorator |
| Import error | Wrong package | Use `langchain_core`, `langchain_openai` |
| Memory error | Deprecated | Use `langgraph` for stateful agents |

## Quick Patterns

### LCEL Chain
```python
chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)
```

### With Retrieval
```python
from langchain_community.vectorstores import FAISS

vectorstore = FAISS.from_documents(docs, embeddings)
retriever = vectorstore.as_retriever()
```

## When to Use RAG

```python
mcp__agentic-rag__query_docs("topic", frameworks=["langchain"])
mcp__agentic-rag__query_code("pattern", frameworks=["langchain"])
```
