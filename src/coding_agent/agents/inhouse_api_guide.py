from textwrap import dedent

INHOUSE_API_GUIDE = dedent(
    """
    # In-House APIs (Available for Import in Code Execution)
    
    The sandbox has access to this codebase via PYTHONPATH. You can import and use
    in-house modules directly in executed Python code.
    
    ## Available Modules
    - `coding_agent.tools.*` - Data access tools (BQ, news, artifacts)
    - `coding_agent.schemas.*` - Pydantic schemas
    - `coding_agent.config.*` - Configuration
    - `coding_agent.sandbox.*` - Sandbox utilities
    
    ## Usage in execute_python
    ```python
    from coding_agent.tools.bq_guarded import GuardedBQ
    from coding_agent.tools.news import NewsClient
    from coding_agent.schemas.financial import *
    
    # Use in-house clients
    bq = GuardedBQ()
    # ... process artifacts ...
    ```
    
    ## Guidelines
    - Prefer using in-house APIs over reimplementing logic
    - Read artifacts from URIs passed as inputs
    - Write outputs (plots/tables) to current directory - they'll be collected as artifacts
    - Don't install packages (pip install disabled)
    - Respect guardrails - use typed clients
    """
).strip()
