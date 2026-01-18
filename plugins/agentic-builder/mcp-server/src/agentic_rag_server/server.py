#!/usr/bin/env python3
"""
Agentic RAG MCP Server

Exposes RAG query interface as Claude Code tools for framework-agnostic
agentic system development.

Tools:
- query_docs: Search documentation across frameworks
- query_code: Search code examples across frameworks
- search_patterns: Find implementation patterns
- list_frameworks: List available frameworks with corpus stats
"""

import sys
from typing import Optional

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
    from src.grounding.query.query import search, CORPUS_GROUPS, ALL_CORPORA
except ImportError as e:
    print(f"ERROR: Could not import RAG system: {e}", file=sys.stderr)
    print(f"Ensure {RAG_PATH} is accessible and dependencies installed", file=sys.stderr)
    sys.exit(1)

# Create MCP server
mcp = FastMCP("agentic-rag")

# SDK name to CORPUS_GROUPS key mapping
SDK_MAPPING = {
    "adk": "adk",
    "openai": "openai",
    "langchain": "langchain",
    "langgraph": "langgraph",
    "anthropic": "anthropic",
    "crewai": "crewai",
    "general": "general",
}


def _get_corpora_for_frameworks(frameworks: list[str], kind: str = "all") -> list[str]:
    """
    Get corpus names for given frameworks filtered by kind.

    Args:
        frameworks: List of framework names (adk, openai, etc.)
        kind: Filter by "doc", "code", or "all"

    Returns:
        List of corpus names
    """
    corpora = []
    for fw in frameworks:
        sdk = SDK_MAPPING.get(fw.lower())
        if sdk and sdk in CORPUS_GROUPS:
            for corpus in CORPUS_GROUPS[sdk]:
                if kind == "all":
                    corpora.append(corpus)
                elif kind == "doc" and ("docs" in corpus or corpus.endswith("_docs")):
                    corpora.append(corpus)
                elif kind == "code" and ("python" in corpus):
                    corpora.append(corpus)
    return corpora


def _format_results(result: dict) -> dict:
    """Format RAG search results into structured evidence pack."""
    evidence = []
    for r in result.get("results", []):
        evidence.append({
            "corpus": r.get("corpus"),
            "kind": r.get("kind"),
            "path": r.get("path"),
            "text": r.get("text"),
            "score": r.get("rerank_score", r.get("score", 0)),
            "lines": f"{r.get('start_line', '')}-{r.get('end_line', '')}" if r.get("start_line") else None,
        })

    return {
        "query": result.get("query"),
        "count": len(evidence),
        "evidence": evidence,
        "coverage": result.get("coverage", {}),
    }


@mcp.tool()
def query_docs(
    query: str,
    frameworks: Optional[list[str]] = None,
    top_k: int = 8,
) -> dict:
    """
    Search documentation across agentic frameworks.

    Use this to find explanations, guides, API references, and conceptual
    documentation about agent development.

    Args:
        query: Natural language search query (e.g., "how to create tools in ADK")
        frameworks: List of framework names to search (adk, openai, langchain,
                   langgraph, anthropic, crewai). If None, searches all.
        top_k: Number of results to return (default: 8)

    Returns:
        Evidence pack with ranked documentation results including corpus,
        file path, text content, and relevance score.
    """
    filters = {"kind": "doc"}

    if frameworks:
        corpora = _get_corpora_for_frameworks(frameworks, kind="doc")
        if corpora:
            filters["corpus"] = corpora

    result = search(
        query=query,
        filters=filters,
        top_k=top_k,
        mode="explain",
        verbose=False,
    )

    return _format_results(result)


@mcp.tool()
def query_code(
    query: str,
    frameworks: Optional[list[str]] = None,
    top_k: int = 8,
) -> dict:
    """
    Search source code examples across agentic frameworks.

    Use this to find implementation examples, code patterns, and working
    code snippets for agent development.

    Args:
        query: Natural language search query (e.g., "LlmAgent with callbacks")
        frameworks: List of framework names to search (adk, openai, langchain,
                   langgraph, anthropic, crewai). If None, searches all.
        top_k: Number of results to return (default: 8)

    Returns:
        Evidence pack with ranked code examples including corpus,
        file path, code content, line numbers, and relevance score.
    """
    filters = {"kind": "code"}

    if frameworks:
        corpora = _get_corpora_for_frameworks(frameworks, kind="code")
        if corpora:
            filters["corpus"] = corpora

    result = search(
        query=query,
        filters=filters,
        top_k=top_k,
        mode="build",
        verbose=False,
    )

    return _format_results(result)


@mcp.tool()
def search_patterns(
    pattern_type: str,
    framework: str,
    top_k: int = 5,
) -> dict:
    """
    Search for specific implementation patterns in a framework.

    Use this to find canonical examples of common patterns like tool
    definitions, agent creation, callbacks, multi-agent setups, etc.

    Args:
        pattern_type: Type of pattern to find. Examples:
            - "tool_definition" - How to define tools/functions
            - "agent_creation" - How to create agents
            - "callbacks" - Lifecycle callbacks and hooks
            - "multi_agent" - Multi-agent orchestration
            - "memory" - State and memory management
            - "streaming" - Streaming responses
        framework: Target framework (adk, openai, langchain, langgraph,
                  anthropic, crewai)
        top_k: Number of results (default: 5)

    Returns:
        Evidence pack with annotated code patterns and context.
    """
    query = f"{pattern_type} implementation example"

    sdk = SDK_MAPPING.get(framework.lower())
    filters = {}
    if sdk and sdk in CORPUS_GROUPS:
        filters["corpus"] = CORPUS_GROUPS[sdk]

    result = search(
        query=query,
        filters=filters,
        top_k=top_k,
        mode="build",
        verbose=False,
    )

    return _format_results(result)


@mcp.tool()
def list_frameworks() -> dict:
    """
    List available frameworks and their corpus statistics.

    Use this to see what frameworks are available for querying and
    understand the scope of documentation and code coverage.

    Returns:
        Dictionary with framework information including:
        - name: Framework identifier
        - sdk: SDK group key
        - corpora: All corpus names for this framework
        - doc_corpora: Documentation corpora
        - code_corpora: Code/source corpora
    """
    frameworks = []
    for name, sdk in SDK_MAPPING.items():
        if sdk in CORPUS_GROUPS:
            corpora = CORPUS_GROUPS[sdk]
            frameworks.append({
                "name": name,
                "sdk": sdk,
                "corpora": corpora,
                "doc_corpora": [c for c in corpora if "docs" in c or c.endswith("_docs")],
                "code_corpora": [c for c in corpora if "python" in c],
            })

    return {
        "frameworks": frameworks,
        "all_corpora": ALL_CORPORA,
        "total_corpora": len(ALL_CORPORA),
    }


def main():
    """Run the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
