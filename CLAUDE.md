# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a Claude Code plugin marketplace for agentic development frameworks. Currently contains the `adk-builder` plugin for Google Agent Development Kit (ADK). The marketplace will expand to support other frameworks (OpenAI Agents SDK, etc.).

## Architecture

### Marketplace Structure

```
agentic-plugins/
├── .claude-plugin/
│   └── marketplace.json      # Plugin registry (add new plugins here)
└── plugins/
    ├── adk-builder/          # Google ADK plugin
    │   ├── .claude-plugin/
    │   │   └── plugin.json   # Plugin manifest (version, entry points)
    │   ├── commands/         # User-invocable slash commands
    │   ├── skills/           # Knowledge base (6 skill clusters)
    │   └── scripts/          # Automation (Bash/Python)
    └── <future-plugins>/     # Same structure as adk-builder
```

### Plugin Components

**Commands** (`commands/*.md`): Slash commands with YAML frontmatter defining `name`, `description`, `allowed-tools`. The `/adk` command is the main orchestrator with mode-based behavior (SPEC → PLAN → BUILD).

**Skills** (`skills/<name>/`): Each skill has:
- `SKILL.md` - Frontmatter with version, description, trigger keywords
- `references/` - Detailed markdown guides
- Skills are referenced via `@skill-name` syntax in specs/plans

**Scripts** (`scripts/`): Shell and Python automation. Currently:
- `init-spec.sh <name>` - Scaffold new spec from template
- `validate-spec.py <spec-path>` - Validate spec completeness

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
     "commands": "./commands",
     "skills": "./skills",
     "scripts": "./scripts"
   }
   ```

2. Add to `.claude-plugin/marketplace.json` plugins array

3. Create commands, skills, and scripts following `adk-builder` patterns

### Modifying Skills

Skills use a two-level structure:
- `SKILL.md` - Summary with trigger keywords (what Claude sees first)
- `references/*.md` - Detailed guides (loaded on demand)

When editing skills:
- Update version in `SKILL.md` frontmatter when making breaking changes
- Keep trigger keywords in the `description` field accurate
- Reference guides should be self-contained with code examples

### Testing Locally

Test plugins by adding the marketplace from a local path:
```bash
/plugin marketplace add ./path/to/agentic-plugins
/plugin install adk-builder@agentic-plugins
/adk  # Test the command
```

Validate marketplace structure:
```bash
/plugin validate .
```

## Skill Cluster Reference

| Skill | Purpose |
|-------|---------|
| `@adk-core` | Project init, agent creation, configuration |
| `@adk-tools` | Function tools, MCP, OpenAPI, built-ins |
| `@adk-behavior` | Callbacks, state, memory, events |
| `@adk-orchestration` | Multi-agent, streaming, routing |
| `@adk-production` | Deployment, security, quality, testing |
| `@adk-advanced` | Extended thinking, visual builder |

## File Conventions

- Command files: `plugins/<plugin>/commands/<command-name>.md`
- Skill definitions: `plugins/<plugin>/skills/<skill-name>/SKILL.md`
- Skill references: `plugins/<plugin>/skills/<skill-name>/references/<topic>.md`
- Plugin manifest: `plugins/<plugin>/.claude-plugin/plugin.json`
- Marketplace registry: `.claude-plugin/marketplace.json`
