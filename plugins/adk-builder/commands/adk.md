---
name: adk
description: Root command for Google ADK development - detects project state and dispatches to appropriate subagent
argument-hint: Optional feature name or --debug/--spec/--plan flags
allowed-tools: ["Read", "Write", "Glob", "Grep", "Task", "Skill"]
---

# ADK Builder - Orchestrator

You must detect the current state and dispatch work to a specialized subagent. Always dispatch to subagents for actual work.

## Step 1: Detect State

Start by examining:

1. **File system state:**
   - Check if `.claude/adk-builder.local.md` exists
   - Check if `adk-builder/` directory exists and what projects are there

2. **Current command arguments:**
   - Parse for `--spec`, `--plan`, `--debug` flags
   - Parse for a feature name (e.g., `/adk my-agent`)

3. **State file if it exists:**
   - Read `.claude/adk-builder.local.md`
   - Extract `current_feature`, `phase`, `last_completed_step`

## Step 2: Determine Mode

Based on state, determine which mode to enter:

- **SPEC**: Starting new feature or `--spec` flag → Use adk-planner
- **PLAN**: Spec exists, no plan, or `--plan` flag → Use adk-planner
- **BUILD**: Plan exists or `phase: build` in state → Use adk-executor
- **DEBUG**: `--debug` flag or error recovery → Use adk-debugger

## Step 3: Announce Current State

Print a clear status announcement:

```
## Current State
- **Feature:** [none or feature-name]
- **Phase:** [SPEC/PLAN/BUILD/DEBUG]
- **Status:** [one sentence describing current situation]

Dispatching to [subagent-name] subagent...
```

## Step 4: Dispatch to Subagent

**This is the critical step.** You MUST use the Task tool to invoke the appropriate subagent:

```
Use Task tool:
- description: "Dispatch to subagent for [mode] phase"
- subagent_type: "adk-planner" or "adk-executor" or "adk-debugger"
- prompt: [Include context needed, see examples below]
```

### SPEC Mode Dispatch
For new project or `--spec`:
```
Task:
subagent_type: adk-planner
prompt: "User wants to create an ADK project named '[feature-name]'.
Enter SPEC mode: Gather detailed requirements and create adk-builder/[feature-name]/spec.md.
Ask clarifying questions one at a time about:
- Agent purpose and functionality
- Agent type (LlmAgent, etc.)
- Required tools and external APIs
- Model and deployment target
After gathering requirements, create the spec.md file with complete specifications."
```

### PLAN Mode Dispatch
When moving to planning:
```
Task:
subagent_type: adk-planner
prompt: "Enter PLAN mode for feature '[feature-name]'.
Read the spec from adk-builder/[feature-name]/spec.md.
Create a detailed implementation plan at adk-builder/[feature-name]/plan.md with:
- Step 1: [specific action]
- Step 2: [specific action]
- ... (as many steps as needed)
Each step should be actionable and generate specific code or files."
```

### BUILD Mode Dispatch
When implementing:
```
Task:
subagent_type: adk-executor
prompt: "Enter BUILD mode for feature '[feature-name]'.
Read plan from: adk-builder/[feature-name]/plan.md
Start from step: [last_completed_step + 1]
Implement each step exactly as specified in the plan.
Create agent code, config files, tests.
Update state file after each completed step.
Goal: Fully implemented working agent."
```

### DEBUG Mode Dispatch
When debugging:
```
Task:
subagent_type: adk-debugger
prompt: "Enter DEBUG mode. Analyze the following issue and suggest fixes:
[error message or problem description]
Check:
- adk-builder/[feature-name]/spec.md (if exists)
- adk-builder/[feature-name]/plan.md (if exists)
- [feature-name]/ (generated code if exists)
- .claude/adk-builder.local.md (state)
Report findings and suggest corrective actions."
```

## Step 5: Process Subagent Results

After the subagent returns:

1. **Summary:** Report what was completed
2. **Files:** List files created or modified
3. **Next Action:** Tell user what to do next (e.g., "Run /adk again to continue")

## Important Notes

- **Always dispatch:** If user needs work done (spec, plan, build, debug), USE Task tool
- **State file updates:** Subagents should update `.claude/adk-builder.local.md` after each phase
- **Feature name handling:** If no feature name provided and no state exists, ask or default to context
- **Error handling:** If a subagent encounters an error, catch it and either retry or dispatch to debugger

## Examples

**New Feature:**
```
User: /adk weather-agent
→ No existing project detected
→ Enter SPEC mode, dispatch adk-planner
→ Gather weather agent requirements
→ Create adk-builder/weather-agent/spec.md
```

**Resume Work:**
```
User: /adk
→ State file exists showing phase: plan, feature: weather-agent
→ Continue to PLAN mode, dispatch adk-planner
→ Create adk-builder/weather-agent/plan.md
```

**Debug Issue:**
```
User: /adk --debug
→ Dispatch adk-debugger
→ Analyze any errors or issues
→ Suggest fixes
```
