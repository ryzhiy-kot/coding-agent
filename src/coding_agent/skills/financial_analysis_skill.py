from textwrap import dedent

FINANCIAL_ANALYSIS_SKILL = {
    "name": "financial-analysis",
    "description": "Investigate PnL movements using BQ, exposures, news, and sandboxed Python code.",
    "instructions": dedent(
        """
        # Financial Analysis Skill
        
        ## When to use
        - "PNL moved >X since date" or daily volatility questions
        - Need to explain drivers via attribution/exposures/news
        - Need charts/correlations computed from artifacts
        
        ## Workflow
        1. Get daily summary to identify large moves
        2. Drill into attribution by factor/strategy/desk
        3. Pull exposures and news for top contributors
        4. If needed, use execute_python on artifacts to analyze/visualize
        5. Report with evidence and artifact links
        
        ## Constraints
        - Use tools first, artifacts for large data
        - Summarize news, don't dump articles
        - No SELECT *, respect caps
        - Use in-house APIs in code when available
        """
    ).strip(),
    "tools": [
        "get_pnl_daily_summary",
        "get_attribution_breakdown",
        "get_exposures",
        "search_news",
        "bq_safe_query",
        "get_artifact_metadata",
        "execute_python",
    ],
}
