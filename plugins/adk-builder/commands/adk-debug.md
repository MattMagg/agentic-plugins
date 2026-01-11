---
name: adk-debug
description: Diagnostic mode for ADK issues - invokes the debugging subagent
argument-hint: Optional error message or file path
allowed-tools: ["Read", "Glob", "Grep", "Task"]
---

# ADK Debug Command

You invoke the ADK debugging subagent to diagnose issues.

## Usage

When this command is invoked:

1. **Collect context** from the user's message:
   - Error message (if provided)
   - File path (if provided)
   - Current working directory

2. **Deploy the debugger**:

```
Use the adk-debugger subagent to diagnose the following issue:

[Include user's error message or description]
[Include relevant file paths]

The project is located at: [current directory]
```

3. **Report results** when debugger completes:

```
## Debugging Complete

**Issue:** [category]
**Root Cause:** [explanation]
**Fix Applied:** [yes/no]
**Verification:** [result]
```

## Examples

**With error message:**
```
User: /adk-debug ModuleNotFoundError: No module named 'google.adk'

→ Deploy adk-debugger with error context
→ Debugger diagnoses: Import category, wrong import path
→ Suggests fix: from google.adk.agents import LlmAgent
```

**With file path:**
```
User: /adk-debug agent.py

→ Deploy adk-debugger to analyze agent.py
→ Debugger finds issues and suggests fixes
```

**General diagnosis:**
```
User: /adk-debug

→ Deploy adk-debugger for general project diagnosis
→ Debugger runs environment checks and reports status
```
