#!/bin/bash
# init-spec.sh
# Generates a new spec file from the template for ADK-builder plugin commands

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
TEMPLATE_DIR="${PLUGIN_ROOT}/.templates"
SPECS_DIR="${PLUGIN_ROOT}/specs"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print colored message
print_msg() {
    local color=$1
    shift
    echo -e "${color}$*${NC}"
}

# Print usage
usage() {
    cat <<EOF
Usage: $0 <command-name>

Generate a new spec file from the template for an ADK-builder command.

Arguments:
    command-name    The name of the command (e.g., "adk-add-tool")

Examples:
    $0 adk-add-tool
    $0 adk-streaming

The script will:
1. Check if the spec file already exists
2. Copy the template to specs/<command-name>.spec.md
3. Open the file for editing (if EDITOR is set)

Environment Variables:
    EDITOR    Text editor to use for editing the file (optional)

EOF
    exit 1
}

# Check arguments
if [ $# -ne 1 ]; then
    print_msg "$RED" "Error: Missing command name"
    echo
    usage
fi

COMMAND_NAME="$1"
SPEC_FILE="${SPECS_DIR}/${COMMAND_NAME}.spec.md"
TEMPLATE_FILE="${TEMPLATE_DIR}/spec-template.md"

# Validate command name format
if [[ ! "$COMMAND_NAME" =~ ^adk-[a-z-]+$ ]]; then
    print_msg "$YELLOW" "Warning: Command name should follow pattern 'adk-*' (e.g., 'adk-add-tool')"
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_msg "$RED" "Aborted"
        exit 1
    fi
fi

# Check if template exists
if [ ! -f "$TEMPLATE_FILE" ]; then
    print_msg "$RED" "Error: Template file not found: $TEMPLATE_FILE"
    exit 1
fi

# Check if spec already exists
if [ -f "$SPEC_FILE" ]; then
    print_msg "$YELLOW" "Warning: Spec file already exists: $SPEC_FILE"
    read -p "Overwrite? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_msg "$BLUE" "Using existing file..."
        if [ -n "${EDITOR:-}" ]; then
            $EDITOR "$SPEC_FILE"
        fi
        exit 0
    fi
fi

# Create specs directory if it doesn't exist
mkdir -p "$SPECS_DIR"

# Copy template
print_msg "$BLUE" "Creating spec file: $SPEC_FILE"
cp "$TEMPLATE_FILE" "$SPEC_FILE"

# Update placeholders in the new spec file
sed -i.bak "s/{COMMAND_NAME}/${COMMAND_NAME}/g" "$SPEC_FILE"
rm -f "${SPEC_FILE}.bak"

print_msg "$GREEN" "✓ Created spec file: $SPEC_FILE"
echo
print_msg "$YELLOW" "Next steps:"
echo "1. Edit the spec file and fill in the sections"
echo "2. Run: ./scripts/validate-spec.py $COMMAND_NAME"
echo "3. Implement the command based on the spec"
echo

# Open in editor if EDITOR is set
if [ -n "${EDITOR:-}" ]; then
    print_msg "$BLUE" "Opening in $EDITOR..."
    $EDITOR "$SPEC_FILE"
else
    print_msg "$YELLOW" "Tip: Set EDITOR environment variable to auto-open the file"
    print_msg "$BLUE" "Example: export EDITOR=vim"
fi

print_msg "$GREEN" "Done!"
