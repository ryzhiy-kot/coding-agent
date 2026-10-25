from datetime import UTC, datetime

from ..schemas.artifacts import ArtifactMetadata, ArtifactRef


class ArtifactStore:
    """Artifact storage interface - implement with GCS/local in practice."""

    def __init__(self, bucket: str = "agent-artifacts"):
        self.bucket = bucket

    async def write(
        self, name: str, data: bytes, content_type: str = "application/octet-stream"
    ) -> ArtifactRef:
        # Placeholder - replace with actual upload
        uri = f"gs://{self.bucket}/{name}"
        return ArtifactRef(
            type="parquet" if name.endswith(".parquet") else "csv",
            mime=content_type,
            url=uri,
            name=name,
            created_at=datetime.now(UTC),
            bytes=len(data),
        )

    async def get_metadata(self, uri: str) -> ArtifactMetadata:
        # Placeholder - replace with actual inspection
        return ArtifactMetadata(
            uri=uri,
            summary="Artifact metadata not implemented in placeholder",
        )
