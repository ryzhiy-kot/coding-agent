"""Agent setup with pydantic_ai and Vertex AI."""

from google.genai.client import Client
from pydantic_ai import Agent
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider

from ..config.settings import get_config
from ..schemas.financial import AnalystReport
from .financial_analyst import FINANCIAL_ANALYST_SYSTEM_PROMPT
from .root import ROOT_AGENT_SYSTEM_PROMPT


def create_financial_analyst_agent() -> Agent[object, AnalystReport]:
    """Create Financial Analyst subagent."""
    config = get_config()
    client = Client(**config.vertex.model_dump())
    provider = GoogleProvider(client=client)
    model = GoogleModel(config.vertex.analyst_model, provider=provider)

    agent = Agent(
        model=model,
        system_prompt=FINANCIAL_ANALYST_SYSTEM_PROMPT,
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


def create_root_agent() -> Agent:
    """Create Root orchestrator agent."""
    config = get_config()
    client = Client(**config.vertex.model_dump())
    provider = GoogleProvider(client=client)
    model = GoogleModel(config.vertex.root_model, provider=provider)

    agent = Agent(
        model=model,
        system_prompt=ROOT_AGENT_SYSTEM_PROMPT,
        retries=2,
    )
    from ..tools.financial_tools import (
        delegate_to_financial_analyst,
        discover_apis_tool,
        discover_data_sources_tool,
        discover_sandbox_capabilities_tool,
    )

    agent.tool(delegate_to_financial_analyst)
    agent.tool(discover_data_sources_tool)
    agent.tool(discover_sandbox_capabilities_tool)
    agent.tool(discover_apis_tool)
    return agent
