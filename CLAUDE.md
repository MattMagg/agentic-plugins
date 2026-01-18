# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a Claude Code plugin marketplace for agentic development frameworks. Contains two plugins:

- **adk-builder** - Specialized plugin for Google Agent Development Kit (ADK) with spec-driven workflows
- **agentic-builder** - Framework-agnostic plugin with RAG-grounded knowledge across ADK, OpenAI, LangChain, LangGraph, Anthropic, and CrewAI

## Architecture

### Marketplace Structure

```
agentic-plugins/
├── .claude-plugin/
│   └── marketplace.json      # Plugin registry
└── plugins/
    ├── adk-builder/          # ADK-specific plugin
    │   ├── .claude-plugin/
    │   │   └── plugin.json
    │   ├── commands/
    │   ├── agents/
    │   └── skills/
    └── agentic-builder/      # Framework-agnostic plugin
        ├── .claude-plugin/
        │   └── plugin.json
        ├── commands/         # /agentic entry point
        ├── agents/           # planner, executor, debugger
        ├── skills/           # 9 skills (6 framework + 3 task)
        ├── hooks/            # session-start, pre-compact
        ├── mcp-server/       # RAG query tools
        └── templates/        # spec.md, plan.md templates
```

### Plugin Manifest

Per official docs, valid `plugin.json` fields:
- **Metadata**: `name`, `version`, `description`, `author`, `keywords`, `homepage`, `repository`, `license`
- **Components**: `commands`, `agents`, `hooks`, `mcpServers`, `lspServers`

**NOT valid**: `skills`, `scripts` (these are just directories commands can read)

### Commands

Command files (`commands/*.md`) use YAML frontmatter with `name`, `description`.

- **adk-builder**: `/adk` - ADK-specific development
- **agentic-builder**: `/agentic` - Framework-agnostic development with auto-detection

### State Management

**adk-builder** (`/adk`) tracks state in:
- `.claude/adk-builder.local.md` - Plugin state (current feature, phase, progress)
- `adk-builder/<feature>/spec.md` - Requirements
- `adk-builder/<feature>/plan.md` - Implementation steps

**agentic-builder** (`/agentic`) tracks state in:
- `.claude/agentic-builder.local.md` - Active frameworks, phase, progress
- `agentic-builder/<feature>/spec.md` - Requirements
- `agentic-builder/<feature>/plan.md` - Implementation steps
- `agentic-builder/<feature>/session.md` - Build progress log

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

## Plugin Skills

Skills are knowledge files in `skills/` that commands reference via `@skill-name` syntax. These are NOT part of the official plugin manifest - just markdown files commands can read.

### ADK Builder Skills

| Skill | Purpose |
|-------|---------|
| `@adk-core` | Project init, agent creation, configuration |
| `@adk-tools` | Function tools, MCP, OpenAPI, built-ins |
| `@adk-behavior` | Callbacks, state, memory, events |
| `@adk-orchestration` | Multi-agent, streaming, routing |
| `@adk-production` | Deployment, security, quality, testing |
| `@adk-advanced` | Extended thinking, visual builder |

### Agentic Builder Skills

**Framework skills** (idioms, gotchas, patterns):
| Skill | Framework |
|-------|-----------|
| `@adk` | Google ADK |
| `@openai-agents` | OpenAI Agents SDK |
| `@langchain` | LangChain |
| `@langgraph` | LangGraph |
| `@anthropic-agents` | Anthropic Agents SDK |
| `@crewai` | CrewAI |

**Task skills**:
| Skill | Purpose |
|-------|---------|
| `@debugging` | Cross-framework debugging patterns |
| `@deployment` | Production deployment checklist |
| `@orchestration` | Multi-agent coordination patterns |

## File Conventions

- Marketplace: `.claude-plugin/marketplace.json`
- Plugin manifest: `plugins/<plugin>/.claude-plugin/plugin.json`
- Commands: `plugins/<plugin>/commands/<name>.md`
