# ADK Builder Plugin Redesign Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Transform the adk-builder plugin from a fragmented 10-command/4-agent system into a cohesive single-entry-point architecture with mode-based behavior, consolidated skills, and spec-driven workflows.

**Architecture:** Single `/adk` root command that detects project state and enters appropriate mode (SPEC/PLAN/BUILD). Separate `/adk-debug` for diagnostics. Skills consolidated from 11 to 6 clusters. State tracked via `adk-builder/<feature>/` folders and `.claude/adk-builder.local.md`. Scripts handle automation (spec init, validation).

**Tech Stack:** Claude Code plugin system (commands, skills, scripts, hooks), Markdown templates, Bash/Python scripts, YAML frontmatter for state.

---

## Phase 1: Cleanup - Remove Old Structure

### Task 1.1: Remove Old Commands

**Files:**
- Delete: `commands/adk-add-memory.md`
- Delete: `commands/adk-add-behavior.md`
- Delete: `commands/adk-add-tool.md`
- Delete: `commands/adk-create-agent.md`
- Delete: `commands/adk-deploy.md`
- Delete: `commands/adk-init.md`
- Delete: `commands/adk-multi-agent.md`
- Delete: `commands/adk-secure.md`
- Delete: `commands/adk-streaming.md`
- Delete: `commands/adk-test.md`

**Step 1: Remove all old command files**

```bash
cd /Users/mac-main/agentic-plugins/adk-builder
rm -f commands/adk-add-memory.md
rm -f commands/adk-add-behavior.md
rm -f commands/adk-add-tool.md
rm -f commands/adk-create-agent.md
rm -f commands/adk-deploy.md
rm -f commands/adk-init.md
rm -f commands/adk-multi-agent.md
rm -f commands/adk-secure.md
rm -f commands/adk-streaming.md
rm -f commands/adk-test.md
```

**Step 2: Verify commands directory only has CLAUDE.md**

Run: `ls commands/`
Expected: Only `CLAUDE.md` remains

**Step 3: Commit cleanup**

```bash
git add -A
git commit -m "chore: remove old granular commands (replaced by /adk root)"
```

---

### Task 1.2: Remove Old Agents

**Files:**
- Delete: `agents/adk-planner.md`
- Delete: `agents/adk-executor.md`
- Delete: `agents/adk-verifier.md`
- Delete: `agents/adk-debugger.md`

**Step 1: Remove all old agent files**

```bash
cd /Users/mac-main/agentic-plugins/adk-builder
rm -f agents/adk-planner.md
rm -f agents/adk-executor.md
rm -f agents/adk-verifier.md
rm -f agents/adk-debugger.md
```

**Step 2: Verify agents directory only has CLAUDE.md**

Run: `ls agents/`
Expected: Only `CLAUDE.md` remains

**Step 3: Commit cleanup**

```bash
git add -A
git commit -m "chore: remove old separate agents (replaced by unified orchestrator)"
```

---

## Phase 2: Create New Commands

### Task 2.1: Create Root /adk Command

**Files:**
- Create: `commands/adk.md`

**Step 1: Write the /adk command**

```markdown
---
name: adk
description: Root command for Google ADK development - detects project state and enters appropriate mode (SPEC/PLAN/BUILD)
argument-hint: Optional feature name or --debug/--spec/--plan flags
allowed-tools: ["Read", "Write", "Bash", "Glob", "Grep", "AskUserQuestion", "Task", "Skill"]
---

# ADK Builder

You are the ADK Builder, an expert system for developing Google Agent Development Kit applications. You operate as a unified orchestrator with mode-based behavior.

## State Detection

On invocation, detect current state:

1. **Check for existing projects**: `ls adk-builder/` - are there existing feature folders?
2. **Check for active state**: Read `.claude/adk-builder.local.md` if it exists
3. **Parse arguments**: `--spec`, `--plan`, `--debug` force specific modes

## Modes

### SPEC Mode (No project OR --spec flag)
- Interactive requirements gathering
- Use hybrid template + conversation approach
- Create `adk-builder/<feature-name>/spec.md`
- Reference skills with `@skill-name` syntax, don't duplicate content
- Ask clarifying questions one at a time
- Record decisions with rationale

### PLAN Mode (Has spec OR --plan flag)
- Read spec from `adk-builder/<feature>/spec.md`
- Transform requirements into ordered implementation steps
- Create `adk-builder/<feature>/plan.md`
- Each step references specific skill sections
- Include verification criteria

### BUILD Mode (Has plan OR direct task)
- Execute plan step-by-step OR implement direct request
- Load relevant skills as needed: `@adk-core`, `@adk-tools`, etc.
- Write clean, production-ready ADK code
- Verify each step before proceeding
- Update `adk-builder/<feature>/session.md` with progress

## State File Format

```yaml
# .claude/adk-builder.local.md
---
current_feature: customer-support-agent
phase: plan
spec_path: adk-builder/customer-support-agent/spec.md
plan_path: adk-builder/customer-support-agent/plan.md
last_completed_step: 3
---

# Session Notes
- Decided on LlmAgent over BaseAgent because...
```

## Skill References

When you need domain knowledge, load the appropriate skill:
- `@adk-core` - Agent creation, project setup, configuration
- `@adk-tools` - Function tools, MCP, OpenAPI, built-ins
- `@adk-behavior` - Callbacks, state, memory, events
- `@adk-orchestration` - Multi-agent patterns, streaming
- `@adk-production` - Deployment, security, quality
- `@adk-advanced` - Extended thinking, visual builder

## Output Format

Always be clear about current mode and next steps:

```
## Current State
- Feature: [name or "none"]
- Mode: [SPEC/PLAN/BUILD]
- Progress: [status]

## Next Action
[What you're about to do]
```

## Error Handling

If you encounter issues during BUILD:
- Stop and diagnose
- Check common issues (imports, docstrings, auth)
- Suggest `/adk-debug` for complex problems
```

**Step 2: Verify file was created**

Run: `cat commands/adk.md | head -20`
Expected: Shows frontmatter and beginning of command

**Step 3: Commit**

```bash
git add commands/adk.md
git commit -m "feat: add /adk root command with mode-based orchestration"
```

---

### Task 2.2: Create /adk-debug Command

**Files:**
- Create: `commands/adk-debug.md`

**Step 1: Write the /adk-debug command**

```markdown
---
name: adk-debug
description: Diagnostic mode for ADK issues - analyzes errors, traces problems, suggests fixes
argument-hint: Optional error message or file path
allowed-tools: ["Read", "Bash", "Glob", "Grep", "Skill"]
---

# ADK Debugger

You are the ADK Debugger, specializing in diagnosing and resolving Google ADK issues. You operate in a systematic, hypothesis-driven manner.

## Diagnostic Process

### 1. Gather Context

```bash
# Check ADK installation
pip list | grep google-adk

# Check project structure
ls -la
ls -la *.py 2>/dev/null || echo "No Python files in root"

# Check for agent.py with root_agent
grep -r "root_agent" --include="*.py" . 2>/dev/null | head -5

# Check .env exists
ls -la .env 2>/dev/null || echo "No .env file"
```

### 2. Categorize Issue

| Category | Symptoms | First Checks |
|----------|----------|--------------|
| **Import/Startup** | ModuleNotFoundError, ImportError | pip list, import paths |
| **Tool Issues** | "tool not found", wrong args | docstrings, type hints, tools=[] |
| **Auth Errors** | 401, 403, API key invalid | .env, GOOGLE_API_KEY |
| **Runtime** | Unexpected behavior, crashes | logs, state, callbacks |
| **Multi-Agent** | Wrong routing, lost context | sub_agents, descriptions |

### 3. Common Fixes

**Import Errors:**
```python
# Wrong
from google.adk import Agent

# Right
from google.adk.agents import LlmAgent
```

**Tool Not Found:**
```python
# Missing docstring - LLM can't understand the tool
def my_tool(x: str) -> str:
    """Describe what this tool does.  # <-- Required!

    Args:
        x: Description of parameter
    """
    return x
```

**Auth Issues:**
```bash
# Check .env format
cat .env | grep -E "GOOGLE_API_KEY|GOOGLE_CLOUD_PROJECT"

# Test auth
python -c "from google import genai; print(genai.Client())"
```

### 4. Output Format

```
## Diagnosis

**Error:** [exact error message]
**Category:** [Import/Tool/Auth/Runtime/Multi-Agent]
**Root Cause:** [explanation]

## Fix

**File:** `path/to/file.py`

```python
# Before
[problematic code]

# After
[fixed code]
```

**Verification:**
Run: `[command]`
Expected: `[result]`
```

## Reference Skills

For deeper investigation:
- `@adk-core` - Project structure, agent configuration
- `@adk-tools` - Tool requirements, ToolContext
- `@adk-behavior` - Callback issues, state problems
- `@adk-production/references/quality` - Logging, tracing
```

**Step 2: Verify file was created**

Run: `cat commands/adk-debug.md | head -20`
Expected: Shows frontmatter and beginning of command

**Step 3: Commit**

```bash
git add commands/adk-debug.md
git commit -m "feat: add /adk-debug diagnostic command"
```

---

## Phase 3: Consolidate Skills

### Task 3.1: Create adk-core Skill (Merge getting-started + agents)

**Files:**
- Create: `skills/adk-core/SKILL.md`
- Move: `skills/adk-getting-started/references/*` → `skills/adk-core/references/`
- Move: `skills/adk-agents/references/*` → `skills/adk-core/references/`
- Delete: `skills/adk-getting-started/` (after merge)
- Delete: `skills/adk-agents/` (after merge)

**Step 1: Create adk-core directory structure**

```bash
cd /Users/mac-main/agentic-plugins/adk-builder
mkdir -p skills/adk-core/references
```

**Step 2: Write adk-core SKILL.md**

```markdown
---
name: ADK Core
description: This skill covers ADK project initialization, agent creation, and configuration. Use when starting new projects, creating agents (LlmAgent, BaseAgent, custom), configuring models, or setting up authentication.
version: 3.0.0
---

# ADK Core

Foundation skill for Google Agent Development Kit projects. Covers initialization, agent creation, and configuration.

## When to Use

- Starting a new ADK project
- Creating agents (LlmAgent, BaseAgent, custom)
- Configuring models and authentication
- Understanding project structure

## When NOT to Use

- Adding tools → `@adk-tools`
- Callbacks/state → `@adk-behavior`
- Multi-agent patterns → `@adk-orchestration`
- Deployment → `@adk-production`

## Quick Reference

### Installation
```bash
pip install google-adk
adk --version
```

### Project Creation
```bash
adk create my_agent
cd my_agent
```

### Basic Agent
```python
from google.adk.agents import LlmAgent

root_agent = LlmAgent(
    name="my_agent",
    model="gemini-2.0-flash",
    instruction="You are a helpful assistant.",
    tools=[]
)
```

### Authentication (.env)
```env
# Option A: Google AI Studio
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_API_KEY=your_key

# Option B: Vertex AI
GOOGLE_GENAI_USE_VERTEXAI=TRUE
GOOGLE_CLOUD_PROJECT=your_project
```

### Running
```bash
adk web      # Browser UI at localhost:8000
adk run      # CLI mode
```

## Key Decisions

| Decision | Options | Guidance |
|----------|---------|----------|
| Agent Type | LlmAgent vs BaseAgent | LlmAgent for LLM reasoning, BaseAgent for custom logic |
| Model | gemini-2.0-flash vs others | Flash for speed, Pro for complex reasoning |
| Auth | API Key vs Vertex | API Key for dev, Vertex for production |
| Config | Python vs YAML | Python for flexibility, YAML for simple agents |

## References

Detailed guides:
- `references/init.md` - Project initialization
- `references/create-project.md` - Scaffolding details
- `references/yaml-config.md` - YAML-based agents
- `references/llm-agent.md` - LlmAgent configuration
- `references/custom-agent.md` - BaseAgent subclassing
- `references/multi-model.md` - Using different models
```

**Step 3: Copy reference files**

```bash
cp skills/adk-getting-started/references/*.md skills/adk-core/references/
cp skills/adk-agents/references/*.md skills/adk-core/references/
```

**Step 4: Copy CLAUDE.md**

```bash
cp skills/adk-getting-started/CLAUDE.md skills/adk-core/CLAUDE.md
```

**Step 5: Verify structure**

Run: `ls skills/adk-core/references/`
Expected: init.md, create-project.md, yaml-config.md, llm-agent.md, custom-agent.md, multi-model.md

**Step 6: Remove old skill directories**

```bash
rm -rf skills/adk-getting-started
rm -rf skills/adk-agents
```

**Step 7: Commit**

```bash
git add -A
git commit -m "feat: consolidate adk-getting-started + adk-agents into adk-core"
```

---

### Task 3.2: Create adk-behavior Skill (Merge behavior + memory)

**Files:**
- Modify: `skills/adk-behavior/SKILL.md`
- Move: `skills/adk-memory/references/*` → `skills/adk-behavior/references/`
- Delete: `skills/adk-memory/` (after merge)

**Step 1: Update adk-behavior SKILL.md**

```markdown
---
name: ADK Behavior
description: This skill covers agent behavior customization including callbacks, session state, memory services, events, artifacts, and human-in-the-loop confirmation patterns.
version: 3.0.0
---

# ADK Behavior

Customize agent behavior through callbacks, state management, memory, and event handling.

## When to Use

- Adding before/after tool callbacks
- Managing session state
- Implementing long-term memory
- Handling events and artifacts
- Adding human-in-the-loop confirmation

## When NOT to Use

- Creating agents → `@adk-core`
- Adding tools → `@adk-tools`
- Multi-agent routing → `@adk-orchestration`

## Quick Reference

### Callbacks
```python
def before_tool(tool, args, tool_context):
    """Runs before every tool call."""
    if "dangerous" in str(args):
        return {"blocked": True}
    return None  # Continue

root_agent = LlmAgent(
    name="agent",
    model="gemini-2.0-flash",
    before_tool_callback=before_tool
)
```

### Session State
```python
def my_tool(query: str, tool_context: ToolContext) -> dict:
    # Read state
    user = tool_context.state.get("user_name", "Unknown")

    # Write state (prefix determines scope)
    tool_context.state["app:counter"] = 1  # App-wide
    tool_context.state["user:pref"] = "dark"  # User-specific
    tool_context.state["temp:cache"] = {}  # Session only

    return {"user": user}
```

### Memory Service
```python
from google.adk.memory import InMemoryMemoryService

memory = InMemoryMemoryService()
root_agent = LlmAgent(
    name="agent",
    model="gemini-2.0-flash",
    memory_service=memory
)
```

## Key Concepts

| Concept | Purpose | Scope |
|---------|---------|-------|
| Callbacks | Intercept tool execution | Per-agent |
| State | Store data across turns | Session/User/App |
| Memory | Long-term recall | Cross-session |
| Events | React to agent lifecycle | Per-invocation |
| Artifacts | File handling | Per-session |

## References

- `references/callbacks.md` - Before/after tool callbacks
- `references/state.md` - Session state management
- `references/memory-service.md` - Long-term memory
- `references/grounding.md` - RAG and knowledge bases
- `references/events.md` - Event handling
- `references/artifacts.md` - File uploads/downloads
- `references/confirmation.md` - Human-in-the-loop
- `references/plugins.md` - Behavior plugins
```

**Step 2: Copy memory references**

```bash
cp skills/adk-memory/references/*.md skills/adk-behavior/references/
```

**Step 3: Verify structure**

Run: `ls skills/adk-behavior/references/`
Expected: callbacks.md, state.md, events.md, artifacts.md, confirmation.md, plugins.md, memory-service.md, grounding.md

**Step 4: Remove old memory skill**

```bash
rm -rf skills/adk-memory
```

**Step 5: Commit**

```bash
git add -A
git commit -m "feat: merge adk-memory into adk-behavior"
```

---

### Task 3.3: Create adk-orchestration Skill (Merge multi-agent + streaming)

**Files:**
- Create: `skills/adk-orchestration/SKILL.md`
- Create: `skills/adk-orchestration/CLAUDE.md`
- Move: `skills/adk-multi-agent/references/*` → `skills/adk-orchestration/references/`
- Move: `skills/adk-streaming/references/*` → `skills/adk-orchestration/references/`
- Delete: `skills/adk-multi-agent/`
- Delete: `skills/adk-streaming/`

**Step 1: Create directory**

```bash
mkdir -p skills/adk-orchestration/references
```

**Step 2: Write SKILL.md**

```markdown
---
name: ADK Orchestration
description: This skill covers multi-agent systems, agent routing, parallel/sequential execution, streaming responses, and real-time communication patterns.
version: 3.0.0
---

# ADK Orchestration

Build multi-agent systems and implement real-time streaming communication.

## When to Use

- Creating multi-agent hierarchies
- Implementing agent routing/delegation
- Using SequentialAgent, ParallelAgent, LoopAgent
- Adding SSE or bidirectional streaming
- Integrating Live API for voice/video

## When NOT to Use

- Single agent creation → `@adk-core`
- Tool implementation → `@adk-tools`
- Callbacks/state → `@adk-behavior`

## Quick Reference

### Multi-Agent Hierarchy
```python
from google.adk.agents import LlmAgent

support_agent = LlmAgent(
    name="support",
    model="gemini-2.0-flash",
    instruction="Handle customer support queries."
)

sales_agent = LlmAgent(
    name="sales",
    model="gemini-2.0-flash",
    instruction="Handle sales inquiries."
)

coordinator = LlmAgent(
    name="coordinator",
    model="gemini-2.0-flash",
    instruction="Route to appropriate specialist.",
    sub_agents=[support_agent, sales_agent]
)

root_agent = coordinator
```

### Workflow Agents
```python
from google.adk.agents import SequentialAgent, ParallelAgent

# Sequential: A → B → C
pipeline = SequentialAgent(
    name="pipeline",
    sub_agents=[research_agent, write_agent, review_agent]
)

# Parallel: A + B + C (concurrent)
parallel = ParallelAgent(
    name="parallel",
    sub_agents=[search_web, search_docs, search_code]
)
```

### SSE Streaming
```python
async for event in agent.run_async_stream(user_input):
    if event.type == "text_delta":
        print(event.content, end="")
```

## Key Patterns

| Pattern | Use Case | Agent Type |
|---------|----------|------------|
| Router | Direct to specialist | LlmAgent with sub_agents |
| Pipeline | Sequential workflow | SequentialAgent |
| Scatter-Gather | Parallel search | ParallelAgent |
| Loop | Iterative refinement | LoopAgent |

## References

- `references/delegation.md` - Sub-agent delegation
- `references/orchestration.md` - Routing patterns
- `references/advanced.md` - Complex hierarchies
- `references/a2a.md` - Agent-to-agent protocol
- `references/sse.md` - Server-sent events
- `references/bidirectional.md` - WebSocket streaming
- `references/multimodal.md` - Voice/video with Live API
```

**Step 3: Copy CLAUDE.md and references**

```bash
cp skills/adk-multi-agent/CLAUDE.md skills/adk-orchestration/CLAUDE.md
cp skills/adk-multi-agent/references/*.md skills/adk-orchestration/references/
cp skills/adk-streaming/references/*.md skills/adk-orchestration/references/
```

**Step 4: Remove old directories**

```bash
rm -rf skills/adk-multi-agent
rm -rf skills/adk-streaming
```

**Step 5: Commit**

```bash
git add -A
git commit -m "feat: consolidate adk-multi-agent + adk-streaming into adk-orchestration"
```

---

### Task 3.4: Create adk-production Skill (Merge deployment + security + quality)

**Files:**
- Create: `skills/adk-production/SKILL.md`
- Create: `skills/adk-production/CLAUDE.md`
- Create: `skills/adk-production/references/`
- Move references from: `adk-deployment`, `adk-security`, `adk-quality`
- Delete: `skills/adk-deployment/`, `skills/adk-security/`, `skills/adk-quality/`

**Step 1: Create directory**

```bash
mkdir -p skills/adk-production/references
```

**Step 2: Write SKILL.md**

```markdown
---
name: ADK Production
description: This skill covers deploying ADK agents to production, implementing security (guardrails, auth), and ensuring quality (testing, tracing, observability).
version: 3.0.0
---

# ADK Production

Deploy, secure, and maintain production-quality ADK agents.

## When to Use

- Deploying to Cloud Run, GKE, or Agent Engine
- Adding security guardrails and authentication
- Implementing testing and evaluation
- Setting up logging, tracing, observability

## When NOT to Use

- Creating agents → `@adk-core`
- Adding tools → `@adk-tools`
- Behavior customization → `@adk-behavior`

## Quick Reference

### Deployment Options

| Platform | Best For | Complexity |
|----------|----------|------------|
| Agent Engine | Managed, serverless | Low |
| Cloud Run | Containerized, scalable | Medium |
| GKE | Full control, Kubernetes | High |

### Basic Cloud Run
```bash
# Build and deploy
gcloud run deploy my-agent \
  --source . \
  --region us-central1 \
  --allow-unauthenticated
```

### Security Guardrails
```python
from google.adk.safety import ContentFilter

content_filter = ContentFilter(
    blocked_categories=["HARM_CATEGORY_DANGEROUS_CONTENT"]
)

root_agent = LlmAgent(
    name="agent",
    model="gemini-2.0-flash",
    safety_settings=content_filter
)
```

### Testing
```python
# test_agent.py
from my_agent import root_agent

def test_basic_response():
    result = root_agent.run("Hello")
    assert "error" not in result.lower()
```

```bash
pytest tests/ -v
```

### Tracing
```bash
adk web --trace_to_cloud my_agent
```

## Key Concerns

| Area | What to Check |
|------|---------------|
| Security | Input validation, auth, rate limits |
| Reliability | Error handling, retries, timeouts |
| Observability | Logs, traces, metrics |
| Quality | Tests, evals, benchmarks |

## References

### Deployment
- `references/agent-engine.md` - Managed deployment
- `references/cloudrun.md` - Container deployment
- `references/gke.md` - Kubernetes deployment

### Security
- `references/guardrails.md` - Content filtering
- `references/auth.md` - Authentication patterns
- `references/security-plugins.md` - Security extensions

### Quality
- `references/evals.md` - Agent evaluation
- `references/tracing.md` - Distributed tracing
- `references/logging.md` - Log management
- `references/observability.md` - Monitoring
- `references/user-sim.md` - User simulation testing
```

**Step 3: Copy CLAUDE.md and references**

```bash
cp skills/adk-deployment/CLAUDE.md skills/adk-production/CLAUDE.md
cp skills/adk-deployment/references/*.md skills/adk-production/references/
cp skills/adk-security/references/*.md skills/adk-production/references/
cp skills/adk-quality/references/*.md skills/adk-production/references/
```

**Step 4: Remove old directories**

```bash
rm -rf skills/adk-deployment
rm -rf skills/adk-security
rm -rf skills/adk-quality
```

**Step 5: Verify final skill structure**

Run: `ls skills/`
Expected: adk-advanced, adk-behavior, adk-core, adk-orchestration, adk-production, adk-tools

**Step 6: Commit**

```bash
git add -A
git commit -m "feat: consolidate adk-deployment + adk-security + adk-quality into adk-production"
```

---

### Task 3.5: Update adk-tools SKILL.md (Keep as-is, minor updates)

**Files:**
- Modify: `skills/adk-tools/SKILL.md`

**Step 1: Update version and cross-references**

Replace the existing SKILL.md content, keeping the same structure but updating skill references:

```markdown
---
name: ADK Tools
description: This skill covers adding tools to ADK agents including FunctionTool, built-in tools (google_search, code_execution), OpenAPI integration, MCP servers, and third-party tool frameworks.
version: 3.0.0
---

# ADK Tools

Extend agent capabilities with custom functions, APIs, and external integrations.

## When to Use

- Creating custom Python function tools
- Using built-in tools (Google Search, Code Execution)
- Integrating REST APIs via OpenAPI
- Connecting MCP servers
- Wrapping LangChain/CrewAI tools
- Implementing long-running async tools

## When NOT to Use

- Creating the agent itself → `@adk-core`
- Callbacks and state → `@adk-behavior`
- Multi-agent routing → `@adk-orchestration`

## Quick Reference

### FunctionTool
```python
def get_weather(city: str, unit: str = "celsius") -> dict:
    """Get current weather for a city.

    Args:
        city: City name to check weather for.
        unit: Temperature unit (celsius/fahrenheit).
    """
    return {"temp": 22, "conditions": "sunny"}

root_agent = LlmAgent(
    name="weather_agent",
    model="gemini-2.0-flash",
    tools=[get_weather]  # Auto-wrapped as FunctionTool
)
```

### Built-in Tools
```python
from google.adk.tools import google_search, code_execution

root_agent = LlmAgent(
    name="research_agent",
    model="gemini-2.0-flash",
    tools=[google_search, code_execution]
)
```

### ToolContext Access
```python
from google.adk.tools.tool_context import ToolContext

def my_tool(query: str, tool_context: ToolContext) -> dict:
    # Access session state
    user = tool_context.state.get("user_name")
    # ToolContext is auto-injected, don't document in docstring
    return {"result": f"Hello {user}"}
```

## Tool Types

| Type | Use Case | Setup |
|------|----------|-------|
| FunctionTool | Custom Python logic | Define function with docstring |
| Built-in | Search, code exec | Import from google.adk.tools |
| OpenAPI | REST APIs | Provide spec URL |
| MCP | External servers | Configure in .mcp.json |
| Third-party | LangChain, CrewAI | Wrap with adapter |

## References

- `references/function-tools.md` - Custom function tools
- `references/builtin-tools.md` - Google Search, Code Execution
- `references/openapi-tools.md` - REST API integration
- `references/mcp-tools.md` - MCP server connection
- `references/third-party-tools.md` - LangChain, CrewAI adapters
- `references/long-running-tools.md` - Async operations
- `references/computer-use.md` - Browser/desktop automation
```

**Step 2: Commit**

```bash
git add skills/adk-tools/SKILL.md
git commit -m "chore: update adk-tools skill references for v3"
```

---

### Task 3.6: Update adk-advanced SKILL.md (Keep as-is, minor updates)

**Files:**
- Modify: `skills/adk-advanced/SKILL.md`

**Step 1: Update version**

Update the frontmatter version to 3.0.0 and ensure cross-references use new skill names.

**Step 2: Commit**

```bash
git add skills/adk-advanced/SKILL.md
git commit -m "chore: update adk-advanced skill for v3"
```

---

## Phase 4: Create Scripts and Templates

### Task 4.1: Create Scripts Directory Structure

**Files:**
- Create: `scripts/init-spec.sh`
- Create: `scripts/validate-spec.py`

**Step 1: Create scripts directory**

```bash
mkdir -p /Users/mac-main/agentic-plugins/adk-builder/scripts
```

**Step 2: Create init-spec.sh**

```bash
#!/bin/bash
# Initialize a new ADK project spec
# Usage: init-spec.sh <feature-name>

set -e

FEATURE_NAME="${1:-new-feature}"
FEATURE_SLUG=$(echo "$FEATURE_NAME" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd '[:alnum:]-')
PROJECT_DIR="adk-builder/${FEATURE_SLUG}"
TIMESTAMP=$(date +%Y-%m-%d)

# Create project directory
mkdir -p "$PROJECT_DIR"

# Create spec.md from template
cat > "$PROJECT_DIR/spec.md" << 'SPEC_EOF'
# ADK Project Spec: {{FEATURE_NAME}}

> Created: {{TIMESTAMP}}
> Status: Draft

## Overview

<!-- What are you building? One paragraph description. -->

## Agent Architecture

| Aspect | Decision | Rationale |
|--------|----------|-----------|
| Agent Type | [ ] LlmAgent / [ ] BaseAgent / [ ] Custom | |
| Model | [ ] gemini-2.0-flash / [ ] gemini-2.0-pro / [ ] Other | |
| Multi-agent | [ ] Single / [ ] Hierarchy / [ ] Workflow | |

## Tools Required

<!-- Reference @adk-tools for implementation details -->

- [ ] Custom function tools
  - Tool 1:
  - Tool 2:
- [ ] Built-in tools
  - [ ] google_search
  - [ ] code_execution
- [ ] External integrations
  - [ ] OpenAPI:
  - [ ] MCP:

## Behavior Configuration

<!-- Reference @adk-behavior for implementation details -->

- [ ] Session state needed
  - Keys:
- [ ] Callbacks required
  - [ ] before_tool_callback
  - [ ] after_tool_callback
- [ ] Memory service
  - [ ] InMemory
  - [ ] Persistent
- [ ] Human-in-the-loop confirmation
  - For:

## Deployment Target

<!-- Reference @adk-production for implementation details -->

- [ ] Local development only
- [ ] Cloud Run
- [ ] Agent Engine
- [ ] GKE

## Open Questions

<!-- Capture unknowns discovered during spec creation -->

1.

## Decisions Made

<!-- Record choices with rationale -->

| Decision | Choice | Why |
|----------|--------|-----|
| | | |

SPEC_EOF

# Replace placeholders
sed -i '' "s/{{FEATURE_NAME}}/${FEATURE_NAME}/g" "$PROJECT_DIR/spec.md"
sed -i '' "s/{{TIMESTAMP}}/${TIMESTAMP}/g" "$PROJECT_DIR/spec.md"

# Create empty session.md
cat > "$PROJECT_DIR/session.md" << 'SESSION_EOF'
# Session Log

## Progress

- [ ] Spec created
- [ ] Spec reviewed
- [ ] Plan created
- [ ] Implementation started
- [ ] Implementation complete
- [ ] Verified

## Notes

SESSION_EOF

echo "Created: $PROJECT_DIR/spec.md"
echo "Created: $PROJECT_DIR/session.md"
```

**Step 3: Make executable**

```bash
chmod +x /Users/mac-main/agentic-plugins/adk-builder/scripts/init-spec.sh
```

**Step 4: Commit**

```bash
git add scripts/
git commit -m "feat: add init-spec.sh script for project scaffolding"
```

---

### Task 4.2: Create Spec Validator Script

**Files:**
- Create: `scripts/validate-spec.py`

**Step 1: Write validate-spec.py**

```python
#!/usr/bin/env python3
"""Validate ADK project spec completeness."""

import sys
import re
from pathlib import Path

REQUIRED_SECTIONS = [
    "## Overview",
    "## Agent Architecture",
    "## Tools Required",
    "## Deployment Target",
]

OPTIONAL_SECTIONS = [
    "## Behavior Configuration",
    "## Open Questions",
    "## Decisions Made",
]


def validate_spec(spec_path: str) -> tuple[bool, list[str]]:
    """Validate spec file and return (is_valid, issues)."""
    issues = []
    path = Path(spec_path)

    if not path.exists():
        return False, [f"Spec file not found: {spec_path}"]

    content = path.read_text()

    # Check required sections
    for section in REQUIRED_SECTIONS:
        if section not in content:
            issues.append(f"Missing required section: {section}")

    # Check for unchecked critical items
    if "Agent Type | [ ]" in content:
        issues.append("Agent Type not selected")

    if "Model | [ ]" in content:
        issues.append("Model not selected")

    # Check for empty overview
    overview_match = re.search(r"## Overview\n\n<!-- .* -->\n\n", content)
    if overview_match:
        issues.append("Overview section is empty (only contains placeholder)")

    # Check for placeholder content
    if "{{" in content and "}}" in content:
        issues.append("Unreplaced template placeholders found")

    return len(issues) == 0, issues


def main():
    if len(sys.argv) < 2:
        print("Usage: validate-spec.py <path/to/spec.md>")
        sys.exit(1)

    spec_path = sys.argv[1]
    is_valid, issues = validate_spec(spec_path)

    if is_valid:
        print("✓ Spec validation passed")
        sys.exit(0)
    else:
        print("✗ Spec validation failed:")
        for issue in issues:
            print(f"  - {issue}")
        sys.exit(1)


if __name__ == "__main__":
    main()
```

**Step 2: Make executable**

```bash
chmod +x /Users/mac-main/agentic-plugins/adk-builder/scripts/validate-spec.py
```

**Step 3: Commit**

```bash
git add scripts/validate-spec.py
git commit -m "feat: add validate-spec.py for spec completeness checking"
```

---

## Phase 5: Update Plugin Manifest and Documentation

### Task 5.1: Update plugin.json

**Files:**
- Modify: `.claude-plugin/plugin.json`

**Step 1: Update plugin.json with new structure**

```json
{
  "name": "adk-builder",
  "version": "3.0.0",
  "description": "Unified Google ADK development with spec-driven workflows, mode-based orchestration, and consolidated knowledge base",
  "author": {
    "name": "ADK Builder Contributors"
  },
  "keywords": ["adk", "google", "agents", "gemini", "vertex-ai", "spec-driven"],
  "commands": "./commands",
  "skills": "./skills",
  "scripts": "./scripts"
}
```

**Step 2: Commit**

```bash
git add .claude-plugin/plugin.json
git commit -m "chore: update plugin.json for v3.0.0"
```

---

### Task 5.2: Update README.md

**Files:**
- Modify: `README.md`

**Step 1: Write new README**

```markdown
# ADK Builder

A Claude Code plugin for building Google Agent Development Kit applications with spec-driven workflows and unified orchestration.

## Installation

```bash
# Add marketplace
/plugin marketplace add MattMagg/agentic-plugins

# Install plugin
/plugin install adk-builder@agentic-plugins
```

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
```

**Step 2: Commit**

```bash
git add README.md
git commit -m "docs: update README for v3.0.0 architecture"
```

---

### Task 5.3: Final Verification and Push

**Step 1: Verify final structure**

```bash
cd /Users/mac-main/agentic-plugins/adk-builder
echo "=== Commands ===" && ls commands/
echo "=== Skills ===" && ls skills/
echo "=== Scripts ===" && ls scripts/
echo "=== Plugin ===" && cat .claude-plugin/plugin.json
```

Expected:
- Commands: adk.md, adk-debug.md, CLAUDE.md
- Skills: adk-advanced, adk-behavior, adk-core, adk-orchestration, adk-production, adk-tools
- Scripts: init-spec.sh, validate-spec.py
- Plugin: version 3.0.0

**Step 2: Run git status**

```bash
git status
```

Expected: Clean working tree or only untracked docs/plans/

**Step 3: Push to remote**

```bash
git push origin main
```

**Step 4: Commit plan file**

```bash
git add docs/plans/
git commit -m "docs: add plugin redesign implementation plan"
git push origin main
```

---

## Summary

| Phase | Tasks | Files Changed |
|-------|-------|---------------|
| Phase 1: Cleanup | 2 | Remove 14 files |
| Phase 2: Commands | 2 | Create 2 files |
| Phase 3: Skills | 6 | Consolidate 11 → 6 |
| Phase 4: Scripts | 2 | Create 2 files |
| Phase 5: Docs | 3 | Update 3 files |

**Total commits**: ~15 atomic commits
**Net file reduction**: ~30 files removed, 6 added
