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
| [adk-builder](./plugins/adk-builder) | Google ADK | Autonomous development with planning, coding, debugging agents |

## Plugin Roadmap

- **openai-agents** - OpenAI Agents SDK
- *more to come*

## Contributing

To add a plugin:

1. Create a folder: `plugins/your-plugin/`
2. Add `.claude-plugin/plugin.json` inside it
3. Add your agents, skills, commands
4. Update `.claude-plugin/marketplace.json` to include your plugin
5. Submit a PR
