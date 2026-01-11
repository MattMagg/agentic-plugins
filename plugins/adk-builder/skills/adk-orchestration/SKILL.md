---
name: ADK Orchestration
description: This skill should be used when the user asks about "multi-agent systems", "sub-agents", "delegation", "agent routing", "orchestration", "SequentialAgent", "ParallelAgent", "LoopAgent", "agent-to-agent", "A2A protocol", "agent hierarchy", "streaming", "real-time responses", "SSE", "server-sent events", "websocket", "bidirectional", "Live API", "voice", "audio", "video", "multimodal streaming", or needs guidance on building systems with multiple specialized agents working together or implementing real-time communication patterns.
version: 2.0.0
---

# ADK Orchestration

Guide for building multi-agent systems with delegation, orchestration, inter-agent communication, and real-time streaming capabilities. Enables specialized agents to collaborate on complex tasks with modern communication patterns.

## When to Use

### Multi-Agent Systems
- Routing requests to specialized sub-agents
- Building agent pipelines (sequential execution)
- Running agents concurrently (parallel execution)
- Creating hierarchical agent teams
- Cross-system agent communication (A2A)

### Streaming & Real-Time
- Streaming text responses as they generate
- Real-time chat with user interrupts
- Voice agent interactions (Live API)
- Video processing and multimodal streaming
- WebSocket bidirectional communication

## When NOT to Use

- Single agent with tools → Use `@adk-agents` and `@adk-tools` instead
- Callbacks and state → Use `@adk-behavior` instead
- Agent deployment → Use `@adk-deployment` instead

## Key Concepts

### Multi-Agent Patterns

**Delegation** routes requests to sub-agents based on their descriptions. The parent agent decides which child handles each request.

**SequentialAgent** executes sub-agents in order (A → B → C). Each agent receives the previous agent's output.

**ParallelAgent** runs sub-agents concurrently. Results are aggregated when all complete.

**LoopAgent** repeats execution until a condition is met. Useful for iterative refinement.

**Hierarchy** nests agent teams for complex organizations. Parent agents coordinate child teams.

**A2A Protocol** enables cross-system agent communication. Agents can call agents in other deployments.

### Streaming Patterns

**SSE (Server-Sent Events)** streams text responses incrementally. Client receives partial responses as they generate.

**Bidirectional Streaming** enables real-time two-way communication. Users can interrupt agent responses mid-stream.

**Live API** powers voice and video agents. Use `gemini-3-flash-live` model for real-time audio/video processing.

**Runner Types**: `Runner` for basic execution, `BidiStreamingRunner` for bidirectional, `LiveAPIRunner` for voice/video.

## References

Detailed guides with code examples:

### Multi-Agent
- `references/delegation.md` - Sub-agent routing patterns
- `references/orchestration.md` - Sequential, Parallel, Loop agents
- `references/advanced.md` - Hierarchical and complex patterns
- `references/a2a.md` - Agent-to-Agent protocol

### Streaming
- `references/sse.md` - Server-sent events streaming
- `references/bidirectional.md` - WebSocket bidirectional
- `references/multimodal.md` - Live API voice/video
