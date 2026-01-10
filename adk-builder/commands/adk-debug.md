---
name: adk-debug
description: Diagnose common ADK issues (import errors, auth failures, runtime crashes)
when_to_use: Use when encountering ADK errors, unexpected behavior, or setup issues
color: red
---

# /adk-debug - ADK Diagnostic Command

Systematically diagnose common ADK issues including import errors, authentication failures, runtime crashes, and configuration problems.

## Diagnostic Process

### 1. Gather Context

Run these commands to collect diagnostic information:

```bash
# Check Python and ADK installation
python --version
pip show google-genai-adk

# Verify project structure
ls -la
cat adk.yaml 2>/dev/null || echo "No adk.yaml found"
cat pyproject.toml 2>/dev/null || echo "No pyproject.toml found"

# Check for ADK imports
find . -name "*.py" -type f -exec grep -l "from google.genai.adk" {} \; 2>/dev/null

# Test basic import
python -c "from google.genai.adk import Agent; print('ADK import successful')" 2>&1
```

### 2. Categorize the Issue

Common issue categories:

#### Import Errors
- **Symptom**: `ModuleNotFoundError: No module named 'google.genai.adk'`
- **Check**: ADK installation, Python version, virtual environment activation
- **Fix**: `pip install google-genai-adk` or `pip install --upgrade google-genai-adk`

#### Authentication Failures
- **Symptom**: `401 Unauthorized`, `API key not found`, authentication errors
- **Check**: Environment variables, service account credentials, ADK config
- **Fix**: Set `GOOGLE_API_KEY` or configure service account authentication

#### Runtime Crashes
- **Symptom**: Agent execution fails, tool errors, timeout issues
- **Check**: Agent configuration, tool definitions, system prompts, dependencies
- **Fix**: Review agent config, validate tool schemas, check logs

#### Configuration Issues
- **Symptom**: YAML parsing errors, missing fields, invalid configuration
- **Check**: adk.yaml syntax, required fields, file paths
- **Fix**: Validate YAML syntax, ensure all required fields are present

### 3. Common Fixes

#### Fix: Install/Upgrade ADK
```bash
pip install --upgrade google-genai-adk
pip install --upgrade google-generativeai
```

#### Fix: Set Authentication
```bash
# Option 1: API Key
export GOOGLE_API_KEY="your-api-key-here"

# Option 2: Service Account (check if file exists)
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account.json"
ls -la $GOOGLE_APPLICATION_CREDENTIALS

# Option 3: gcloud authentication
gcloud auth application-default login
```

#### Fix: Verify Project Structure
```bash
# Check for required files
ls -la adk.yaml agents/ tools/ 2>/dev/null

# Validate YAML syntax
python -c "import yaml; yaml.safe_load(open('adk.yaml'))" 2>&1
```

#### Fix: Check Dependencies
```bash
# List installed packages
pip list | grep -E "google|genai|adk"

# Check for conflicts
pip check
```

#### Fix: Enable Debug Logging
```python
# Add to your Python script
import logging
logging.basicConfig(level=logging.DEBUG)
```

### 4. Output Format

After running diagnostics, provide:

1. **Environment Summary**
   - Python version
   - ADK version
   - OS/Platform
   - Virtual environment status

2. **Issue Classification**
   - Category (import/auth/runtime/config)
   - Specific error message
   - Suspected root cause

3. **Recommended Actions**
   - Immediate fixes to try
   - Configuration changes needed
   - Links to relevant documentation

4. **Next Steps**
   - If issue persists, suggest related skills:
     - `/adk-init` - Re-initialize project
     - `/adk-create-agent` - Recreate agent with validated config
     - Skills for specific components (tools, memory, etc.)

## Related Skills

- **adk-builder:adk-init** - Initialize or re-initialize ADK project
- **adk-builder:adk-create-agent** - Create new agent with validated configuration
- **adk-builder:adk-test** - Run tests to verify fixes
- **adk-builder:adk-advanced** - Advanced configuration and troubleshooting

## Example Usage

**User**: "I'm getting ModuleNotFoundError when importing ADK"

**Assistant**: *Runs diagnostic commands, identifies missing installation, provides fix:*
```bash
pip install google-genai-adk
python -c "from google.genai.adk import Agent; print('Success')"
```

**User**: "My agent is getting authentication errors"

**Assistant**: *Checks environment variables, validates credentials, guides setup:*
```bash
export GOOGLE_API_KEY="your-key"
# or
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/creds.json"
```
