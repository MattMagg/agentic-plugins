#!/bin/bash
# Agentic Builder - Pre-Compact Hook
# Ensures critical state is preserved before context compaction

set -e

# Read input from stdin
INPUT=$(cat)
CWD=$(echo "$INPUT" | python3 -c "import sys, json; print(json.load(sys.stdin).get('cwd', '.'))" 2>/dev/null || echo ".")

# Check for state file
STATE_FILE="$CWD/.claude/agentic-builder.local.md"

if [ ! -f "$STATE_FILE" ]; then
    # No state to preserve
    exit 0
fi

# Extract critical state
extract_state() {
    local frameworks=$(grep "^frameworks:" "$STATE_FILE" 2>/dev/null | cut -d: -f2 | tr -d ' []' || echo "")
    local phase=$(grep "^phase:" "$STATE_FILE" 2>/dev/null | cut -d: -f2 | tr -d ' ' || echo "")
    local feature=$(grep "^feature:" "$STATE_FILE" 2>/dev/null | cut -d: -f2 | tr -d ' "' || echo "")
    local step=$(grep "^last_completed_step:" "$STATE_FILE" 2>/dev/null | cut -d: -f2 | tr -d ' ' || echo "0")
    local total=$(grep "^total_steps:" "$STATE_FILE" 2>/dev/null | cut -d: -f2 | tr -d ' ' || echo "")

    echo "Agentic Builder State: framework=$frameworks, phase=$phase, feature=$feature, step=$step${total:+/$total}"
}

# Output state summary for context preservation
STATE=$(extract_state)
echo "$STATE"
