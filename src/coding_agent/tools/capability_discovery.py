from typing import Any

from pydantic_ai import RunContext

from ..config.settings import get_config


async def discover_data_sources(ctx: RunContext) -> dict[str, Any]:
    """Discover available BQ tables, schemas, and samples."""
    config = get_config()
    # Placeholder - replace with actual INFORMATION_SCHEMA queries
    return {
        "bq": {
            "project": config.bq.project_id,
            "datasets": [config.bq.dataset_pnl, config.bq.dataset_exposures],
            "tables": [],
            "note": "Use INFORMATION_SCHEMA to list tables/columns",
        }
    }


async def discover_sandbox_capabilities(ctx: RunContext) -> dict[str, Any]:
    """Discover available Python modules in sandbox."""
    config = get_config().sandbox
    return {
        "allowed_imports": config.allowed_imports,
        "blocked_imports": config.blocked_imports,
        "can_pip_install": config.allow_pip_install,
        "network_allowed": config.allow_network,
        "timeout_seconds": config.timeout_seconds,
    }


async def discover_apis(ctx: RunContext) -> dict[str, Any]:
    """Discover available internal APIs."""
    return {
        "news_api": get_config().news.base_url,
        "bq": True,
        "artifact_store": get_config().storage.local_dir,
    }
