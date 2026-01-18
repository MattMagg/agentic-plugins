#!/usr/bin/env python3
"""
Agentic RAG MCP Server

Exposes the full RAG query interface as Claude Code tools for framework-agnostic
agentic system development.

Based on: /Users/mac-main/rag_qdrant_voyage/docs/rag-query.md

Tools:
- search: Full-featured search with all RAG options
- query_sdk: Simplified SDK-scoped search
- list_frameworks: List available SDKs and corpora
"""

import sys
from typing import Optional, Literal

# Add RAG system to path
RAG_PATH = "/Users/mac-main/rag_qdrant_voyage"
if RAG_PATH not in sys.path:
    sys.path.insert(0, RAG_PATH)

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    print("ERROR: mcp package not installed. Run: pip install mcp", file=sys.stderr)
    sys.exit(1)

try:
    from src.grounding.query.query import search as rag_search, CORPUS_GROUPS, ALL_CORPORA
except ImportError as e:
    print(f"ERROR: Could not import RAG system: {e}", file=sys.stderr)
    print(f"Ensure {RAG_PATH} is accessible and dependencies installed", file=sys.stderr)
    sys.exit(1)

# Create MCP server
mcp = FastMCP("agentic-rag")

# Valid SDK names (maps to CORPUS_GROUPS keys)
VALID_SDKS = ["adk", "openai", "langchain", "langgraph", "anthropic", "crewai", "general"]

# SDK to corpora mapping from docs
SDK_CORPORA = {
    "adk": ["adk_docs", "adk_python"],
    "openai": ["openai_agents_docs", "openai_agents_python"],
    "langchain": ["langgraph_python", "langchain_python", "deepagents_python", "deepagents_docs"],
    "langgraph": ["langgraph_python", "deepagents_python", "deepagents_docs"],
    "anthropic": ["claude_sdk_docs", "claude_sdk_python"],
    "crewai": ["crewai_docs", "crewai_python"],
    "general": ["agent_dev_docs"],
}


def _format_results(result: dict) -> dict:
    """Format RAG search results into structured evidence pack."""
    evidence = []
    for r in result.get("results", []):
        item = {
            "corpus": r.get("corpus"),
            "kind": r.get("kind"),
            "path": r.get("path"),
            "text": r.get("text"),
            "score": r.get("rerank_score", r.get("score", 0)),
        }
        # Include line numbers for code
        if r.get("start_line"):
            item["lines"] = f"{r.get('start_line')}-{r.get('end_line')}"
        evidence.append(item)

    return {
        "query": result.get("query"),
        "count": len(evidence),
        "evidence": evidence,
        "coverage": result.get("coverage", {}),
        "timing": result.get("timing", {}),
    }


@mcp.tool()
def search(
    query: str,
    sdk: Optional[str] = None,
    corpus: Optional[list[str]] = None,
    kind: Optional[Literal["doc", "code"]] = None,
    mode: Literal["build", "debug", "explain", "refactor"] = "build",
    top_k: int = 12,
    multi_query: bool = False,
    expand_context: bool = True,
    expand_top_k: int = 5,
    score_threshold: float = 0.0,
    verbose: bool = False,
) -> dict:
    """
    Full-featured RAG search across agentic framework documentation and code.

    This is the primary search tool with all available options. For simpler
    SDK-scoped queries, use query_sdk instead.

    Args:
        query: Natural language search query
        sdk: SDK group filter. One of: adk, openai, langchain, langgraph,
             anthropic, crewai, general. Limits search to that SDK's corpora.
        corpus: Specific corpus names to search (overrides sdk if provided).
                Valid: adk_docs, adk_python, openai_agents_docs, openai_agents_python,
                langgraph_python, langchain_python, deepagents_python, deepagents_docs,
                claude_sdk_docs, claude_sdk_python, crewai_docs, crewai_python, agent_dev_docs
        kind: Filter by content type: "doc" (documentation) or "code" (source code)
        mode: Retrieval mode affects ranking:
              - "build": Prioritize implementation code (default)
              - "debug": Prioritize error handling, troubleshooting
              - "explain": Prioritize conceptual docs, guides
              - "refactor": Prioritize patterns, best practices
        top_k: Number of results to return (default: 12)
        multi_query: Enable query expansion for better recall (+15%, slower)
        expand_context: Fetch adjacent chunks around results (default: True)
        expand_top_k: Number of top results to expand context for (default: 5)
        score_threshold: Filter results below this relevance score (0 = disabled)
        verbose: Include timing breakdown in response

    Returns:
        Evidence pack with:
        - query: Original query
        - count: Number of results
        - evidence: List of results with corpus, kind, path, text, score, lines
        - coverage: Doc/code balance stats
        - timing: Performance breakdown (if verbose=True)

    Examples:
        # Search ADK for tool creation
        search("how to define function tools", sdk="adk", mode="build")

        # Search all docs for agent patterns
        search("multi-agent orchestration", kind="doc", mode="explain")

        # Debug search with expanded queries
        search("ToolContext error", sdk="adk", mode="debug", multi_query=True)
    """
    filters = {}

    # Apply SDK filter
    if sdk:
        sdk_lower = sdk.lower()
        if sdk_lower in SDK_CORPORA:
            filters["corpus"] = SDK_CORPORA[sdk_lower]

    # Override with specific corpus if provided
    if corpus:
        filters["corpus"] = corpus

    # Apply kind filter
    if kind:
        filters["kind"] = kind

    result = rag_search(
        query=query,
        filters=filters if filters else None,
        top_k=top_k,
        mode=mode,
        multi_query=multi_query,
        expand_context=expand_context,
        expand_top_k=expand_top_k,
        score_threshold=score_threshold,
        verbose=verbose,
    )

    return _format_results(result)


@mcp.tool()
def query_sdk(
    query: str,
    sdk: str,
    top_k: int = 10,
    mode: Literal["build", "debug", "explain", "refactor"] = "build",
) -> dict:
    """
    Simplified SDK-scoped search for quick queries.

    This is a convenience wrapper around search() for common SDK-specific lookups.
    For more control, use search() directly.

    Args:
        query: Natural language search query
        sdk: SDK to search. One of:
             - adk: Google Agent Development Kit
             - openai: OpenAI Agents SDK
             - langchain: LangChain ecosystem (includes LangGraph + DeepAgents)
             - langgraph: LangGraph specifically (includes DeepAgents)
             - anthropic: Anthropic Claude Agent SDK
             - crewai: CrewAI framework
             - general: General agent development docs
        top_k: Number of results (default: 10)
        mode: Retrieval mode - build, debug, explain, or refactor

    Returns:
        Evidence pack with ranked results from the specified SDK.

    SDK Corpora:
        - adk: adk_docs, adk_python
        - openai: openai_agents_docs, openai_agents_python
        - langchain: langgraph_python, langchain_python, deepagents_python, deepagents_docs
        - langgraph: langgraph_python, deepagents_python, deepagents_docs
        - anthropic: claude_sdk_docs, claude_sdk_python
        - crewai: crewai_docs, crewai_python
        - general: agent_dev_docs
    """
    sdk_lower = sdk.lower()
    if sdk_lower not in SDK_CORPORA:
        return {
            "error": f"Invalid SDK '{sdk}'. Valid options: {', '.join(VALID_SDKS)}",
            "valid_sdks": VALID_SDKS,
        }

    return search(
        query=query,
        sdk=sdk_lower,
        top_k=top_k,
        mode=mode,
        expand_context=True,
    )


@mcp.tool()
def list_frameworks() -> dict:
    """
    List available SDKs, their corpora, and search capabilities.

    Use this to understand what frameworks are searchable and what
    corpora are available for each.

    Returns:
        Dictionary with:
        - sdks: List of SDK groups with their corpora
        - all_corpora: Complete list of all available corpora
        - modes: Available retrieval modes and their purposes
        - options: Key search options and defaults
    """
    sdks = []
    for sdk_name in VALID_SDKS:
        corpora = SDK_CORPORA.get(sdk_name, [])
        sdks.append({
            "name": sdk_name,
            "corpora": corpora,
            "doc_corpora": [c for c in corpora if "docs" in c],
            "code_corpora": [c for c in corpora if "python" in c],
        })

    return {
        "sdks": sdks,
        "all_corpora": list(ALL_CORPORA) if hasattr(ALL_CORPORA, '__iter__') else [],
        "modes": {
            "build": "Prioritize implementation code (default)",
            "debug": "Prioritize error handling, troubleshooting",
            "explain": "Prioritize conceptual docs, guides",
            "refactor": "Prioritize patterns, best practices",
        },
        "options": {
            "top_k": "Number of results (default: 12)",
            "multi_query": "Query expansion for +15% recall (default: False)",
            "expand_context": "Fetch adjacent chunks (default: True)",
            "score_threshold": "Filter low-relevance results (default: 0)",
        },
    }


def main():
    """Run the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
