from typing import Any

from pydantic_ai import RunContext

from ..config.settings import get_config


async def discover_data_sources(_: RunContext) -> dict[str, Any]:
    """Discover available BQ tables, schemas, and samples."""
    config = get_config()
    return {
        "bq": {
            "project": config.bq.project_id,
            "datasets": [config.bq.dataset_pnl, config.bq.dataset_exposures],
            "tables": [],
            "note": "Use INFORMATION_SCHEMA to list tables/columns",
        }
    }


async def discover_sandbox_capabilities(_: RunContext) -> dict[str, Any]:
    """Discover available Python modules in sandbox."""
    config = get_config().sandbox
    return {
        "allowed_imports": config.allowed_imports,
        "blocked_imports": config.blocked_imports,
        "can_pip_install": config.allow_pip_install,
        "network_allowed": config.allow_network,
        "timeout_seconds": config.timeout_seconds,
    }


async def discover_apis(_: RunContext) -> dict[str, Any]:
    """Discover available internal APIs."""
    config = get_config()
    return {
        "news_api": config.news.base_url,
        "bq": True,
        "artifact_store": config.storage.local_dir,
    }
