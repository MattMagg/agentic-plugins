#!/bin/bash
# Agentic Builder - Session Start Hook
# Detects frameworks and loads session state

set -e

# Read input from stdin
INPUT=$(cat)
CWD=$(echo "$INPUT" | python3 -c "import sys, json; print(json.load(sys.stdin).get('cwd', '.'))" 2>/dev/null || echo ".")

# Check for state file
STATE_FILE="$CWD/.claude/agentic-builder.local.md"

# Detect frameworks in project
detect_frameworks() {
    local frameworks=""

    if grep -r "from google.adk" --include="*.py" "$CWD" 2>/dev/null | head -1 | grep -q .; then
        frameworks="${frameworks}adk,"
    fi
    if grep -r "from agents import\|from openai" --include="*.py" "$CWD" 2>/dev/null | head -1 | grep -q .; then
        frameworks="${frameworks}openai,"
    fi
    if grep -r "from langchain" --include="*.py" "$CWD" 2>/dev/null | head -1 | grep -q .; then
        frameworks="${frameworks}langchain,"
    fi
    if grep -r "from langgraph" --include="*.py" "$CWD" 2>/dev/null | head -1 | grep -q .; then
        frameworks="${frameworks}langgraph,"
    fi
    if grep -r "from crewai" --include="*.py" "$CWD" 2>/dev/null | head -1 | grep -q .; then
        frameworks="${frameworks}crewai,"
    fi

    # Remove trailing comma
    echo "${frameworks%,}"
}

# Build context message
build_context() {
    local msg="Agentic Builder ready."

    # Check for state file
    if [ -f "$STATE_FILE" ]; then
        # Extract key info from state file
        local phase=$(grep "^phase:" "$STATE_FILE" 2>/dev/null | cut -d: -f2 | tr -d ' ' || echo "")
        local feature=$(grep "^feature:" "$STATE_FILE" 2>/dev/null | cut -d: -f2 | tr -d ' "' || echo "")
        local step=$(grep "^last_completed_step:" "$STATE_FILE" 2>/dev/null | cut -d: -f2 | tr -d ' ' || echo "0")

        if [ -n "$phase" ] && [ -n "$feature" ]; then
            msg="$msg Resuming: $feature (phase: $phase, step: $step)."
        fi
    fi

    # Detect frameworks
    local detected=$(detect_frameworks)
    if [ -n "$detected" ]; then
        msg="$msg Detected frameworks: $detected."
    fi

    echo "$msg"
}

# Output context for Claude
CONTEXT=$(build_context)
echo "$CONTEXT"
