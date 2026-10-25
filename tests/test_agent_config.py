from coding_agent.agents.financial_analyst import FINANCIAL_ANALYST_SYSTEM_PROMPT
from coding_agent.agents.root import ROOT_AGENT_SYSTEM_PROMPT


def test_prompts_contain_keywords():
    assert "orchestrator" in ROOT_AGENT_SYSTEM_PROMPT.lower()
    assert "financial_analyst" in ROOT_AGENT_SYSTEM_PROMPT
    assert "artifact" in FINANCIAL_ANALYST_SYSTEM_PROMPT
    assert "execute_python" in FINANCIAL_ANALYST_SYSTEM_PROMPT
    assert "coding_agent" in FINANCIAL_ANALYST_SYSTEM_PROMPT
    assert "can" in FINANCIAL_ANALYST_SYSTEM_PROMPT.lower()
    assert "cannot" in FINANCIAL_ANALYST_SYSTEM_PROMPT.lower()
    assert "clarify" in FINANCIAL_ANALYST_SYSTEM_PROMPT.lower()


def test_financial_tools_defined():
    from coding_agent import tools

    for tool_name in [
        "get_pnl_daily_summary",
        "get_attribution_breakdown",
        "get_exposures",
        "search_news",
        "bq_safe_query",
        "get_artifact_metadata",
        "execute_python",
        "delegate_to_financial_analyst",
        "discover_data_sources_tool",
        "discover_sandbox_capabilities_tool",
        "discover_apis_tool",
    ]:
        assert hasattr(tools, tool_name), tool_name
