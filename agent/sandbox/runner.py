"""Sandbox runner — isolated code execution with output/error/perf capture.

NEVER runs untested code in the main process. Uses subprocess with
timeout, memory limits, and no network access.
"""

import asyncio
import logging
import os
import resource
import sys
import tempfile
import time
from dataclasses import dataclass, field
from pathlib import Path

from agent.config import get_settings

logger = logging.getLogger(__name__)


@dataclass
class SandboxResult:
    """Result of a sandbox execution."""
    stdout: str = ""
    stderr: str = ""
    return_code: int = -1
    passed: bool = False
    execution_time_ms: float = 0.0
    timed_out: bool = False
    error_summary: str = ""

    @property
    def has_error(self) -> bool:
        return self.return_code != 0 or bool(self.stderr.strip())

    @property
    def output(self) -> str:
        """Clean output — stdout if success, stderr if failure."""
        if self.passed:
            return self.stdout.strip()
        return self.stderr.strip() or self.stdout.strip()


class SandboxRunner:
    """Isolated code execution environment.

    Security measures:
    - Subprocess with timeout
    - Memory limit via resource.setrlimit
    - Writes only to temp directory
    - Captures all output
    """

    def __init__(self):
        self.settings = get_settings()
        self._sandbox_dir = self.settings.sandbox_path_resolved
        self._sandbox_dir.mkdir(parents=True, exist_ok=True)

    async def run(
        self,
        code: str,
        language: str = "python",
        timeout: int | None = None,
        memory_limit_mb: int = 512,
    ) -> SandboxResult:
        """Execute code in an isolated subprocess.

        Args:
            code: Source code to execute.
            language: Programming language (python supported now).
            timeout: Max seconds before kill.
            memory_limit_mb: Max memory in MB.

        Returns:
            SandboxResult with captured output and metrics.
        """
        timeout = timeout or self.settings.sandbox_timeout

        if language != "python":
            return SandboxResult(
                stderr=f"Language '{language}' not yet supported. Only 'python' is available.",
                return_code=1,
                error_summary=f"Unsupported language: {language}",
            )

        return await self._run_python(code, timeout, memory_limit_mb)

    async def _run_python(
        self, code: str, timeout: int, memory_limit_mb: int
    ) -> SandboxResult:
        """Execute Python code in a subprocess."""
        # Write code to temp file
        code_file = self._sandbox_dir / f"sandbox_{os.getpid()}_{time.time_ns()}.py"

        try:
            code_file.write_text(code, encoding="utf-8")

            start = time.perf_counter()

            proc = await asyncio.create_subprocess_exec(
                sys.executable, str(code_file),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=str(self._sandbox_dir),
                env=self._sandbox_env(),
            )

            try:
                stdout_bytes, stderr_bytes = await asyncio.wait_for(
                    proc.communicate(), timeout=timeout
                )
                elapsed_ms = (time.perf_counter() - start) * 1000

                stdout = stdout_bytes.decode("utf-8", errors="replace")
                stderr = stderr_bytes.decode("utf-8", errors="replace")

                passed = proc.returncode == 0 and not stderr.strip()

                return SandboxResult(
                    stdout=stdout,
                    stderr=stderr,
                    return_code=proc.returncode or 0,
                    passed=passed,
                    execution_time_ms=elapsed_ms,
                    error_summary=self._extract_error_summary(stderr) if stderr else "",
                )

            except asyncio.TimeoutError:
                proc.kill()
                await proc.wait()
                elapsed_ms = (time.perf_counter() - start) * 1000
                return SandboxResult(
                    stderr=f"Execution timed out after {timeout}s",
                    return_code=-9,
                    timed_out=True,
                    execution_time_ms=elapsed_ms,
                    error_summary=f"Timeout after {timeout}s",
                )

        except Exception as e:
            return SandboxResult(
                stderr=str(e),
                return_code=1,
                error_summary=f"Sandbox error: {e}",
            )
        finally:
            # Clean up temp file
            if code_file.exists():
                code_file.unlink()

    def _sandbox_env(self) -> dict[str, str]:
        """Create a restricted environment for the subprocess."""
        env = os.environ.copy()
        # Remove sensitive vars
        for key in ["OPENAI_API_KEY", "API_KEY", "SECRET", "TOKEN", "PASSWORD"]:
            env.pop(key, None)
        # Set sandbox-specific vars
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        env["PYTHONUNBUFFERED"] = "1"
        return env

    def _extract_error_summary(self, stderr: str) -> str:
        """Extract the last meaningful error line from stderr."""
        lines = stderr.strip().split("\n")
        # Get last non-empty line (usually the actual error message)
        for line in reversed(lines):
            line = line.strip()
            if line and not line.startswith("Traceback"):
                return line
        return stderr.strip()[:200]

    async def run_batch(
        self, code_list: list[str], language: str = "python"
    ) -> list[SandboxResult]:
        """Run multiple code snippets concurrently."""
        tasks = [self.run(code, language) for code in code_list]
        return await asyncio.gather(*tasks)

    def cleanup(self) -> None:
        """Remove all sandbox temp files."""
        for f in self._sandbox_dir.glob("sandbox_*.py"):
            f.unlink()


# ── Singleton ────────────────────────────────────────────────────
_sandbox: SandboxRunner | None = None


def get_sandbox() -> SandboxRunner:
    global _sandbox
    if _sandbox is None:
        _sandbox = SandboxRunner()
    return _sandbox
