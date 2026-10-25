from datetime import date
from typing import Any

from pydantic import BaseModel, Field

from .artifacts import ArtifactRef


class PnLDailySummaryRow(BaseModel):
    date: date
    pnl_total: float
    abs_move: float
    currency: str = "USD"
    top_contributors: list[dict[str, Any]] = Field(default_factory=list)
    drivers_summary: str | None = None


class PnLDailySummary(BaseModel):
    start_date: date
    end_date: date
    min_abs_move: float | None = None
    rows: list[PnLDailySummaryRow] = Field(default_factory=list)
    preview: list[dict[str, Any]] = Field(default_factory=list)
    artifact_uri: str | None = None
    row_count: int = 0


class AttributionBreakdown(BaseModel):
    dates: list[date]
    group_by: list[str]
    preview: list[dict[str, Any]] = Field(default_factory=list)
    artifact_uri: str | None = None
    row_count: int = 0
    bytes_scanned_est: int | None = None


class ExposureRow(BaseModel):
    ticker: str
    book: str | None = None
    notional: float | None = None
    delta: float | None = None
    sector: str | None = None
    factor_exposures: dict[str, float] = Field(default_factory=dict)
    as_of: date | None = None


class ExposuresResult(BaseModel):
    as_of: date
    tickers: list[str]
    preview: list[ExposureRow] = Field(default_factory=list)
    artifact_uri: str | None = None
    row_count: int = 0


class NewsItem(BaseModel):
    title: str
    source: str | None = None
    published_at: str | None = None
    url: str | None = None
    summary: str
    tickers: list[str] = Field(default_factory=list)


class NewsResult(BaseModel):
    tickers: list[str]
    start: date
    end: date
    items: list[NewsItem] = Field(default_factory=list)
    truncated: bool = True


class BQSafeQueryResult(BaseModel):
    ok: bool
    template_name: str | None = None
    sql: str | None = None
    preview: list[dict[str, Any]] = Field(default_factory=list)
    row_count: int = 0
    bytes_scanned_est: int | None = None
    artifact_uri: str | None = None
    warnings: list[str] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)


class CodeExecInput(BaseModel):
    name: str
    uri: str


class CodeExecResult(BaseModel):
    ok: bool
    stdout: str = ""
    stderr: str = ""
    summary: str = ""
    artifacts: list[ArtifactRef] = Field(default_factory=list)
    runtime_ms: int | None = None
    mem_mb_peak: int | None = None


class AnalystReport(BaseModel):
    summary: str
    drivers: list[dict[str, Any]] = Field(default_factory=list)
    evidence: list[dict[str, Any]] = Field(default_factory=list)
    artifacts: list[ArtifactRef] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)
