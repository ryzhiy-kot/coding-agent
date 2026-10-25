"""Tools for financial analysis."""

from .financial_tools import (
    bq_safe_query,
    delegate_to_fact_checker,
    delegate_to_financial_analyst,
    delegate_to_report_writer,
    discover_apis_tool,
    discover_data_sources_tool,
    discover_sandbox_capabilities_tool,
    execute_python,
    get_artifact_metadata,
    get_attribution_breakdown,
    get_exposures,
    get_pnl_daily_summary,
    search_news,
)

_financial_analyst_instance = None
_fact_checker_instance = None
_report_writer_instance = None


def get_financial_analyst():
    from ..agents.setup import create_financial_analyst_agent

    global _financial_analyst_instance
    if _financial_analyst_instance is None:
        _financial_analyst_instance = create_financial_analyst_agent()
    return _financial_analyst_instance


def get_fact_checker():
    from ..agents.setup import create_fact_checker_agent

    global _fact_checker_instance
    if _fact_checker_instance is None:
        _fact_checker_instance = create_fact_checker_agent()
        from .financial_tools import get_artifact_metadata

        _fact_checker_instance.tool(get_artifact_metadata)
    return _fact_checker_instance


def get_report_writer():
    from ..agents.setup import create_report_writer_agent

    global _report_writer_instance
    if _report_writer_instance is None:
        _report_writer_instance = create_report_writer_agent()
    return _report_writer_instance


__all__ = [
    "bq_safe_query",
    "delegate_to_fact_checker",
    "delegate_to_financial_analyst",
    "delegate_to_report_writer",
    "discover_apis_tool",
    "discover_data_sources_tool",
    "discover_sandbox_capabilities_tool",
    "execute_python",
    "get_artifact_metadata",
    "get_attribution_breakdown",
    "get_exposures",
    "get_fact_checker",
    "get_financial_analyst",
    "get_pnl_daily_summary",
    "get_report_writer",
    "search_news",
]
