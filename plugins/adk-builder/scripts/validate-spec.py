#!/usr/bin/env python3
"""
validate-spec.py
Validates spec files for ADK-builder plugin commands.
"""

import argparse
import re
import sys
from pathlib import Path
from typing import List, Tuple

# ANSI colors
RED = '\033[0;31m'
GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
BLUE = '\033[0;34m'
NC = '\033[0m'  # No Color


def print_msg(color: str, *args):
    """Print colored message."""
    print(f"{color}{' '.join(map(str, args))}{NC}")


def validate_spec_file(spec_path: Path) -> Tuple[bool, List[str]]:
    """
    Validate a spec file.

    Returns:
        Tuple of (is_valid, list of errors/warnings)
    """
    errors = []
    warnings = []

    if not spec_path.exists():
        errors.append(f"Spec file not found: {spec_path}")
        return False, errors

    content = spec_path.read_text()

    # Required sections
    required_sections = [
        "# Command Specification",
        "## Overview",
        "## User-Facing Behavior",
        "## Implementation Requirements",
        "## Error Handling",
        "## Testing Requirements",
        "## Examples"
    ]

    for section in required_sections:
        if section not in content:
            errors.append(f"Missing required section: {section}")

    # Check for template placeholders
    placeholders = re.findall(r'\{[A-Z_]+\}', content)
    if placeholders:
        errors.append(f"Template placeholders not replaced: {', '.join(set(placeholders))}")

    # Check for TODO markers
    if 'TODO:' in content or '[TODO]' in content:
        warnings.append("File contains TODO markers - ensure they are addressed")

    # Check for minimum content in key sections
    if '## User-Facing Behavior' in content:
        behavior_section = content.split('## User-Facing Behavior')[1].split('##')[0]
        if len(behavior_section.strip()) < 50:
            warnings.append("User-Facing Behavior section seems incomplete (< 50 chars)")

    # Check for code examples
    if '```' not in content:
        warnings.append("No code examples found - consider adding examples")

    return len(errors) == 0, errors + warnings


def main():
    parser = argparse.ArgumentParser(
        description='Validate spec files for ADK-builder plugin commands'
    )
    parser.add_argument(
        'command_name',
        nargs='?',
        help='Command name (e.g., "adk-add-tool") to validate specific spec'
    )
    parser.add_argument(
        '--all',
        action='store_true',
        help='Validate all spec files'
    )

    args = parser.parse_args()

    # Determine plugin root
    script_dir = Path(__file__).parent
    plugin_root = script_dir.parent
    specs_dir = plugin_root / 'specs'

    if not specs_dir.exists():
        print_msg(RED, f"Error: Specs directory not found: {specs_dir}")
        sys.exit(1)

    # Determine which specs to validate
    if args.all:
        spec_files = list(specs_dir.glob('*.spec.md'))
        if not spec_files:
            print_msg(YELLOW, "No spec files found in", specs_dir)
            sys.exit(0)
    elif args.command_name:
        spec_file = specs_dir / f"{args.command_name}.spec.md"
        spec_files = [spec_file]
    else:
        parser.print_help()
        sys.exit(1)

    # Validate specs
    all_valid = True
    for spec_file in spec_files:
        print_msg(BLUE, f"\nValidating: {spec_file.name}")
        is_valid, messages = validate_spec_file(spec_file)

        if is_valid:
            print_msg(GREEN, "✓ Valid")
        else:
            print_msg(RED, "✗ Invalid")
            all_valid = False

        # Print messages
        for msg in messages:
            if msg.startswith("Warning"):
                print_msg(YELLOW, f"  • {msg}")
            else:
                print_msg(RED, f"  • {msg}")

    # Summary
    print()
    if all_valid:
        print_msg(GREEN, "All specs valid!")
        sys.exit(0)
    else:
        print_msg(RED, "Some specs have errors")
        sys.exit(1)


if __name__ == '__main__':
    main()
