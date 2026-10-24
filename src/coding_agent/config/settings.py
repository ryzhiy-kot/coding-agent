from pydantic import BaseModel, Field


class BQConfig(BaseModel):
    project_id: str = Field(default="your-project")
    dataset_pnl: str = Field(default="pnl")
    dataset_exposures: str = Field(default="exposures")
    max_bytes_billed: int = Field(default=10_000_000_000)
    max_rows_preview: int = Field(default=50)
    dry_run: bool = Field(default=True)


class NewsConfig(BaseModel):
    base_url: str = Field(default="https://api.example.com/news")
    max_items: int = Field(default=10)
    timeout_seconds: int = Field(default=30)


class SandboxConfig(BaseModel):
    provider: str = Field(default="local")
    timeout_seconds: int = Field(default=120)
    memory_mb: int = Field(default=512)
    disk_mb: int = Field(default=1024)
    allow_pip_install: bool = Field(default=False)
    allow_network: bool = Field(default=False)
    allowed_imports: list[str] = Field(
        default_factory=lambda: [
            "pandas",
            "numpy",
            "pyarrow",
            "duckdb",
            "matplotlib",
            "seaborn",
            "plotly",
            "scipy",
            "sklearn",
            "json",
            "csv",
            "datetime",
            "math",
            "statistics",
            "collections",
            "itertools",
            "functools",
            "pathlib",
            "typing",
        ]
    )
    blocked_imports: list[str] = Field(
        default_factory=lambda: [
            "subprocess",
            "os.system",
            "socket",
            "requests",
            "urllib",
            "http.client",
            "ctypes",
            "multiprocessing",
            "shutil",
            "tempfile",
            "pip",
            "setuptools",
            "distutils",
        ]
    )
    workdir: str = Field(default="/tmp/agent-sandbox")
    pythonpath_extra: list[str] = Field(default_factory=list)


class StorageConfig(BaseModel):
    bucket: str = Field(default="agent-artifacts")
    presign_ttl_seconds: int = Field(default=3600)
    local_dir: str = Field(default="/tmp/agent-artifacts")


class VertexConfig(BaseModel):
    project_id: str = Field(default="your-project")
    location: str = Field(default="us-central1")
    root_model: str = Field(default="google-gla:gemini-2.5-flash")
    analyst_model: str = Field(default="google-gla:gemini-2.5-pro")


class AppConfig(BaseModel):
    bq: BQConfig = Field(default_factory=BQConfig)
    news: NewsConfig = Field(default_factory=NewsConfig)
    sandbox: SandboxConfig = Field(default_factory=SandboxConfig)
    storage: StorageConfig = Field(default_factory=StorageConfig)
    vertex: VertexConfig = Field(default_factory=VertexConfig)


def get_config() -> AppConfig:
    return AppConfig()
