from datetime import date
from typing import Any

from ..config.settings import get_config
from ..schemas.financial import (
    AttributionBreakdown,
    BQSafeQueryResult,
    ExposuresResult,
    PnLDailySummary,
    PnLDailySummaryRow,
)
from .artifacts import ArtifactStore


class GuardedBQ:
    """Guardrailed BigQuery access with dry-run and caps."""

    def __init__(self):
        self.config = get_config().bq
        self.store = ArtifactStore()

    async def get_pnl_daily_summary(
        self,
        start_date: date,
        end_date: date,
        min_abs_move: float | None = 50000.0,
        max_rows_preview: int | None = None,
    ) -> PnLDailySummary:
        max_rows_preview = max_rows_preview or self.config.max_rows_preview
        # Placeholder implementation - replace with actual BQ queries
        rows: list[PnLDailySummaryRow] = []
        preview: list[dict[str, Any]] = []
        return PnLDailySummary(
            start_date=start_date,
            end_date=end_date,
            min_abs_move=min_abs_move,
            rows=rows,
            preview=preview,
            row_count=len(rows),
            artifact_uri=None,
        )

    async def get_attribution_breakdown(
        self,
        dates: list[date],
        group_by: list[str],
        max_rows_preview: int | None = None,
    ) -> AttributionBreakdown:
        max_rows_preview = max_rows_preview or self.config.max_rows_preview
        return AttributionBreakdown(
            dates=dates,
            group_by=group_by,
            preview=[],
            row_count=0,
            bytes_scanned_est=None,
            artifact_uri=None,
        )

    async def get_exposures(
        self,
        as_of: date,
        tickers: list[str],
        max_rows_preview: int | None = None,
    ) -> ExposuresResult:
        max_rows_preview = max_rows_preview or self.config.max_rows_preview
        return ExposuresResult(
            as_of=as_of,
            tickers=tickers,
            preview=[],
            row_count=0,
            artifact_uri=None,
        )

    async def bq_safe_query(
        self,
        template_name: str | None = None,
        sql: str | None = None,
        params: dict[str, Any] | None = None,
        max_rows: int | None = None,
        max_bytes: int | None = None,
    ) -> BQSafeQueryResult:
        max_rows = max_rows or self.config.max_rows_preview
        max_bytes = max_bytes or self.config.max_bytes_billed
        warnings: list[str] = []
        errors: list[str] = []

        if sql and not template_name:
            # Basic guardrails - extend with proper SQL parsing
            sql_upper = sql.upper()
            if "SELECT *" in sql_upper:
                errors.append("SELECT * is not allowed. Use explicit columns.")
            if "LIMIT" not in sql_upper and max_rows:
                sql = f"{sql.rstrip().rstrip(';')} LIMIT {max_rows}"

        if errors:
            return BQSafeQueryResult(ok=False, errors=errors, warnings=warnings)

        # Placeholder - implement dry-run and actual execution
        return BQSafeQueryResult(
            ok=True,
            template_name=template_name,
            sql=sql,
            preview=[],
            row_count=0,
            bytes_scanned_est=0,
            warnings=warnings,
            errors=[],
        )
