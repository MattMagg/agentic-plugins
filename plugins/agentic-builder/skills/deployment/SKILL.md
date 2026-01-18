---
name: Agent Deployment
description: Production deployment workflow for agentic systems. Directs to RAG for implementation.
---

# Agent Deployment Workflow

## Deployment Decision Framework

| Framework | Primary Option | Alternative | RAG Query |
|-----------|---------------|-------------|-----------|
| ADK | Agent Engine (Vertex AI) | Cloud Run, GKE | `"ADK deployment agent engine"` |
| OpenAI | Any Python hosting | Serverless, Docker | `"openai agents deployment"` |
| LangChain | LangServe, Cloud Run | Docker, K8s | `"langchain langserve deployment"` |
| LangGraph | LangGraph Platform | Cloud Run | `"langgraph platform deployment"` |
| CrewAI | CrewAI Enterprise | Docker | `"crewai deployment production"` |
| Anthropic | Any Python hosting | Docker, Serverless | `"anthropic agent deployment"` |

## Pre-Deployment Checklist

### Code Readiness
- [ ] All tests passing
- [ ] Error handling complete
- [ ] Logging configured
- [ ] Input validation in place
- [ ] Output guardrails active

### Configuration
- [ ] Environment variables documented
- [ ] Secrets in secret manager (NOT in .env or code)
- [ ] Rate limiting configured
- [ ] Token limits set
- [ ] Timeout values appropriate

### Security
- [ ] API key rotation plan
- [ ] Audit logging enabled
- [ ] PII handling documented
- [ ] Input sanitization active
- [ ] Output filtering configured

### Monitoring
- [ ] Health check endpoint
- [ ] Metrics collection
- [ ] Alerting rules defined
- [ ] Log aggregation setup

## Deployment Workflow

### Step 1: Environment Configuration
**RAG Query**: `mcp__agentic-rag__search("[framework] environment configuration", mode="explain")`

Production differs from development:
- LOG_LEVEL: INFO (not DEBUG)
- TRACE_ENABLED: false (or sampling)
- Secrets: Use secret manager, not .env

### Step 2: Containerization (if applicable)
**RAG Query**: `mcp__agentic-rag__search("[framework] dockerfile", mode="build")`

### Step 3: Platform Deployment
**RAG Query**: `mcp__agentic-rag__search("[framework] [platform] deployment", mode="explain")`

### Step 4: Monitoring Setup
**RAG Query**: `mcp__agentic-rag__search("[framework] monitoring observability", mode="explain")`

## Key Production Metrics

| Metric | Alert Threshold | Why It Matters |
|--------|-----------------|----------------|
| Latency p95 | > 5s | User experience |
| Error rate | > 1% | Reliability |
| Token usage | Spike > 200% | Cost control |
| Tool failures | > 5% | Agent effectiveness |
| Routing accuracy | < 90% | Multi-agent health |

## Security Considerations

### Input Validation
- Sanitize user input before passing to agent
- Limit input length
- Filter known attack patterns

**RAG Query**: `mcp__agentic-rag__search("agent input validation security", mode="explain")`

### Output Guardrails
- Filter sensitive information
- Prevent prompt leakage
- Validate tool outputs

**RAG Query**: `mcp__agentic-rag__search("agent guardrails output filtering", mode="explain")`

### Secret Management
- Never hardcode API keys
- Use platform secret managers (GCP Secret Manager, AWS Secrets Manager, etc.)
- Rotate keys regularly

**RAG Query**: `mcp__agentic-rag__search("[framework] secret management", mode="explain")`

## Scaling Considerations

| Concern | Solution | RAG Query |
|---------|----------|-----------|
| Cold starts | Keep warm instances | `"[framework] cold start"` |
| Concurrent requests | Queue + workers | `"[framework] scaling"` |
| Token limits | Request batching | `"[framework] rate limiting"` |
| State persistence | External store | `"[framework] state persistence"` |
