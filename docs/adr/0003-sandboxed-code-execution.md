# ADR-0003: Sandboxed Python Code Execution

- Status: Accepted
- Date: 2026-10-24
- Deciders: Agent Architecture

## Context

The Financial Analyst must write and execute Python code to analyze artifacts, compute correlations/attributions, and produce visualizations (graphs/tables). Running arbitrary code in the agent process is unsafe and hard to resource-limit.

## Decision

Provide `execute_python` via an **isolated sandbox** with strict controls:
- Isolated runtime (e.g., E2B/Daytona/Modal or container with nsjail/cgroups).
- Import allowlist (pandas, numpy, pyarrow, duckdb, matplotlib, plotly, etc.).
- Network egress denied by default; only allow approved internal endpoints if absolutely necessary.
- Timeouts (e.g., 60-120s) and memory/disk limits.
- No `pip install` at runtime; deps baked into image.
- Inputs passed as artifact URIs only (read-only mounts where possible).
- Outputs captured as artifacts (images/HTML/CSV/Parquet) uploaded to object store with presigned URLs.
- Tool result returns only: stdout/stderr (truncated), summary, artifact list with URLs/captions, runtime/mem metrics.
- Block dangerous builtins/modules (`os.system`, `subprocess`, `socket`, `ctypes`, etc.).

## Consequences

### Positive
- Safe execution environment.
- Can process large artifacts without blowing context.
- Produces shareable visualizations.
- Resource/cost control.

### Negative
- Operational complexity (sandbox provider/infrastructure).
- Cold starts possible.
- Debugging can be harder (logs/artifacts vs inline).

## Alternatives Considered
- **Execute in same process**: Insecure and no resource isolation.
- **Use Jupyter kernel in-process**: Still shares resources; harder to sandbox egress/files.
- **Remote REPL without isolation**: Unacceptable from security/cost perspective.
