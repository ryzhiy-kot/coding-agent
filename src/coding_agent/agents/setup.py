"""Agent setup with pydantic_ai and Vertex AI."""

from pydantic_ai import Agent
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers import google_cloud

from ..config.settings import get_config
from ..schemas.financial import AnalystReport
from .financial_analyst import FINANCIAL_ANALYST_SYSTEM_PROMPT
from .root import ROOT_AGENT_SYSTEM_PROMPT


def create_financial_analyst_agent() -> Agent[object, AnalystReport]:
    """Create Financial Analyst subagent."""
    config = get_config()
    provider = google_cloud.GoogleCloudProvider(
        project=config.vertex.project_id,
        location=config.vertex.location,
    )
    model = GoogleModel(config.vertex.analyst_model, provider=provider)

    agent = Agent(
        model=model,
        system_prompt=FINANCIAL_ANALYST_SYSTEM_PROMPT,
        output_type=AnalystReport,
        retries=2,
    )
    return agent


def create_root_agent() -> Agent:
    """Create Root orchestrator agent."""
    config = get_config()
    provider = google_cloud.GoogleCloudProvider(
        project=config.vertex.project_id,
        location=config.vertex.location,
    )
    model = GoogleModel(config.vertex.root_model, provider=provider)

    agent = Agent(
        model=model,
        system_prompt=ROOT_AGENT_SYSTEM_PROMPT,
        retries=2,
    )
    # Wire delegation tool
    from ..tools.financial_tools import delegate_to_financial_analyst

    agent.tool(delegate_to_financial_analyst)
    return agent
