# ADK Builder

A Claude Code plugin for building Google Agent Development Kit applications with spec-driven workflows and unified orchestration.

## Installation

```bash
# Add marketplace
/plugin marketplace add MattMagg/agentic-plugins

# Install plugin
/plugin install adk-builder@agentic-plugins
```

## Development

For active plugin development, use `--plugin-dir` to load directly from source (bypasses cache):

```bash
# From the agentic-plugins repo root
claude --plugin-dir ./plugins/adk-builder

# Or with absolute path from anywhere
claude --plugin-dir /path/to/agentic-plugins/plugins/adk-builder
```

This avoids stale cache issues - edits are live on next Claude restart.

## Commands

### `/adk` - Main Entry Point

The unified command that detects your project state and enters the appropriate mode:

- **SPEC Mode**: No project exists → Interactive requirements gathering
- **PLAN Mode**: Has spec → Generate implementation steps
- **BUILD Mode**: Has plan or direct task → Implement

```bash
/adk                    # Auto-detect mode
/adk --spec             # Force spec mode
/adk --plan             # Force plan mode
/adk customer-support   # Start new feature
```

### `/adk-debug` - Diagnostics

Systematic debugging for ADK issues:

```bash
/adk-debug              # General diagnostic
/adk-debug "tool not found"  # Specific error
```

## Project Structure

When you run `/adk`, it creates:

```
your-repo/
├── adk-builder/
│   └── feature-name/
│       ├── spec.md      # Requirements and decisions
│       ├── plan.md      # Implementation steps
│       └── session.md   # Progress tracking
└── .claude/
    └── adk-builder.local.md  # Plugin state
```

## Skills

The plugin includes consolidated knowledge across 6 skill areas:

| Skill | Topics |
|-------|--------|
| `@adk-core` | Project init, agent creation, configuration |
| `@adk-tools` | Function tools, MCP, OpenAPI, built-ins |
| `@adk-behavior` | Callbacks, state, memory, events |
| `@adk-orchestration` | Multi-agent, streaming, routing |
| `@adk-production` | Deployment, security, quality |
| `@adk-advanced` | Extended thinking, visual builder |

## Workflow

1. **Start**: `/adk my-feature`
2. **Spec**: Answer questions, make decisions
3. **Plan**: Review generated implementation steps
4. **Build**: Execute plan or make direct changes
5. **Debug**: `/adk-debug` if issues arise

## Scripts

```bash
# Initialize new spec (used internally by /adk)
scripts/init-spec.sh <feature-name>

# Validate spec completeness
scripts/validate-spec.py adk-builder/<feature>/spec.md
```
