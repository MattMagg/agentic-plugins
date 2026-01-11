---
name: ADK Core
description: This skill should be used when the user asks about "creating a new ADK project", "initializing ADK", "setting up Google ADK", "adk create command", "ADK project structure", "YAML agent configuration", "creating an agent", "LlmAgent", "BaseAgent", "custom agent", "agent with different model", "Claude with ADK", "OpenAI with ADK", "LiteLLM", "multi-model agent", or needs guidance on bootstrapping an ADK development environment, authentication setup, choosing between Python code and YAML-based agent definitions, agent configuration, model selection, system instructions, or extending the base agent class for non-LLM logic.
version: 2.0.0
---

# ADK Core

Comprehensive guide for initializing Google Agent Development Kit (ADK) projects and creating agents. Covers project setup, authentication, agent configuration, and model selection.

## When to Use

**Project Setup:**
- Starting a new ADK project from scratch
- Setting up authentication (API key or Vertex AI)
- Understanding ADK project structure
- Choosing between Python and YAML configuration
- Running agents locally for development

**Agent Creation:**
- Creating a new ADK agent from scratch
- Configuring agent parameters (model, name, instruction, description)
- Using non-Gemini models (Claude, OpenAI via LiteLLM)
- Building custom agents without LLM reasoning

## When NOT to Use

- Adding tools to agents → Use `@adk-tools` instead
- Multi-agent orchestration → Use `@adk-multi-agent` instead
- Callbacks and state management → Use `@adk-behavior` instead
- Deploying to production → Use `@adk-deployment` instead
- Memory and knowledge management → Use `@adk-memory` instead

## Key Concepts

### Project Initialization

**Installation**: `pip install google-adk` in Python 3.10+ virtual environment. Verify with `adk --version`.

**Project Creation**: `adk create <name>` scaffolds a new agent project with `agent.py`, `__init__.py`, and `.env`.

**Authentication Options**: Google AI Studio (GOOGLE_API_KEY) for prototyping, Vertex AI (GOOGLE_CLOUD_PROJECT) for production.

**Running Agents**: `adk run` for CLI, `adk web` for development UI, `adk api_server` for HTTP API.

**YAML Configuration**: Declarative agent definition without Python code. Quick prototyping for simple agents.

**Project Structure**: `agent.py` exports `root_agent`. ADK CLI discovers and runs the exported agent.

### Agent Types

**LlmAgent** is the standard agent type for AI reasoning, conversation, and tool use. Requires `model` and `name` parameters. Use `instruction` for system prompts and `description` for routing in multi-agent systems.

**BaseAgent** is for custom non-LLM logic. Extend it and implement `run_async()` to yield responses. Use when you need deterministic behavior or external API orchestration.

**Model Selection**: Default to `gemini-3-flash-preview`. Use LiteLLM prefix for other providers (e.g., `anthropic/claude-sonnet-4`).

## References

Detailed guides with code examples:

**Project Setup:**
- `references/init.md` - Complete initialization workflow
- `references/create-project.md` - Python project scaffolding
- `references/yaml-config.md` - YAML-based configuration

**Agent Creation:**
- `references/llm-agent.md` - Complete LlmAgent configuration and parameters
- `references/custom-agent.md` - BaseAgent extension patterns
- `references/multi-model.md` - LiteLLM setup and model switching
