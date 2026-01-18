---
name: Agent Deployment
description: Production deployment patterns for agentic systems. Use when deploying agents to production.
---

# Agent Deployment Patterns

## Deployment Options by Framework

| Framework | Recommended | Alternative |
|-----------|-------------|-------------|
| ADK | Agent Engine, Cloud Run | GKE, local |
| OpenAI | Any Python hosting | Serverless |
| LangChain | LangServe, Cloud Run | Docker |
| LangGraph | LangGraph Platform | Cloud Run |
| CrewAI | CrewAI Enterprise | Docker |

## Pre-Deployment Checklist

- [ ] All tests passing
- [ ] Environment variables documented
- [ ] Secrets in secret manager (not .env)
- [ ] Rate limiting configured
- [ ] Error handling complete
- [ ] Logging configured
- [ ] Monitoring set up
- [ ] Guardrails in place

## ADK Deployment

### Agent Engine (Recommended)
```python
# Deploy to Vertex AI Agent Engine
from google.adk.deploy import deploy_to_agent_engine

deploy_to_agent_engine(
    agent=root_agent,
    project_id="my-project",
    location="us-central1"
)
```

### Cloud Run
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "-m", "adk", "serve", "--host", "0.0.0.0"]
```

## Security Checklist

- [ ] Input validation/sanitization
- [ ] Output guardrails
- [ ] API key rotation plan
- [ ] Audit logging enabled
- [ ] Rate limiting per user
- [ ] Token limits set
- [ ] PII handling documented

## Environment Configuration

### Development
```env
ENVIRONMENT=development
LOG_LEVEL=DEBUG
TRACE_ENABLED=true
```

### Production
```env
ENVIRONMENT=production
LOG_LEVEL=INFO
TRACE_ENABLED=false
SECRET_MANAGER=gcp  # or aws, azure
```

## Monitoring Setup

### Key Metrics
- Request latency (p50, p95, p99)
- Error rate
- Token usage
- Tool call frequency
- Agent routing accuracy

### Alerting
- Error rate > 1%
- Latency p95 > 5s
- Token usage spike

## When to Use RAG

```python
mcp__agentic-rag__query_docs("deployment [framework]", frameworks=[fw])
mcp__agentic-rag__query_docs("production security", frameworks=[fw])
```
