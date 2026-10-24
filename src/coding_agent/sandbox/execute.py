from ..config.settings import get_config
from ..schemas.financial import CodeExecInput, CodeExecResult
from .execute_local import LocalSandboxExecutor


class CodeExecutor:
    """Execute Python in sandbox with limits."""

    def __init__(self):
        self.config = get_config().sandbox
        if self.config.provider == "local":
            self._impl = LocalSandboxExecutor()
        else:
            self._impl = LocalSandboxExecutor()  # fallback to local for now

    async def execute_python(
        self,
        code: str,
        inputs: list[CodeExecInput] | None = None,
    ) -> CodeExecResult:
        return await self._impl.execute_python(code, inputs)
