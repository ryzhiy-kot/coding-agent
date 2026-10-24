# Context

## Glossary

- **Artifact**: A materialized result (file) produced by data retrieval or code execution, stored outside the LLM context (e.g., Parquet/CSV/PNG/HTML in object storage), referenced by URI.
- **Attribution (PnL Attribution)**: Decomposition of portfolio/book PnL into drivers (factors, sectors, strategies, desks) for a given period/grain.
- **Book**: A logical grouping of positions/trades used for PnL attribution and exposure reporting.
- **Code Execution Sandbox**: An isolated runtime where Python code can run with restricted imports/network/resources to process artifacts and produce visualizations/tables.
- **Exposure**: Position-level or aggregated market exposure (e.g., by ticker/sector/factor) as of a given timestamp.
- **Financial Analyst Agent**: A specialized subagent responsible for investigating PnL movements using tools and code execution, with strict cost/token awareness.
- **Guardrailed Query**: A data access path (template or validated query) that enforces filters, limits, and cost estimation (bytes scanned/rows) before execution.
- **News Summary**: A truncated/condensed representation of news (headlines, timestamps, sources, short summary) returned by the news API, never full article bodies by default.
- **Preview**: A small sample (e.g., first N rows/aggregates) returned in-tool to the agent; full results go to artifacts.
- **Root Agent**: Orchestrator that routes user requests to appropriate subagents/tools.
- **Tool-First Access**: Pattern where data is retrieved via typed tools/summaries rather than dumping raw tables into the LLM context.
