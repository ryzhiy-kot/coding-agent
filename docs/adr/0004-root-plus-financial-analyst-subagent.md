# ADR-0004: Root Agent + Financial Analyst Subagent

- Status: Accepted
- Date: 2026-10-24
- Deciders: Agent Architecture

## Context

We need to add a code-executing financial analyst to an existing pydantic_ai + Google Vertex AI agent setup. We want clear separation of concerns and to keep the root agent focused on routing/general tasks.

## Decision

Adopt **two-agent architecture**:
- **Root Agent**: Orchestrator/router. Handles general queries, routes PnL/exposure/news/attribution/code-execution-investigation tasks to the Financial Analyst via handoff/tool.
- **Financial Analyst Agent**: Specialized subagent with domain system prompt (schemas, guardrails, ticker universe), tools (domain BQ/news, safe query, artifact metadata, execute_python), and cost/token awareness. Uses stronger/reasoning model as needed.
- Use pydantic_ai Agents with typed tool schemas (Pydantic). Consider structured output (`output_type`) for the analyst's final report.
- Leverage Vertex AI context caching for static parts of the analyst's system prompt.

## Consequences

### Positive
- Focused instructions reduce confusion and hallucinations.
- Easier to enforce guardrails in one place.
- Can tune model/cost per agent.
- Clean handoffs from existing root.

### Negative
- More agents to wire/test.
- Handoff context needs care (pass relevant IDs/URIs, not raw data).
- Routing logic required in root.

## Alternatives Considered
- **Single monolithic agent with many tools**: Becomes bloated; harder to enforce specialized guardrails and prompts.
- **Function-calling only without subagent**: Possible but less clean separation of system prompts/permissions.
- **Multi-agent framework beyond pydantic_ai**: Unnecessary; pydantic_ai supports composition/handoffs well.
