---
name: ADK Production
description: This skill should be used when the user asks about "deploying", "production", "Agent Engine", "Vertex AI", "Cloud Run", "GKE", "Kubernetes", "hosting", "scaling", "guardrails", "safety", "content filtering", "input validation", "output validation", "authentication", "OAuth", "API keys", "credentials", "security plugins", "testing agents", "evaluation", "evals", "benchmarks", "tracing", "Cloud Trace", "logging", "observability", "AgentOps", "LangSmith", "user simulation", or needs guidance on deploying ADK agents to production environments, implementing safety measures, access control, secure authentication, testing, debugging, monitoring, or evaluating ADK agent quality.
version: 2.0.0
---

# ADK Production

Complete guide for deploying, securing, testing, and monitoring ADK agents in production. Covers deployment platforms, security guardrails, authentication, testing frameworks, tracing, and observability.

## When to Use

**Deployment:**
- Deploying agents to production
- Choosing between hosting options (Agent Engine, Cloud Run, GKE)
- Configuring auto-scaling
- Setting up CI/CD for agents
- Integrating with Vertex AI services

**Security:**
- Validating or filtering user input
- Filtering agent responses before delivery
- Implementing OAuth or API key authentication
- Creating reusable security plugins
- Blocking unsafe topics or content

**Quality & Testing:**
- Creating test suites for agents
- Evaluating agent responses against criteria
- Debugging execution with tracing
- Setting up production monitoring
- Automated testing with synthetic users

## When NOT to Use

- Local development → Use `@adk-getting-started` instead
- Agent creation → Use `@adk-agents` instead
- Tool integration → Use `@adk-tools` instead
- General callbacks → Use `@adk-behavior` instead
- Multi-agent systems → Use `@adk-multi-agent` instead

## Key Concepts

### Deployment

**Agent Engine** is the recommended managed deployment. Auto-scales, integrates with Vertex AI services, no infrastructure management.

**Cloud Run** offers container control with serverless scaling. Build custom Docker images for more control over the runtime.

**GKE (Kubernetes)** provides enterprise-scale deployment. Full control over infrastructure, networking, and scaling policies.

**Deployment CLI**: `adk deploy` handles Agent Engine deployment. For Cloud Run/GKE, containerize with `adk api_server`.

**Environment Configuration**: Use environment variables for credentials. Never commit secrets to source control.

### Security

**Input Guardrails** validate user input before processing. Use `before_model_callback` to block or modify unsafe requests.

**Output Guardrails** filter agent responses before returning to users. Use `after_model_callback` to redact PII, profanity, or sensitive data.

**Authentication** secures tool access. Configure OAuth credentials for Google APIs or custom authentication for third-party services.

**Security Plugins** bundle reusable security callbacks. Create plugins for logging, rate limiting, or content moderation.

**Credential Management** uses environment variables and secure storage. Never hardcode secrets in agent code.

### Quality & Testing

**Evaluations (Evals)** test agent behavior against expected outputs. Define test cases with inputs and expected results, measure pass rates.

**Tracing** captures execution flow for debugging. Cloud Trace integration shows LLM calls, tool executions, and timing.

**Logging** provides structured event capture. Use LoggingPlugin for consistent log formatting and levels.

**Observability** integrates with third-party platforms (AgentOps, LangSmith) for production monitoring and analytics.

**User Simulation** automates testing with synthetic conversations. Generate diverse test scenarios without manual testing.

## References

Detailed guides with code examples:

**Deployment:**
- `references/agent-engine.md` - Vertex AI Agent Engine
- `references/cloudrun.md` - Cloud Run deployment
- `references/gke.md` - Kubernetes deployment

**Security:**
- `references/guardrails.md` - Input/output validation
- `references/auth.md` - Authentication patterns
- `references/security-plugins.md` - Reusable security bundles

**Quality & Testing:**
- `references/evals.md` - Evaluation framework
- `references/tracing.md` - Cloud Trace integration
- `references/logging.md` - Structured logging
- `references/observability.md` - Third-party integrations
- `references/user-sim.md` - Synthetic user testing
