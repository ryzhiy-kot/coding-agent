"""Agent setup with pydantic_ai and Vertex AI."""

from pydantic_ai import Agent
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider

from ..config.settings import get_config
from ..schemas.financial import AnalystReport
from .financial_analyst import FINANCIAL_ANALYST_SYSTEM_PROMPT
from .roles import CODER_PROMPT, FACT_CHECKER_PROMPT, REPORT_WRITER_PROMPT
from .root import ROOT_AGENT_SYSTEM_PROMPT


def create_financial_analyst_agent() -> Agent:
    """Create Financial Analyst/Coder subagent."""
    config = get_config()
    provider = GoogleProvider(
        project=config.vertex.project_id, location=config.vertex.location
    )
    model = GoogleModel(config.vertex.analyst_model, provider=provider)

    agent = Agent(
        model=model,
        system_prompt=FINANCIAL_ANALYST_SYSTEM_PROMPT + "\n\n" + CODER_PROMPT,
        output_type=AnalystReport,
        retries=2,
    )
    from ..tools.financial_tools import (
        bq_safe_query,
        execute_python,
        get_artifact_metadata,
        get_attribution_breakdown,
        get_exposures,
        get_pnl_daily_summary,
        search_news,
    )

    agent.tool(get_pnl_daily_summary)
    agent.tool(get_attribution_breakdown)
    agent.tool(get_exposures)
    agent.tool(search_news)
    agent.tool(bq_safe_query)
    agent.tool(get_artifact_metadata)
    agent.tool(execute_python)
    return agent


def create_fact_checker_agent() -> Agent:
    """Create Fact Checker/Reviewer subagent."""
    config = get_config()
    provider = GoogleProvider(
        project=config.vertex.project_id, location=config.vertex.location
    )
    model = GoogleModel(config.vertex.root_model, provider=provider)

    agent = Agent(
        model=model,
        system_prompt=FACT_CHECKER_PROMPT,
        retries=2,
    )
    from ..tools.financial_tools import get_artifact_metadata

    agent.tool(get_artifact_metadata)
    return agent


def create_report_writer_agent() -> Agent:
    """Create Report Writer subagent."""
    config = get_config()
    provider = GoogleProvider(
        project=config.vertex.project_id, location=config.vertex.location
    )
    model = GoogleModel(config.vertex.root_model, provider=provider)

    agent = Agent(
        model=model,
        system_prompt=REPORT_WRITER_PROMPT,
        retries=2,
    )
    return agent


def create_root_agent() -> Agent:
    """Create Root orchestrator agent - NO code execution."""
    config = get_config()
    provider = GoogleProvider(
        project=config.vertex.project_id, location=config.vertex.location
    )
    model = GoogleModel(config.vertex.root_model, provider=provider)

    agent = Agent(
        model=model,
        system_prompt=ROOT_AGENT_SYSTEM_PROMPT,
        retries=2,
    )
    from ..tools.financial_tools import (
        delegate_to_fact_checker,
        delegate_to_financial_analyst,
        delegate_to_report_writer,
        discover_apis_tool,
        discover_data_sources_tool,
        discover_sandbox_capabilities_tool,
    )

    agent.tool(delegate_to_financial_analyst)
    agent.tool(delegate_to_fact_checker)
    agent.tool(delegate_to_report_writer)
    agent.tool(discover_data_sources_tool)
    agent.tool(discover_sandbox_capabilities_tool)
    agent.tool(discover_apis_tool)
    return agent
