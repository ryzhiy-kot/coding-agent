from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field


class ArtifactRef(BaseModel):
    type: Literal["image", "table", "html", "json", "parquet", "csv"]
    mime: str
    url: str
    name: str | None = None
    caption: str | None = None
    rows: int | None = None
    bytes: int | None = None
    created_at: datetime | None = None
    metadata: dict[str, Any] | None = None


class ArtifactMetadata(BaseModel):
    uri: str
    shape_rows: int | None = None
    shape_cols: int | None = None
    columns: list[str] = Field(default_factory=list)
    dtypes: dict[str, str] = Field(default_factory=dict)
    size_bytes: int | None = None
    summary: str | None = None
