# coding-agent

Financial analyst agent with code execution, integrated with pydantic_ai and Google Vertex AI.

## Architecture

- **Root Agent**: Orchestrator that routes requests to specialists
- **Financial Analyst Agent**: Specialized subagent for PnL investigation with cost/token awareness
- **Tool-First Access**: Data retrieved via typed tools, large results go to artifacts
- **Guardrailed BigQuery**: Dry-run, caps, templates, no SELECT *
- **Sandboxed Code Execution**: Isolated Python runtime for analysis and visualizations
- **Artifact-First**: Results stored outside LLM context, only previews/URIs returned

## Documentation

- [Context/Glossary](CONTEXT.md)
- [ADRs](docs/adr/)
  - [0001 - Tool-First Access with Artifact Materialization](docs/adr/0001-tool-first-artifact-model.md)
  - [0002 - Guardrailed BigQuery Access](docs/adr/0002-guardrailed-bq-access.md)
  - [0003 - Sandboxed Python Code Execution](docs/adr/0003-sandboxed-code-execution.md)
  - [0004 - Root Agent + Financial Analyst Subagent](docs/adr/0004-root-plus-financial-analyst-subagent.md)

## Setup

```bash
uv sync
```

## Usage

See `src/coding_agent/agents/` for agent setup with pydantic_ai and Vertex AI.

## Handoff & Tool Wiring

- Root agent has `delegate_to_financial_analyst` tool to route PnL/exposure/news/attribution queries
- Financial analyst is wired with domain tools: `get_pnl_daily_summary`, `get_attribution_breakdown`, `get_exposures`, `search_news`, `bq_safe_query`, `get_artifact_metadata`, `execute_python`
- Tools enforce artifact-first pattern and guardrails (dry-run, caps, previews)

## Local Sandboxed Execution
- `execute_python` runs locally with import restrictions (no pip install, no subprocess/socket)
- Allowed imports configured in SandboxConfig; blocked list enforced
- Artifacts (png/html/csv/parquet/json) collected from run dir
- In-house APIs (this repo) available via PYTHONPATH - can import `coding_agent.*` modules
- Skills support for discoverable workflows

## Research Team Orchestration
- Manager pattern: clarify business problem, assess feasibility (data/sources/modules), plan, delegate
- Roles: Coding/Financial Analyst, Fact Checker/Reviewer, Report Writer
- Capability discovery tools to check data sources, sandbox modules, APIs
- Skills-based loading supported via pydantic_ai patterns

## Agent Instructions
- Financial analyst plugged with all tools and coder instructions (clarify, feasibility check, artifact-first, in-house APIs)
- Root agent wired with delegation and capability discovery

## Research Pipeline
- Root orchestrator: NO code execution, only clarification/feasibility/delegation/communication
- Pipeline: clarify -> assess feasibility -> delegate to coder/analyst -> fact check -> report write
- Subagents: Financial Analyst/Coder (can execute code), Fact Checker, Report Writer
