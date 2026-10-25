# ADR-0005: Research Team Orchestration (Manager + Specialist + Fact Checker + Report Writer)

- Status: Proposed
- Date: 2026-10-25
- Deciders: Agent Architecture

## Context

The current financial analyst is helpful but needs to be more specific about capabilities/limitations, clarify business questions before answering, and validate data/code feasibility. We need to ensure answers are grounded in available data/sources and presented in the right form.

## Decision

Evolve from single subagent to a **research team manager** pattern with specialized roles, orchestrated via skills/dynamic loading:
- **Research Manager**: Clarifies business problem (baseline/comparison, metrics, scope), assesses feasibility against available data/sources/modules, plans work, routes to specialists.
- **Coding/Financial Analyst**: Investigates using tools, writes/executes Python in sandbox, produces artifacts/analysis.
- **Fact Checker/Report Reviewer**: Validates numerical claims against artifacts/data, checks guardrails (cost/token), flags unsupported claims.
- **Report Writer**: Produces final answer in required format (length/structure/visuals) based on reviewer feedback.

Implementation options:
1. Use pydantic_ai subagents with handoffs and a manager agent
2. Use pydantic_ai Skills (dynamic loading) to load role prompts/tools per phase
3. Hybrid: manager uses skills to load capabilities/metadata, delegates to subagents

Also need **capability discovery**: inventory of data sources (BQ tables metadata + samples), available Python modules in sandbox env, news API, artifact store. Expose via tools/skills.

## Consequences

### Positive
- Forces clarification before answering
- Grounds answers in available data/code capabilities
- Better quality control via fact checking
- Flexible output formatting

### Negative
- More complex orchestration
- More turns/latency
- Need to manage state across roles

## Alternatives Considered
- Single agent with detailed system prompt: Less explicit about capability checks
- Fixed pipeline: Less flexible for different question types
