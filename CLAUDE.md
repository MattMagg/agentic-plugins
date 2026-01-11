# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a Claude Code plugin marketplace for agentic development frameworks. Currently contains the `adk-builder` plugin for Google Agent Development Kit (ADK). The marketplace will expand to support other frameworks (OpenAI Agents SDK, etc.).

## Architecture

### Marketplace Structure

```
agentic-plugins/
├── .claude-plugin/
│   └── marketplace.json      # Plugin registry
└── plugins/
    └── adk-builder/
        ├── .claude-plugin/
        │   └── plugin.json   # Plugin manifest
        └── commands/         # Slash commands (declared in manifest)
```

### Plugin Manifest

Per official docs, valid `plugin.json` fields:
- **Metadata**: `name`, `version`, `description`, `author`, `keywords`, `homepage`, `repository`, `license`
- **Components**: `commands`, `agents`, `hooks`, `mcpServers`, `lspServers`

**NOT valid**: `skills`, `scripts` (these are just directories commands can read)

### Commands

Command files (`commands/*.md`) use YAML frontmatter with `name`, `description`. The `/adk` command is the main entry point.

### State Management

The `/adk` command tracks state in:
- `.claude/adk-builder.local.md` - Plugin state (current feature, phase, progress)
- `plugins/adk-builder/<feature>/spec.md` - Requirements
- `plugins/adk-builder/<feature>/plan.md` - Implementation steps
- `plugins/adk-builder/<feature>/session.md` - Build progress log

## Development Workflow

### Adding a New Plugin

1. Create `plugins/<plugin-name>/.claude-plugin/plugin.json`:
   ```json
   {
     "name": "plugin-name",
     "version": "1.0.0",
     "description": "Brief description",
     "commands": "./commands"
   }
   ```

2. Add to `.claude-plugin/marketplace.json` plugins array:
   ```json
   {
     "name": "plugin-name",
     "description": "Description for marketplace",
     "source": "./plugins/plugin-name",
     "category": "development"
   }
   ```

3. Create command files in `commands/` directory

### Testing Locally

**For development (recommended):** Use `--plugin-dir` to load directly from source, bypassing the cache:

```bash
# From repo root - loads plugin without installation
claude --plugin-dir ./plugins/adk-builder
```

Edits to plugin files are live on next Claude restart. No reinstallation needed.

**For release testing:** Install via marketplace to test the full install flow:

```bash
/plugin marketplace add ./path/to/agentic-plugins
/plugin install adk-builder@agentic-plugins
/adk  # Test the command
```

Note: Installed plugins are cached. After edits, you must reinstall or bump the version.

**Validate marketplace structure:**
```bash
/plugin validate .
```

## ADK Builder Skills (internal)

The adk-builder plugin includes knowledge files in `skills/` that commands reference via `@skill-name` syntax. These are NOT part of the official plugin manifest - just markdown files commands can read.

| Skill | Purpose |
|-------|---------|
| `@adk-core` | Project init, agent creation, configuration |
| `@adk-tools` | Function tools, MCP, OpenAPI, built-ins |
| `@adk-behavior` | Callbacks, state, memory, events |
| `@adk-orchestration` | Multi-agent, streaming, routing |
| `@adk-production` | Deployment, security, quality, testing |
| `@adk-advanced` | Extended thinking, visual builder |

## File Conventions

- Marketplace: `.claude-plugin/marketplace.json`
- Plugin manifest: `plugins/<plugin>/.claude-plugin/plugin.json`
- Commands: `plugins/<plugin>/commands/<name>.md`
