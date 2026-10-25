from coding_agent import tools


def test_financial_tools_defined():

    for tool_name in [
        "get_pnl_daily_summary",
        "get_attribution_breakdown",
        "get_exposures",
        "search_news",
        "bq_safe_query",
        "get_artifact_metadata",
        "execute_python",
        "delegate_to_financial_analyst",
        "delegate_to_fact_checker",
        "delegate_to_report_writer",
        "discover_data_sources_tool",
        "discover_sandbox_capabilities_tool",
        "discover_apis_tool",
    ]:
        assert hasattr(tools, tool_name), tool_name
