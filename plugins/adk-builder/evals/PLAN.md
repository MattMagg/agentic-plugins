# ADK-Builder Plugin Evaluation Framework Plan

## Executive Summary

This plan creates a rigorous evaluation framework for the `adk-builder` Claude Code plugin. The framework uses Claude Code to test itself via programmatic SDK invocation, hook-based validation, and multi-agent eval patterns.

**Key Insight from Research:** No dedicated plugin evaluation framework exists in the ecosystem. This will be the first purpose-built solution.

---

## Phase 0: Documentation Discovery (COMPLETED)

### Allowed APIs

| API | Source | Purpose |
|-----|--------|---------|
| `claude -p "prompt"` | CLI Reference | One-shot headless execution |
| `claude --output-format json` | CLI Reference | Structured output with session_id, usage, result |
| `claude --allowedTools "..."` | CLI Reference | Auto-approve specific tools |
| `claude --resume "session_id"` | CLI Reference | Continue previous session |
| `claude --append-system-prompt` | CLI Reference | Add eval instructions without replacing defaults |
| `claude --max-turns N` | CLI Reference | Limit conversation turns |
| `claude-agent-sdk.query()` | Agent SDK | Python programmatic invocation |
| `AgentDefinition` | Agent SDK | Subagent configuration |
| `Stop` hook | Hooks Reference | Block completion until criteria met |
| `PostToolUse` hook | Hooks Reference | Validate tool results |
| `SessionStart` hook | Hooks Reference | Initialize eval context |
| `.mcp.json` | MCP Docs | Configure MCP servers per project |

### Anti-Patterns (DO NOT USE)

| Pattern | Why It Fails |
|---------|-------------|
| `--dangerously-skip-permissions` in automated evals | Security risk; use `--allowedTools` instead |
| Recursive subagent spawning | Subagents cannot spawn subagents (Task forbidden) |
| Guessing tool names | Use exact tool names from CLI docs |
| Using MCP for inter-session state | MCP servers don't share state across sessions |
| `claude -i` or `claude --interactive` | These flags don't exist |

### Copy-Ready Reference Locations

| Use Case | Location |
|----------|----------|
| JSON output parsing | CLI Reference → "Output formats" section |
| Hook configuration | `.claude/settings.json` hooks field |
| Python SDK streaming | Agent SDK → "Streaming responses" section |
| Session continuation | CLI Reference → "Continue vs Resume" section |
| Plugin loading | `claude --plugin-dir /path` during development |

---

## Phase 1: Evaluation Infrastructure Setup

### Objective
Create the foundational directory structure, configuration files, and base utilities for running evaluations.

### Tasks

#### 1.1 Create Directory Structure
```
plugins/adk-builder/evals/
├── PLAN.md                    # This file
├── datasets/                  # Evaluation prompts and expected behaviors
│   ├── command-activation.jsonl
│   ├── spec-mode.jsonl
│   ├── plan-mode.jsonl
│   ├── build-mode.jsonl
│   └── skill-loading.jsonl
├── runners/                   # Evaluation execution scripts
│   ├── run_eval.py           # Main Python eval runner
│   ├── run_eval.sh           # Bash wrapper for CI
│   └── helpers.py            # Shared utilities
├── hooks/                     # Validation hooks for evaluations
│   ├── eval_stop_hook.py     # Enforce completion criteria
│   ├── eval_post_tool.py     # Validate tool outputs
│   └── eval_session_start.py # Initialize eval context
├── results/                   # Eval outputs (gitignored)
│   └── .gitkeep
├── reports/                   # Generated reports
│   └── .gitkeep
└── .claude/
    └── settings.json         # Eval-specific Claude settings
```

#### 1.2 Create Eval Runner (Python SDK)

**File:** `evals/runners/run_eval.py`

```python
#!/usr/bin/env python3
"""
ADK-Builder Plugin Evaluation Runner

Uses Claude Agent SDK to programmatically run evaluation sessions.
"""

import asyncio
import json
import sys
from pathlib import Path
from dataclasses import dataclass
from typing import AsyncIterator, Optional

# NOTE: Requires `pip install claude-agent-sdk`
from claude_agent_sdk import query, ClaudeAgentOptions


@dataclass
class EvalCase:
    """Single evaluation test case."""
    id: str
    prompt: str
    expected_behaviors: list[str]
    max_turns: int = 10
    allowed_tools: list[str] = None


@dataclass
class EvalResult:
    """Result from a single evaluation."""
    case_id: str
    session_id: str
    success: bool
    behaviors_found: list[str]
    behaviors_missing: list[str]
    result_text: str
    token_usage: dict
    error: Optional[str] = None


async def run_single_eval(case: EvalCase) -> EvalResult:
    """Run a single evaluation case."""

    behaviors_found = []
    result_text = ""
    session_id = None
    token_usage = {}

    try:
        async for message in query(
            prompt=case.prompt,
            options=ClaudeAgentOptions(
                allowed_tools=case.allowed_tools or ["Read", "Write", "Glob", "Grep", "Bash"],
                # Load the plugin from parent directory
                # plugin_dir=str(Path(__file__).parent.parent.parent),
            )
        ):
            # Capture session ID
            if hasattr(message, 'session_id'):
                session_id = message.session_id

            # Capture result
            if hasattr(message, 'result'):
                result_text = message.result

            # Capture usage
            if hasattr(message, 'usage'):
                token_usage = message.usage

        # Check expected behaviors
        for behavior in case.expected_behaviors:
            if behavior_detected(behavior, result_text):
                behaviors_found.append(behavior)

        behaviors_missing = [b for b in case.expected_behaviors if b not in behaviors_found]

        return EvalResult(
            case_id=case.id,
            session_id=session_id or "unknown",
            success=len(behaviors_missing) == 0,
            behaviors_found=behaviors_found,
            behaviors_missing=behaviors_missing,
            result_text=result_text,
            token_usage=token_usage,
        )

    except Exception as e:
        return EvalResult(
            case_id=case.id,
            session_id="error",
            success=False,
            behaviors_found=[],
            behaviors_missing=case.expected_behaviors,
            result_text="",
            token_usage={},
            error=str(e),
        )


def behavior_detected(behavior: str, result: str) -> bool:
    """Check if a behavior is present in the result."""
    # Simple keyword matching - extend for complex behaviors
    behavior_checks = {
        "spec_mode_entered": "Mode: SPEC" in result or "SPEC Mode" in result,
        "plan_mode_entered": "Mode: PLAN" in result or "PLAN Mode" in result,
        "build_mode_entered": "Mode: BUILD" in result or "BUILD Mode" in result,
        "state_file_created": "adk-builder.local.md" in result,
        "spec_file_created": "spec.md" in result,
        "skill_loaded": "@adk-" in result,
        "error_handled_gracefully": "Error" not in result or "handled" in result.lower(),
        "clarifying_question_asked": "?" in result,
    }
    return behavior_checks.get(behavior, behavior.lower() in result.lower())


async def run_dataset(dataset_path: Path) -> list[EvalResult]:
    """Run all cases in a dataset file."""
    results = []

    with open(dataset_path) as f:
        for line in f:
            if not line.strip():
                continue
            case_data = json.loads(line)
            case = EvalCase(**case_data)
            result = await run_single_eval(case)
            results.append(result)
            print(f"  [{'+' if result.success else '-'}] {case.id}")

    return results


def generate_report(results: list[EvalResult], output_path: Path):
    """Generate a markdown report from results."""
    total = len(results)
    passed = sum(1 for r in results if r.success)

    report = f"""# ADK-Builder Evaluation Report

**Date:** {__import__('datetime').datetime.now().isoformat()}
**Total Cases:** {total}
**Passed:** {passed}
**Failed:** {total - passed}
**Pass Rate:** {passed/total*100:.1f}%

## Summary

| Case ID | Status | Behaviors Found | Behaviors Missing |
|---------|--------|-----------------|-------------------|
"""

    for r in results:
        status = "✅" if r.success else "❌"
        found = ", ".join(r.behaviors_found) or "none"
        missing = ", ".join(r.behaviors_missing) or "none"
        report += f"| {r.case_id} | {status} | {found} | {missing} |\n"

    report += "\n## Detailed Results\n\n"

    for r in results:
        report += f"### {r.case_id}\n\n"
        report += f"- **Session ID:** `{r.session_id}`\n"
        report += f"- **Success:** {r.success}\n"
        if r.error:
            report += f"- **Error:** {r.error}\n"
        report += f"- **Token Usage:** {r.token_usage}\n"
        report += f"\n<details><summary>Result Text</summary>\n\n```\n{r.result_text[:2000]}...\n```\n</details>\n\n"

    output_path.write_text(report)
    print(f"Report written to {output_path}")


async def main():
    """Main entry point."""
    datasets_dir = Path(__file__).parent.parent / "datasets"
    reports_dir = Path(__file__).parent.parent / "reports"
    reports_dir.mkdir(exist_ok=True)

    all_results = []

    for dataset_file in sorted(datasets_dir.glob("*.jsonl")):
        print(f"\nRunning: {dataset_file.name}")
        results = await run_dataset(dataset_file)
        all_results.extend(results)

    if all_results:
        report_path = reports_dir / f"eval-{__import__('datetime').date.today()}.md"
        generate_report(all_results, report_path)

    # Exit with error if any failed
    failed = sum(1 for r in all_results if not r.success)
    sys.exit(1 if failed > 0 else 0)


if __name__ == "__main__":
    asyncio.run(main())
```

#### 1.3 Create Evaluation Datasets

**File:** `evals/datasets/command-activation.jsonl`
```json
{"id": "adk_basic_invoke", "prompt": "/adk", "expected_behaviors": ["state_detected", "mode_announced"]}
{"id": "adk_with_feature", "prompt": "/adk weather-agent", "expected_behaviors": ["spec_mode_entered", "feature_named"]}
{"id": "adk_force_spec", "prompt": "/adk --spec", "expected_behaviors": ["spec_mode_entered"]}
{"id": "adk_force_plan", "prompt": "/adk --plan", "expected_behaviors": ["plan_mode_entered"]}
{"id": "adk_debug", "prompt": "/adk-debug", "expected_behaviors": ["debug_mode_entered"]}
```

**File:** `evals/datasets/spec-mode.jsonl`
```json
{"id": "spec_creates_file", "prompt": "/adk test-agent", "expected_behaviors": ["spec_file_created", "clarifying_question_asked"]}
{"id": "spec_asks_questions", "prompt": "/adk customer-support", "expected_behaviors": ["clarifying_question_asked", "requirement_recorded"]}
{"id": "spec_references_skills", "prompt": "/adk multi-agent-system", "expected_behaviors": ["skill_referenced"]}
```

**File:** `evals/datasets/skill-loading.jsonl`
```json
{"id": "loads_adk_core", "prompt": "/adk new-project --spec\nI want a basic greeting agent", "expected_behaviors": ["skill_loaded", "adk_core_referenced"]}
{"id": "loads_adk_tools", "prompt": "/adk tool-agent --spec\nI need an agent that uses external APIs", "expected_behaviors": ["adk_tools_referenced"]}
{"id": "loads_adk_orchestration", "prompt": "/adk multi-agent --spec\nI want multiple agents working together", "expected_behaviors": ["adk_orchestration_referenced"]}
```

#### 1.4 Create Validation Hooks

**File:** `evals/hooks/eval_stop_hook.py`
```python
#!/usr/bin/env python3
"""
Stop hook for evaluation - blocks completion until criteria met.
"""
import json
import os
import sys

def main():
    # Read hook input from stdin
    input_data = json.load(sys.stdin)

    # Get the result text from the session
    result = input_data.get("result", "")

    # Check for required completion markers
    required_markers = os.environ.get("EVAL_REQUIRED_MARKERS", "").split(",")

    missing = [m for m in required_markers if m and m not in result]

    if missing:
        output = {
            "decision": "block",
            "reason": f"Missing required markers: {', '.join(missing)}"
        }
    else:
        output = {"decision": "approve"}

    print(json.dumps(output))


if __name__ == "__main__":
    main()
```

**File:** `evals/hooks/eval_post_tool.py`
```python
#!/usr/bin/env python3
"""
PostToolUse hook - validates tool outputs during evaluation.
"""
import json
import sys

def main():
    input_data = json.load(sys.stdin)

    tool_name = input_data.get("tool_name", "")
    tool_result = input_data.get("result", "")

    # Track tool usage for evaluation metrics
    eval_log_path = ".claude/eval_tool_log.jsonl"

    with open(eval_log_path, "a") as f:
        log_entry = {
            "tool": tool_name,
            "result_length": len(str(tool_result)),
            "success": "error" not in str(tool_result).lower()
        }
        f.write(json.dumps(log_entry) + "\n")

    # Always approve (just logging)
    print(json.dumps({"decision": "approve"}))


if __name__ == "__main__":
    main()
```

#### 1.5 Create Eval-Specific Settings

**File:** `evals/.claude/settings.json`
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": ".*",
        "hooks": [
          {
            "type": "command",
            "command": "python ../hooks/eval_post_tool.py"
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python ../hooks/eval_stop_hook.py"
          }
        ]
      }
    ]
  }
}
```

### Verification Checklist
- [ ] Directory structure created matching specification
- [ ] `run_eval.py` runs without import errors: `python -c "import evals.runners.run_eval"`
- [ ] Hook scripts are executable: `chmod +x evals/hooks/*.py`
- [ ] Dataset files are valid JSONL: `cat datasets/*.jsonl | python -m json.tool --no-indent`
- [ ] Settings.json is valid JSON: `python -m json.tool evals/.claude/settings.json`

---

## Phase 2: CLI-Based Evaluation Runner

### Objective
Create a bash-based runner that uses `claude -p` for evaluation, suitable for CI/CD and environments without Python SDK.

### Tasks

#### 2.1 Create Bash Eval Runner

**File:** `evals/runners/run_eval.sh`
```bash
#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EVALS_DIR="$(dirname "$SCRIPT_DIR")"
PLUGIN_DIR="$(dirname "$EVALS_DIR")"
RESULTS_DIR="$EVALS_DIR/results"
REPORTS_DIR="$EVALS_DIR/reports"

# Ensure directories exist
mkdir -p "$RESULTS_DIR" "$REPORTS_DIR"

# Timestamp for this run
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
RESULT_FILE="$RESULTS_DIR/run_$TIMESTAMP.jsonl"
REPORT_FILE="$REPORTS_DIR/report_$TIMESTAMP.md"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

total=0
passed=0
failed=0

run_eval_case() {
    local id="$1"
    local prompt="$2"
    local expected="$3"

    echo -n "  [$id] "

    # Run Claude with the plugin loaded
    result=$(claude -p "$prompt" \
        --plugin-dir "$PLUGIN_DIR" \
        --allowedTools "Read,Write,Glob,Grep,Bash" \
        --output-format json \
        --max-turns 5 \
        2>/dev/null || echo '{"error": "execution failed"}')

    # Extract result text
    result_text=$(echo "$result" | jq -r '.result // ""')
    session_id=$(echo "$result" | jq -r '.session_id // "unknown"')

    # Check expected behaviors (simple substring match)
    local all_found=true
    for behavior in $(echo "$expected" | tr ',' '\n'); do
        if [[ ! "$result_text" == *"$behavior"* ]]; then
            all_found=false
            break
        fi
    done

    # Log result
    echo "{\"id\": \"$id\", \"session_id\": \"$session_id\", \"success\": $all_found}" >> "$RESULT_FILE"

    if $all_found; then
        echo -e "${GREEN}PASS${NC}"
        ((passed++))
    else
        echo -e "${RED}FAIL${NC}"
        ((failed++))
    fi

    ((total++))
}

# Header
echo "================================"
echo "ADK-Builder Evaluation Runner"
echo "================================"
echo ""
echo "Plugin: $PLUGIN_DIR"
echo "Results: $RESULT_FILE"
echo ""

# Run datasets
for dataset in "$EVALS_DIR/datasets/"*.jsonl; do
    echo "Running: $(basename "$dataset")"

    while IFS= read -r line; do
        [[ -z "$line" ]] && continue

        id=$(echo "$line" | jq -r '.id')
        prompt=$(echo "$line" | jq -r '.prompt')
        expected=$(echo "$line" | jq -r '.expected_behaviors | join(",")')

        run_eval_case "$id" "$prompt" "$expected"
    done < "$dataset"

    echo ""
done

# Summary
echo "================================"
echo "Summary"
echo "================================"
echo "Total:  $total"
echo -e "Passed: ${GREEN}$passed${NC}"
echo -e "Failed: ${RED}$failed${NC}"
echo "Pass Rate: $(echo "scale=1; $passed * 100 / $total" | bc)%"
echo ""

# Generate markdown report
cat > "$REPORT_FILE" << EOF
# ADK-Builder Evaluation Report

**Date:** $(date -Iseconds)
**Total Cases:** $total
**Passed:** $passed
**Failed:** $failed
**Pass Rate:** $(echo "scale=1; $passed * 100 / $total" | bc)%

## Results

$(cat "$RESULT_FILE" | while read line; do
    id=$(echo "$line" | jq -r '.id')
    success=$(echo "$line" | jq -r '.success')
    status="❌"
    [[ "$success" == "true" ]] && status="✅"
    echo "- $status $id"
done)
EOF

echo "Report: $REPORT_FILE"

# Exit with failure if any tests failed
[[ $failed -gt 0 ]] && exit 1
exit 0
```

#### 2.2 Create CI Integration

**File:** `evals/.github/workflows/plugin-eval.yml`
```yaml
name: Plugin Evaluation

on:
  push:
    paths:
      - 'plugins/adk-builder/**'
  pull_request:
    paths:
      - 'plugins/adk-builder/**'
  workflow_dispatch:

jobs:
  evaluate:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Install Claude Code
        run: |
          curl -fsSL https://claude.ai/install.sh | bash
          echo "$HOME/.claude/bin" >> $GITHUB_PATH

      - name: Set up API key
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          echo "ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY" >> $GITHUB_ENV

      - name: Run evaluations
        run: |
          cd plugins/adk-builder
          chmod +x evals/runners/run_eval.sh
          ./evals/runners/run_eval.sh

      - name: Upload results
        uses: actions/upload-artifact@v4
        with:
          name: eval-results
          path: plugins/adk-builder/evals/reports/
```

### Verification Checklist
- [ ] `run_eval.sh` is executable: `chmod +x evals/runners/run_eval.sh`
- [ ] Script runs without errors: `./evals/runners/run_eval.sh` (with `ANTHROPIC_API_KEY` set)
- [ ] Results file created in `evals/results/`
- [ ] Report file created in `evals/reports/`
- [ ] Exit code is 0 when all pass, 1 when any fail

---

## Phase 3: Multi-Agent Evaluation Subagents

### Objective
Create specialized subagents for different aspects of plugin evaluation, enabling parallel and thorough testing.

### Tasks

#### 3.1 Create Eval Coordinator Agent

**File:** `evals/agents/eval-coordinator.md`
```yaml
---
name: eval-coordinator
description: Orchestrates evaluation of the adk-builder plugin by delegating to specialized eval agents
allowedTools:
  - Read
  - Glob
  - Grep
  - Task
---
# Eval Coordinator

You orchestrate comprehensive evaluation of the adk-builder plugin.

## Evaluation Flow

1. **Discovery Phase**: Identify all commands, skills, and modes to test
2. **Delegation Phase**: Spawn specialized eval agents for each aspect
3. **Collection Phase**: Gather results from all agents
4. **Reporting Phase**: Synthesize findings into final report

## Agents to Deploy

- `command-eval-agent`: Tests slash command activation and routing
- `mode-eval-agent`: Tests SPEC/PLAN/BUILD mode transitions
- `skill-eval-agent`: Tests skill loading and reference accuracy
- `error-eval-agent`: Tests error handling and graceful degradation

## Report Structure

After all agents complete, synthesize into:

```markdown
# Plugin Evaluation Summary

## Command Activation Rate
- /adk: X/Y successful
- /adk-debug: X/Y successful

## Mode Transition Accuracy
- SPEC mode: X/Y correct behaviors
- PLAN mode: X/Y correct behaviors
- BUILD mode: X/Y correct behaviors

## Skill Loading Success
- @adk-core: X/Y loaded correctly
- @adk-tools: X/Y loaded correctly
...

## Error Handling
- Graceful failures: X/Y
- Helpful messages: X/Y

## Overall Score: X%
```
```

#### 3.2 Create Command Eval Agent

**File:** `evals/agents/command-eval-agent.md`
```yaml
---
name: command-eval-agent
description: Evaluates slash command activation and response accuracy
allowedTools:
  - Read
  - Glob
  - Grep
  - Bash
---
# Command Evaluation Agent

You test that adk-builder slash commands activate correctly and produce expected outputs.

## Test Protocol

For each command:

1. **Invoke** the command with test input
2. **Verify** the expected mode is entered
3. **Check** for required output markers
4. **Record** pass/fail with evidence

## Commands to Test

1. `/adk` - Should detect state and announce mode
2. `/adk <feature-name>` - Should enter SPEC mode with feature context
3. `/adk --spec` - Should force SPEC mode
4. `/adk --plan` - Should force PLAN mode
5. `/adk --debug` - Should provide debug output
6. `/adk-debug` - Should enter debug workflow

## Expected Behaviors

| Command | Expected Output Contains |
|---------|-------------------------|
| `/adk` | "Current State", "Mode:" |
| `/adk test` | "SPEC", "test" |
| `/adk --plan` | "PLAN" |

## Report Format

```json
{
  "command": "/adk",
  "input": "test-agent",
  "expected": ["SPEC", "test-agent"],
  "found": ["SPEC", "test-agent"],
  "passed": true
}
```
```

#### 3.3 Create Mode Transition Agent

**File:** `evals/agents/mode-eval-agent.md`
```yaml
---
name: mode-eval-agent
description: Evaluates SPEC/PLAN/BUILD mode transitions and state management
allowedTools:
  - Read
  - Write
  - Glob
  - Bash
---
# Mode Transition Evaluation Agent

You test that adk-builder correctly transitions between SPEC, PLAN, and BUILD modes.

## Test Scenarios

### Scenario 1: Fresh Start → SPEC
1. Ensure no existing state file
2. Run `/adk new-feature`
3. Verify SPEC mode entered
4. Verify spec.md created

### Scenario 2: SPEC → PLAN
1. Create minimal spec.md
2. Run `/adk --plan`
3. Verify PLAN mode entered
4. Verify plan.md created

### Scenario 3: PLAN → BUILD
1. Create minimal plan.md
2. Run `/adk` (should auto-detect)
3. Verify BUILD mode entered
4. Verify progress tracking starts

### Scenario 4: Resume Session
1. Create state file with partial progress
2. Run `/adk`
3. Verify session resumed at correct step

## State File Verification

Check `.claude/adk-builder.local.md` contains:
- `current_feature`
- `phase`
- `last_completed_step` (if applicable)

## Report Format

```json
{
  "scenario": "fresh_to_spec",
  "steps": [
    {"action": "clear state", "success": true},
    {"action": "run /adk", "success": true},
    {"action": "verify SPEC mode", "success": true}
  ],
  "passed": true
}
```
```

#### 3.4 Create Skill Loading Agent

**File:** `evals/agents/skill-eval-agent.md`
```yaml
---
name: skill-eval-agent
description: Evaluates that skills load correctly and contain accurate information
allowedTools:
  - Read
  - Glob
  - Grep
---
# Skill Loading Evaluation Agent

You verify that adk-builder skills load correctly and provide accurate, up-to-date information.

## Skills to Evaluate

| Skill | Expected Content |
|-------|-----------------|
| @adk-core | LlmAgent, BaseAgent, project setup |
| @adk-tools | FunctionTool, MCP, OpenAPI |
| @adk-behavior | callbacks, state, events |
| @adk-orchestration | SequentialAgent, ParallelAgent |
| @adk-production | deployment, guardrails, evals |
| @adk-advanced | ThinkingConfig, visual builder |

## Verification Process

For each skill:

1. **Locate** the skill file in `skills/` directory
2. **Read** the skill content
3. **Verify** required topics are covered
4. **Check** code examples are syntactically valid
5. **Validate** referenced APIs exist in official docs

## Accuracy Checks

- No deprecated APIs (e.g., old import paths)
- Correct parameter names in examples
- Valid Python syntax in code blocks
- Consistent with Google ADK documentation

## Report Format

```json
{
  "skill": "@adk-core",
  "file": "skills/adk-core/SKILL.md",
  "topics_found": ["LlmAgent", "BaseAgent", "project_setup"],
  "topics_missing": [],
  "syntax_errors": [],
  "accuracy_score": 1.0
}
```
```

### Verification Checklist
- [ ] All agent files created in `evals/agents/`
- [ ] Agent YAML frontmatter is valid
- [ ] Agents have clear, distinct responsibilities
- [ ] Agents do NOT include `Task` in their tools (no recursive spawning)
- [ ] Report formats are consistent JSON

---

## Phase 4: Self-Improving Evaluation Loop

### Objective
Create a continuous evaluation loop where Claude Code tests itself, identifies failures, and suggests improvements.

### Tasks

#### 4.1 Create Ralph Loop Runner

**File:** `evals/runners/ralph_loop.sh`
```bash
#!/bin/bash
# Ralph Loop: Self-improving evaluation cycle
# Named after the pattern from Claude Code community

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EVALS_DIR="$(dirname "$SCRIPT_DIR")"
PLUGIN_DIR="$(dirname "$EVALS_DIR")"

MAX_ITERATIONS=5
ITERATION=0
COMPLETE_MARKER="ALL_EVALS_PASSED"

echo "Starting Ralph Loop evaluation..."
echo "Max iterations: $MAX_ITERATIONS"
echo ""

while [ $ITERATION -lt $MAX_ITERATIONS ]; do
    ITERATION=$((ITERATION + 1))
    echo "=== Iteration $ITERATION ==="

    # Run evaluation and capture result
    RESULT=$(claude -p "
You are evaluating the adk-builder plugin.

1. Read the current state from evals/results/loop_state.md (if exists)
2. Run the command-activation.jsonl evaluations
3. Document any failures in evals/results/loop_state.md
4. If all pass, write '$COMPLETE_MARKER' to evals/results/loop_state.md
5. If failures exist, analyze and suggest fixes

Current iteration: $ITERATION of $MAX_ITERATIONS
" \
        --plugin-dir "$PLUGIN_DIR" \
        --allowedTools "Read,Write,Glob,Grep,Bash" \
        --append-system-prompt "Focus on fixing failures, not adding features. Be minimal." \
        --max-turns 10 \
        --output-format json \
        2>/dev/null || echo '{"result": "error"}')

    # Check for completion marker
    if grep -q "$COMPLETE_MARKER" "$EVALS_DIR/results/loop_state.md" 2>/dev/null; then
        echo ""
        echo "✅ All evaluations passed after $ITERATION iterations"
        exit 0
    fi

    echo "Iteration $ITERATION complete - continuing..."
    echo ""
    sleep 2
done

echo ""
echo "❌ Max iterations reached without full pass"
exit 1
```

#### 4.2 Create Eval Improvement Agent

**File:** `evals/agents/eval-improver.md`
```yaml
---
name: eval-improver
description: Analyzes evaluation failures and suggests concrete fixes
allowedTools:
  - Read
  - Glob
  - Grep
---
# Eval Improvement Agent

You analyze evaluation failures and suggest specific, actionable fixes.

## Input

You receive evaluation results showing:
- Which test cases failed
- What behaviors were expected vs found
- The actual output from the plugin

## Analysis Process

1. **Categorize** failures by type:
   - Command not recognized
   - Wrong mode entered
   - Missing output markers
   - Skill not loaded
   - Error in execution

2. **Trace** root cause:
   - Is the command file correct?
   - Is the mode detection logic flawed?
   - Are the expected behaviors realistic?

3. **Propose** fixes:
   - Specific file + line changes
   - New test cases if expectations are wrong
   - Documentation updates if behavior is correct

## Output Format

```markdown
## Failure Analysis

### Failure 1: adk_basic_invoke
**Expected:** mode_announced
**Got:** (no output)
**Root Cause:** Command not found in plugin
**Fix:** Verify commands/adk.md exists and is properly formatted

### Failure 2: spec_creates_file
**Expected:** spec_file_created
**Got:** "Mode: SPEC" but no file
**Root Cause:** SPEC mode doesn't auto-create file on first run
**Fix:** Update commands/adk.md line 25-30 to create spec file

## Suggested Fixes (Priority Order)

1. [HIGH] Fix command loading - check plugin.json commands path
2. [MED] Update SPEC mode to create spec file immediately
3. [LOW] Add more descriptive output markers
```
```

### Verification Checklist
- [ ] Ralph loop script is executable
- [ ] Loop correctly detects completion marker
- [ ] Loop respects max iterations
- [ ] Improvement agent provides actionable suggestions
- [ ] State file tracks progress across iterations

---

## Phase 5: Comprehensive Test Datasets

### Objective
Create thorough evaluation datasets covering edge cases, error conditions, and real-world usage patterns.

### Tasks

#### 5.1 Create Edge Case Dataset

**File:** `evals/datasets/edge-cases.jsonl`
```json
{"id": "empty_feature_name", "prompt": "/adk ''", "expected_behaviors": ["error_handled", "helpful_message"]}
{"id": "special_chars_feature", "prompt": "/adk my-agent_v2.0", "expected_behaviors": ["spec_mode_entered", "feature_named"]}
{"id": "very_long_feature", "prompt": "/adk this-is-a-very-long-feature-name-that-exceeds-normal-limits", "expected_behaviors": ["spec_mode_entered"]}
{"id": "unicode_feature", "prompt": "/adk café-agent", "expected_behaviors": ["spec_mode_entered"]}
{"id": "conflicting_flags", "prompt": "/adk --spec --plan", "expected_behaviors": ["error_handled", "flag_conflict_noted"]}
{"id": "nonexistent_feature_resume", "prompt": "/adk nonexistent-feature --plan", "expected_behaviors": ["error_handled", "no_spec_found"]}
{"id": "corrupted_state_file", "prompt": "/adk", "expected_behaviors": ["state_recovered", "mode_announced"], "setup": "create corrupted .claude/adk-builder.local.md"}
```

#### 5.2 Create Workflow Integration Dataset

**File:** `evals/datasets/workflow-integration.jsonl`
```json
{"id": "full_spec_to_plan", "prompt": "/adk weather-agent\nI want an agent that provides weather information for a given city\nIt should use the OpenWeatherMap API\nYes, that's all\n/adk --plan", "expected_behaviors": ["spec_completed", "plan_generated"]}
{"id": "plan_to_build", "prompt": "/adk test-agent --plan\nNow let's build it\n/adk", "expected_behaviors": ["build_mode_entered", "step_tracking_started"]}
{"id": "mid_build_interrupt", "prompt": "/adk\nSTOP", "expected_behaviors": ["progress_saved", "state_preserved"]}
{"id": "resume_after_interrupt", "prompt": "/adk", "expected_behaviors": ["session_resumed", "correct_step"]}
```

#### 5.3 Create Skill Accuracy Dataset

**File:** `evals/datasets/skill-accuracy.jsonl`
```json
{"id": "adk_core_llmagent", "prompt": "Using @adk-core, show me how to create an LlmAgent", "expected_behaviors": ["LlmAgent_import", "correct_constructor"]}
{"id": "adk_tools_function", "prompt": "Using @adk-tools, show me how to create a FunctionTool", "expected_behaviors": ["FunctionTool_import", "decorator_usage"]}
{"id": "adk_orchestration_sequential", "prompt": "Using @adk-orchestration, show me SequentialAgent", "expected_behaviors": ["SequentialAgent_import", "sub_agents_param"]}
{"id": "adk_production_guardrails", "prompt": "Using @adk-production, show me how to add guardrails", "expected_behaviors": ["guardrail_callback", "before_model_call"]}
```

#### 5.4 Create Error Recovery Dataset

**File:** `evals/datasets/error-recovery.jsonl`
```json
{"id": "missing_api_key", "prompt": "/adk\nBuild the agent now", "expected_behaviors": ["auth_error_detected", "helpful_fix_suggested"]}
{"id": "invalid_python_syntax", "prompt": "/adk\nHere's my code: def broken(:", "expected_behaviors": ["syntax_error_caught", "correction_suggested"]}
{"id": "import_error", "prompt": "/adk\nfrom nonexistent import thing", "expected_behaviors": ["import_error_caught", "alternatives_suggested"]}
{"id": "network_timeout", "prompt": "/adk\nFetch from http://timeout.test", "expected_behaviors": ["timeout_handled", "retry_suggested"]}
```

### Verification Checklist
- [ ] All JSONL files are valid: `cat *.jsonl | python -m json.tool`
- [ ] Edge cases cover boundary conditions
- [ ] Workflow tests cover realistic user journeys
- [ ] Skill accuracy tests verify actual ADK patterns
- [ ] Error recovery tests cover common failure modes

---

## Phase 6: Metrics and Reporting

### Objective
Create comprehensive metrics collection and reporting for continuous monitoring of plugin quality.

### Tasks

#### 6.1 Create Metrics Collector

**File:** `evals/runners/metrics.py`
```python
#!/usr/bin/env python3
"""
Metrics collector for adk-builder evaluations.
"""

import json
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional


@dataclass
class EvalMetrics:
    """Comprehensive evaluation metrics."""
    timestamp: str

    # Activation metrics
    command_activation_rate: float
    skill_activation_rate: float

    # Accuracy metrics
    mode_transition_accuracy: float
    skill_content_accuracy: float
    output_format_compliance: float

    # Error handling
    graceful_error_rate: float
    helpful_message_rate: float

    # Performance
    avg_turns_to_complete: float
    avg_token_usage: int

    # Overall
    overall_pass_rate: float

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2)

    @classmethod
    def from_results(cls, results: list[dict]) -> 'EvalMetrics':
        """Compute metrics from raw evaluation results."""

        total = len(results)
        if total == 0:
            return cls(
                timestamp=datetime.now().isoformat(),
                command_activation_rate=0.0,
                skill_activation_rate=0.0,
                mode_transition_accuracy=0.0,
                skill_content_accuracy=0.0,
                output_format_compliance=0.0,
                graceful_error_rate=0.0,
                helpful_message_rate=0.0,
                avg_turns_to_complete=0.0,
                avg_token_usage=0,
                overall_pass_rate=0.0
            )

        # Count by category
        command_tests = [r for r in results if r.get('category') == 'command']
        skill_tests = [r for r in results if r.get('category') == 'skill']
        mode_tests = [r for r in results if r.get('category') == 'mode']
        error_tests = [r for r in results if r.get('category') == 'error']

        def pass_rate(tests):
            if not tests:
                return 1.0
            return sum(1 for t in tests if t.get('success')) / len(tests)

        return cls(
            timestamp=datetime.now().isoformat(),
            command_activation_rate=pass_rate(command_tests),
            skill_activation_rate=pass_rate(skill_tests),
            mode_transition_accuracy=pass_rate(mode_tests),
            skill_content_accuracy=pass_rate([r for r in skill_tests if 'accuracy' in r.get('id', '')]),
            output_format_compliance=pass_rate([r for r in results if 'format' in r.get('id', '')]),
            graceful_error_rate=pass_rate(error_tests),
            helpful_message_rate=pass_rate([r for r in error_tests if 'helpful' in str(r.get('behaviors_found', []))]),
            avg_turns_to_complete=sum(r.get('turns', 5) for r in results) / total,
            avg_token_usage=sum(r.get('tokens', 1000) for r in results) // total,
            overall_pass_rate=pass_rate(results)
        )


def load_results(results_dir: Path) -> list[dict]:
    """Load all result files from directory."""
    results = []
    for file in results_dir.glob("*.jsonl"):
        with open(file) as f:
            for line in f:
                if line.strip():
                    results.append(json.loads(line))
    return results


def generate_metrics_report(metrics: EvalMetrics, output_path: Path):
    """Generate a markdown metrics report."""

    report = f"""# ADK-Builder Evaluation Metrics

**Generated:** {metrics.timestamp}

## Summary

| Metric | Value | Status |
|--------|-------|--------|
| Overall Pass Rate | {metrics.overall_pass_rate*100:.1f}% | {"🟢" if metrics.overall_pass_rate > 0.9 else "🟡" if metrics.overall_pass_rate > 0.7 else "🔴"} |
| Command Activation | {metrics.command_activation_rate*100:.1f}% | {"🟢" if metrics.command_activation_rate > 0.9 else "🟡" if metrics.command_activation_rate > 0.7 else "🔴"} |
| Skill Activation | {metrics.skill_activation_rate*100:.1f}% | {"🟢" if metrics.skill_activation_rate > 0.9 else "🟡" if metrics.skill_activation_rate > 0.7 else "🔴"} |
| Mode Transitions | {metrics.mode_transition_accuracy*100:.1f}% | {"🟢" if metrics.mode_transition_accuracy > 0.9 else "🟡" if metrics.mode_transition_accuracy > 0.7 else "🔴"} |
| Error Handling | {metrics.graceful_error_rate*100:.1f}% | {"🟢" if metrics.graceful_error_rate > 0.9 else "🟡" if metrics.graceful_error_rate > 0.7 else "🔴"} |

## Performance

- **Average Turns:** {metrics.avg_turns_to_complete:.1f}
- **Average Tokens:** {metrics.avg_token_usage:,}

## Thresholds

| Metric | Target | Current | Gap |
|--------|--------|---------|-----|
| Pass Rate | 90% | {metrics.overall_pass_rate*100:.1f}% | {(0.9 - metrics.overall_pass_rate)*100:+.1f}% |
| Command Activation | 95% | {metrics.command_activation_rate*100:.1f}% | {(0.95 - metrics.command_activation_rate)*100:+.1f}% |
| Skill Activation | 90% | {metrics.skill_activation_rate*100:.1f}% | {(0.9 - metrics.skill_activation_rate)*100:+.1f}% |

## Raw Metrics

```json
{metrics.to_json()}
```
"""

    output_path.write_text(report)


if __name__ == "__main__":
    import sys

    results_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("results")
    output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("reports/metrics.md")

    results = load_results(results_dir)
    metrics = EvalMetrics.from_results(results)
    generate_metrics_report(metrics, output_path)

    print(f"Metrics report: {output_path}")
    print(f"Overall pass rate: {metrics.overall_pass_rate*100:.1f}%")
```

#### 6.2 Create Historical Tracking

**File:** `evals/runners/track_history.py`
```python
#!/usr/bin/env python3
"""
Track evaluation metrics over time.
"""

import json
from datetime import datetime
from pathlib import Path


def append_metrics(metrics_file: Path, new_metrics: dict):
    """Append new metrics to history file."""

    history = []
    if metrics_file.exists():
        with open(metrics_file) as f:
            history = json.load(f)

    # Add timestamp if not present
    if 'timestamp' not in new_metrics:
        new_metrics['timestamp'] = datetime.now().isoformat()

    history.append(new_metrics)

    # Keep last 100 entries
    history = history[-100:]

    with open(metrics_file, 'w') as f:
        json.dump(history, f, indent=2)


def generate_trend_report(history_file: Path, output_path: Path):
    """Generate a trend report from history."""

    if not history_file.exists():
        return

    with open(history_file) as f:
        history = json.load(f)

    if len(history) < 2:
        return

    latest = history[-1]
    previous = history[-2]

    def trend(key):
        delta = latest.get(key, 0) - previous.get(key, 0)
        if delta > 0.01:
            return f"↑ +{delta*100:.1f}%"
        elif delta < -0.01:
            return f"↓ {delta*100:.1f}%"
        return "→ stable"

    report = f"""# Evaluation Trend Report

**Latest:** {latest.get('timestamp', 'unknown')}
**Previous:** {previous.get('timestamp', 'unknown')}

## Trends

| Metric | Current | Trend |
|--------|---------|-------|
| Pass Rate | {latest.get('overall_pass_rate', 0)*100:.1f}% | {trend('overall_pass_rate')} |
| Command Activation | {latest.get('command_activation_rate', 0)*100:.1f}% | {trend('command_activation_rate')} |
| Skill Activation | {latest.get('skill_activation_rate', 0)*100:.1f}% | {trend('skill_activation_rate')} |
| Error Handling | {latest.get('graceful_error_rate', 0)*100:.1f}% | {trend('graceful_error_rate')} |

## History (Last 10)

| Date | Pass Rate | Commands | Skills |
|------|-----------|----------|--------|
"""

    for entry in history[-10:]:
        date = entry.get('timestamp', 'unknown')[:10]
        pr = entry.get('overall_pass_rate', 0) * 100
        cmd = entry.get('command_activation_rate', 0) * 100
        skill = entry.get('skill_activation_rate', 0) * 100
        report += f"| {date} | {pr:.0f}% | {cmd:.0f}% | {skill:.0f}% |\n"

    output_path.write_text(report)


if __name__ == "__main__":
    from metrics import EvalMetrics, load_results

    results_dir = Path("results")
    history_file = Path("reports/history.json")
    trend_report = Path("reports/trends.md")

    results = load_results(results_dir)
    metrics = EvalMetrics.from_results(results)

    append_metrics(history_file, {
        'timestamp': metrics.timestamp,
        'overall_pass_rate': metrics.overall_pass_rate,
        'command_activation_rate': metrics.command_activation_rate,
        'skill_activation_rate': metrics.skill_activation_rate,
        'graceful_error_rate': metrics.graceful_error_rate,
    })

    generate_trend_report(history_file, trend_report)
```

### Verification Checklist
- [ ] Metrics collector computes all defined metrics
- [ ] History tracking preserves at most 100 entries
- [ ] Trend report shows directional changes
- [ ] Thresholds are clearly defined and actionable
- [ ] Reports are human-readable markdown

---

## Phase 7: Final Integration

### Objective
Wire everything together into a cohesive, runnable evaluation system.

### Tasks

#### 7.1 Create Master Runner

**File:** `evals/run_all.sh`
```bash
#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "================================"
echo "ADK-Builder Full Evaluation Suite"
echo "================================"
echo ""

# Phase 1: Run basic evaluations
echo "Phase 1: Basic Evaluations"
"$SCRIPT_DIR/runners/run_eval.sh"

# Phase 2: Run Python SDK evaluations (if available)
if command -v python3 &> /dev/null && python3 -c "import claude_agent_sdk" 2>/dev/null; then
    echo ""
    echo "Phase 2: SDK Evaluations"
    python3 "$SCRIPT_DIR/runners/run_eval.py"
fi

# Phase 3: Generate metrics
echo ""
echo "Phase 3: Metrics Generation"
python3 "$SCRIPT_DIR/runners/metrics.py" "$SCRIPT_DIR/results" "$SCRIPT_DIR/reports/metrics.md"

# Phase 4: Update history
echo ""
echo "Phase 4: History Tracking"
python3 "$SCRIPT_DIR/runners/track_history.py"

# Final summary
echo ""
echo "================================"
echo "Evaluation Complete"
echo "================================"
echo ""
echo "Reports generated:"
ls -la "$SCRIPT_DIR/reports/"
```

#### 7.2 Create README

**File:** `evals/README.md`
```markdown
# ADK-Builder Evaluation Framework

Rigorous testing of the adk-builder Claude Code plugin using Claude Code itself.

## Quick Start

```bash
# Set your API key
export ANTHROPIC_API_KEY=your-key-here

# Run all evaluations
./run_all.sh

# Or run specific components
./runners/run_eval.sh           # CLI-based evaluation
python runners/run_eval.py       # SDK-based evaluation (requires pip install claude-agent-sdk)
./runners/ralph_loop.sh         # Self-improving loop
```

## Structure

```
evals/
├── datasets/          # Test cases in JSONL format
├── runners/           # Evaluation scripts
├── agents/            # Specialized eval subagents
├── hooks/             # Validation hooks
├── results/           # Raw outputs (gitignored)
└── reports/           # Generated reports
```

## Metrics Tracked

| Metric | Target | Description |
|--------|--------|-------------|
| Command Activation | 95% | /adk commands activate correctly |
| Skill Activation | 90% | @skill references load properly |
| Mode Transitions | 90% | SPEC/PLAN/BUILD flow correctly |
| Error Handling | 85% | Errors are caught gracefully |

## Adding Tests

Add JSONL entries to `datasets/`:

```json
{"id": "test_name", "prompt": "your prompt", "expected_behaviors": ["behavior1", "behavior2"]}
```

## CI/CD

The GitHub Action in `.github/workflows/plugin-eval.yml` runs on every push to the plugin.
```

### Verification Checklist
- [ ] `run_all.sh` executes all phases in order
- [ ] README provides clear getting-started instructions
- [ ] All scripts are executable
- [ ] .gitignore excludes results/ contents
- [ ] Reports are generated in reports/

---

## Summary: Allowed APIs

### CLI Invocation

| Flag | Purpose |
|------|---------|
| `-p "prompt"` | One-shot mode |
| `--output-format json` | Structured output |
| `--allowedTools "..."` | Auto-approve tools |
| `--resume "id"` | Continue session |
| `--plugin-dir /path` | Load plugin |
| `--append-system-prompt` | Add eval context |
| `--max-turns N` | Limit iterations |

### Python SDK

```python
from claude_agent_sdk import query, ClaudeAgentOptions, AgentDefinition

async for message in query(
    prompt="...",
    options=ClaudeAgentOptions(
        allowed_tools=["Read", "Write", "Glob"],
        agents={"name": AgentDefinition(...)},
    )
):
    ...
```

### Hooks

| Hook | Purpose |
|------|---------|
| `Stop` | Block completion |
| `PostToolUse` | Validate tool outputs |
| `SessionStart` | Initialize context |

---

## Anti-Pattern Guards

1. **DO NOT** use `--dangerously-skip-permissions` in automated evals
2. **DO NOT** include `Task` in subagent tool lists (no recursion)
3. **DO NOT** guess tool names - verify against documentation
4. **DO NOT** assume MCP state persists across sessions
5. **DO NOT** use flags that don't exist (`-i`, `--interactive`)

---

## Success Criteria

The evaluation framework is complete when:

- [ ] Command activation rate ≥ 95%
- [ ] Skill activation rate ≥ 90%
- [ ] Mode transition accuracy ≥ 90%
- [ ] Error handling rate ≥ 85%
- [ ] CI runs green on every PR
- [ ] Metrics tracked over time with trend analysis
