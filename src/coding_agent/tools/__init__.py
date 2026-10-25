"""Tools for financial analysis."""

from .financial_tools import (
    bq_safe_query,
    execute_python,
    get_artifact_metadata,
    get_attribution_breakdown,
    get_exposures,
    get_pnl_daily_summary,
    search_news,
)

_financial_analyst = None


def get_financial_analyst():
    from ..agents.setup import create_financial_analyst_agent

    global _financial_analyst
    if _financial_analyst is None:
        _financial_analyst = create_financial_analyst_agent()
        # Wire tools to analyst
        _financial_analyst.tool(get_pnl_daily_summary)
        _financial_analyst.tool(get_attribution_breakdown)
        _financial_analyst.tool(get_exposures)
        _financial_analyst.tool(search_news)
        _financial_analyst.tool(bq_safe_query)
        _financial_analyst.tool(get_artifact_metadata)
        _financial_analyst.tool(execute_python)
    return _financial_analyst


from .financial_tools import (
    delegate_to_financial_analyst,
    discover_apis_tool,
    discover_data_sources_tool,
    discover_sandbox_capabilities_tool,
)

__all__ = [
    "bq_safe_query",
    "delegate_to_financial_analyst",
    "discover_apis_tool",
    "discover_data_sources_tool",
    "discover_sandbox_capabilities_tool",
    "execute_python",
    "get_artifact_metadata",
    "get_attribution_breakdown",
    "get_exposures",
    "get_financial_analyst",
    "get_pnl_daily_summary",
    "search_news",
]
