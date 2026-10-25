from datetime import date
from typing import Any

from pydantic_ai import RunContext

from ..sandbox.execute import CodeExecutor
from ..schemas.artifacts import ArtifactMetadata
from ..schemas.financial import (
    AnalystReport,
    AttributionBreakdown,
    BQSafeQueryResult,
    CodeExecInput,
    CodeExecResult,
    ExposuresResult,
    NewsResult,
    PnLDailySummary,
)
from ..tools.artifacts import ArtifactStore
from ..tools.bq_guarded import GuardedBQ
from ..tools.news import NewsClient

bq = GuardedBQ()
news = NewsClient()
executor = CodeExecutor()
store = ArtifactStore()


async def get_pnl_daily_summary(
    ctx: RunContext,
    start_date: date,
    end_date: date,
    min_abs_move: float | None = 50000.0,
) -> PnLDailySummary:
    """Get daily PnL summary with top contributors. Large results go to artifacts."""
    return await bq.get_pnl_daily_summary(start_date, end_date, min_abs_move)


async def get_attribution_breakdown(
    ctx: RunContext,
    dates: list[date],
    group_by: list[str],
) -> AttributionBreakdown:
    """Get PnL attribution breakdown by drivers."""
    return await bq.get_attribution_breakdown(dates, group_by)


async def get_exposures(
    ctx: RunContext,
    as_of: date,
    tickers: list[str],
) -> ExposuresResult:
    """Get exposures for specific tickers only."""
    return await bq.get_exposures(as_of, tickers)


async def search_news(
    ctx: RunContext,
    tickers: list[str],
    start: date,
    end: date,
    max_items: int | None = 10,
) -> NewsResult:
    """Search news with summaries only (no full articles)."""
    return await news.search_news(tickers, start, end, max_items)


async def bq_safe_query(
    ctx: RunContext,
    template_name: str | None = None,
    sql: str | None = None,
    params: dict[str, Any] | None = None,
    max_rows: int | None = None,
    max_bytes: int | None = None,
) -> BQSafeQueryResult:
    """Execute guardrailed BQ query with dry-run and caps."""
    return await bq.bq_safe_query(template_name, sql, params, max_rows, max_bytes)


async def get_artifact_metadata(
    ctx: RunContext,
    uri: str,
) -> ArtifactMetadata:
    """Get metadata for artifact without reading full contents."""
    return await store.get_metadata(uri)


async def execute_python(
    ctx: RunContext,
    code: str,
    inputs: list[dict[str, Any]] | None = None,
) -> CodeExecResult:
    """Execute Python in sandbox to analyze artifacts and create visualizations."""
    input_objs = [CodeExecInput(**i) for i in (inputs or [])]
    return await executor.execute_python(code, input_objs)


async def delegate_to_financial_analyst(
    ctx: RunContext,
    query: str,
    context: dict[str, Any] | None = None,
) -> AnalystReport:
    """Delegate PnL/exposure/news/attribution questions to financial analyst."""
    from . import get_financial_analyst

    analyst = get_financial_analyst()
    result = await analyst.run(query, deps=context or {})
    return result.output


async def discover_data_sources_tool(ctx: RunContext) -> dict[str, Any]:
    from .capability_discovery import discover_data_sources

    return await discover_data_sources(ctx)


async def discover_sandbox_capabilities_tool(ctx: RunContext) -> dict[str, Any]:
    from .capability_discovery import discover_sandbox_capabilities

    return await discover_sandbox_capabilities(ctx)


async def discover_apis_tool(ctx: RunContext) -> dict[str, Any]:
    from .capability_discovery import discover_apis

    return await discover_apis(ctx)
