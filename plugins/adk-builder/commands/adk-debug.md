---
name: adk-debug
description: Diagnostic mode for ADK issues - invokes the debugging subagent
argument-hint: Optional error message or file path
allowed-tools: ["Read", "Glob", "Grep", "Task", "Skill"]
---

# ADK Debug Command

Diagnose ADK-related issues by dispatching to the adk-debugger subagent.

## Your Task

When /adk-debug is invoked:

1. **Collect context** from user's message and environment
2. **Dispatch adk-debugger** using the Task tool
3. **Report findings** and suggestions

## Step-by-Step Execution

### 1. Extract Information

From the user's input, extract:
- **Error message** (if provided)
- **File path** (if provided)
- **Project context** (check .claude/adk-builder.local.md for current feature)
- **Description** (what the user is trying to do)

### 2. Invoke Debugger via Task

Use the Task tool to dispatch adk-debugger:

```
Task:
subagent_type: adk-debugger
description: "Diagnose ADK issue"
prompt: "Analyze the following issue and suggest fixes:

Problem: [user's error message or description]
Context: [relevant files or commands]
Project: [current feature if exists]

Check the code, logs, and configuration.
Identify root cause and suggest corrective actions.
If possible, provide specific code fixes or commands to run."
```

### 3. Process and Report Results

When the debugger returns:

1. **Summary:** Explain what was diagnosed
2. **Root Cause:** Why it happened
3. **Fix:** Specific steps to resolve
4. **Verification:** How to test the fix

## Examples

**Error message provided:**
```
User: /adk-debug ModuleNotFoundError: No module named 'google.adk'

→ Dispatch adk-debugger with error context
→ Debugger identifies import issue
→ Suggests: pip install google-agents or check ADK installation
→ Provides corrected import statement
```

**File path provided:**
```
User: /adk-debug weather_agent/agent.py

→ Dispatch adk-debugger to analyze file
→ Debugger reads file, checks for issues
→ Reports syntax errors, missing imports, etc.
```

**General diagnosis:**
```
User: /adk-debug

→ Dispatch adk-debugger for environment check
→ Debugger verifies:
  - ADK is installed
  - Dependencies available
  - Current project state
  - Any pending issues
```

## Important

- **Always dispatch:** Use Task tool to invoke adk-debugger
- **Include context:** Provide error messages, file paths, descriptions
- **Be specific:** If possible, quote error messages exactly
- **Report clearly:** After debugger finishes, summarize findings for user
