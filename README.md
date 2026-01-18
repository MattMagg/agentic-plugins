# Agentic Plugins

Claude Code plugins for building AI agents across frameworks.

## Installation

Add this marketplace:
```bash
/plugin marketplace add MattMagg/agentic-plugins
```

Then install plugins:
```bash
/plugin install <plugin-name>@agentic-plugins
```

## Available Plugins

| Plugin | Framework | Description |
|--------|-----------|-------------|
| [adk-builder](./plugins/adk-builder) | Google ADK | Specialized ADK development with spec-driven workflows |
| [agentic-builder](./plugins/agentic-builder) | Multi-framework | Framework-agnostic builder with RAG-grounded knowledge |

### agentic-builder

Supports 6 frameworks with RAG-powered documentation access:
- Google ADK
- OpenAI Agents SDK
- LangChain
- LangGraph
- Anthropic Agents SDK
- CrewAI

Features:
- Auto-detects framework from project code
- Adaptive workflow: SPEC → PLAN → BUILD → DEBUG
- MCP server for RAG queries against framework documentation
- Session hooks for context persistence

## Contributing

To add a plugin:

1. Create a folder: `plugins/your-plugin/`
2. Add `.claude-plugin/plugin.json` inside it
3. Add your agents, skills, commands
4. Update `.claude-plugin/marketplace.json` to include your plugin
5. Submit a PR
