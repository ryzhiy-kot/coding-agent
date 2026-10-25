import asyncio
import json
import os
import subprocess
import sys
import time
import uuid
from pathlib import Path

from ..config.settings import get_config
from ..schemas.artifacts import ArtifactRef
from ..schemas.financial import CodeExecInput, CodeExecResult


class SandboxError(Exception):
    pass


class LocalSandboxExecutor:
    """Local sandboxed execution with import restrictions and artifact handling."""

    def __init__(self):
        self.config = get_config().sandbox
        self.storage = get_config().storage
        self.workdir = Path(self.config.workdir)
        self.workdir.mkdir(parents=True, exist_ok=True)
        self.artifacts_dir = Path(self.storage.local_dir)
        self.artifacts_dir.mkdir(parents=True, exist_ok=True)

    def _check_imports(self, code: str) -> tuple[bool, list[str]]:
        issues = []
        for blocked in self.config.blocked_imports:
            if blocked in code:
                issues.append(f"Blocked import/reference: {blocked}")
        return len(issues) == 0, issues

    async def execute_python(
        self,
        code: str,
        inputs: list[CodeExecInput] | None = None,
    ) -> CodeExecResult:
        start = time.time()
        inputs = inputs or []

        ok, issues = self._check_imports(code)
        if not ok:
            return CodeExecResult(
                ok=False,
                stderr="\n".join(issues),
                summary="Import restrictions violated",
                artifacts=[],
                runtime_ms=int((time.time() - start) * 1000),
            )

        run_id = str(uuid.uuid4())
        run_dir = self.workdir / run_id
        run_dir.mkdir(parents=True, exist_ok=True)

        inputs_meta = [{"name": i.name, "uri": i.uri} for i in inputs]
        (run_dir / "inputs.json").write_text(json.dumps(inputs_meta, indent=2))

        env = os.environ.copy()
        pythonpath = env.get("PYTHONPATH", "")
        extras = ":".join(self.config.pythonpath_extra)
        if extras:
            env["PYTHONPATH"] = f"{extras}:{pythonpath}" if pythonpath else extras

        code_file = run_dir / "script.py"
        code_file.write_text(code)

        try:
            proc = await asyncio.to_thread(
                subprocess.run,
                [sys.executable, str(code_file)],
                cwd=str(run_dir),
                env=env,
                timeout=self.config.timeout_seconds,
                capture_output=True,
                text=True,
                check=False,
            )
            stdout = proc.stdout[-8000:] if proc.stdout else ""
            stderr = proc.stderr[-8000:] if proc.stderr else ""
            ok_run = proc.returncode == 0
        except subprocess.TimeoutExpired:
            return CodeExecResult(
                ok=False,
                stderr=f"Execution timed out after {self.config.timeout_seconds}s",
                summary="Timeout",
                artifacts=[],
                runtime_ms=int((time.time() - start) * 1000),
            )
        except (OSError, ValueError):
            return CodeExecResult(
                ok=False,
                stderr="Execution error",
                summary="Execution error",
                artifacts=[],
                runtime_ms=int((time.time() - start) * 1000),
            )

        artifacts: list[ArtifactRef] = []
        for ext, mime, atype in [
            (".png", "image/png", "image"),
            (".jpg", "image/jpeg", "image"),
            (".jpeg", "image/jpeg", "image"),
            (".svg", "image/svg+xml", "image"),
            (".html", "text/html", "html"),
            (".csv", "text/csv", "table"),
            (".parquet", "application/parquet", "parquet"),
            (".json", "application/json", "json"),
        ]:
            for f in run_dir.glob(f"*{ext}"):
                dest = self.artifacts_dir / f"{run_id}_{f.name}"
                dest.write_bytes(f.read_bytes())
                artifacts.append(
                    ArtifactRef(
                        type=atype,
                        mime=mime,
                        url=f"file://{dest}",
                        name=f.name,
                        caption=f"Generated {f.name}",
                        bytes=dest.stat().st_size,
                    )
                )

        summary = stdout.strip().split("\n")[-5:] if stdout.strip() else []
        summary_text = (
            " | ".join(summary) if summary else ("Success" if ok_run else "Failed")
        )

        return CodeExecResult(
            ok=ok_run,
            stdout=stdout,
            stderr=stderr,
            summary=summary_text,
            artifacts=artifacts,
            runtime_ms=int((time.time() - start) * 1000),
            mem_mb_peak=None,
        )
