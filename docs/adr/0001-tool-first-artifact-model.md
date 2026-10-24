# ADR-0001: Tool-First Access with Artifact Materialization

- Status: Accepted
- Date: 2026-10-24
- Deciders: Agent Architecture

## Context

The Financial Analyst needs to answer questions like "PNL moved >50K since beginning of September every day - why?" using BigQuery (historical PnL attribution, exposures, Bloomberg tickers), a news API, and Python code execution. Dumping large tables or full news articles into the LLM context is expensive in tokens/cost and risks blowing context. 

## Decision

Adopt a **tool-first, artifact-first** pattern:
- Expose typed domain tools (e.g., `get_pnl_daily_summary`, `get_attribution_breakdown`, `get_exposures`, `search_news`) that return small previews/aggregates.
- Write full query results to external artifacts (object storage/local) as Parquet/CSV/JSON and return URIs + metadata.
- Require code execution to read from artifacts via URIs rather than accepting large blobs in tool results.
- Enforce truncation/clamping of tool outputs to a small preview (e.g., top N rows/aggregates).

## Consequences

### Positive
- Keeps LLM context small (cost/token aware).
- Enables processing of arbitrarily large datasets in the sandbox.
- Clear separation: reasoning in agent, computation in sandbox.
- Traceable via artifact URIs.

### Negative
- More plumbing (artifact storage, metadata, URI passing).
- Slightly more complex flow for simple queries.
- Need to manage artifact lifecycle/cleanup.

## Alternatives Considered
- **Dump everything into context**: Simple but violates cost/token constraints.
- **Let agent write arbitrary SQL and stream results**: Still risks large result sets; hard to enforce caps.
- **RAG over data lake**: Overkill for structured relational/time-series queries; harder to enforce precise filters/cost estimation.
