# ADR-0002: Guardrailed BigQuery Access

- Status: Accepted
- Date: 2026-10-24
- Deciders: Agent Architecture

## Context

The agent needs access to BigQuery with PnL attribution, exposures, and a select set of Bloomberg tickers. Unrestricted SQL can cause massive scans (cost) and may return huge result sets (tokens). 

## Decision

Use **guardrailed query access**:
- Prefer domain-specific tools over freeform SQL.
- When SQL is necessary, use `bq_safe_query` with allowlisted query templates or a SQL rewriter.
- Enforce: require filters (date ranges/tickers), block `SELECT *`, require/insert `LIMIT` where appropriate, use parameterized queries.
- Perform BigQuery dry-run to estimate bytes scanned; reject or warn if over budget.
- Always write results > preview size to artifacts; return preview + `bytes_scanned_est` + `artifact_uri`.
- Label queries for cost tracking/quotas.

## Consequences

### Positive
- Prevents accidental full-table scans.
- Cost-aware by construction (dry-run + caps).
- Easier to reason about schemas via templates.
- Auditable query patterns.

### Negative
- Less flexible for ad-hoc exploratory SQL.
- Template maintenance burden.
- Rewriter needs careful testing to avoid bypasses.

## Alternatives Considered
- **Read-only service account with dataset ACLs only**: Necessary but insufficient (can still scan large datasets).
- **Row-level security + column masking**: Good for PII/exposure control but doesn't solve cost from large scans.
- **Let agent write SQL freely with instructions**: Relies on model compliance; not enforceable.
