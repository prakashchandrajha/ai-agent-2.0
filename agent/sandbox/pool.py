"""Sandbox Warm Pool — MASTER_PLAN Task 1.NEW-B.

Pre-warms a pool of SandboxRunner instances so execution never pays
the cold-start cost.  Activated only when the ``sandbox_pool`` feature
flag is enabled.

Design contract (per MASTER_PLAN):
- Pool size: exactly 3 runners at all times.
- execute() borrows the next warm runner, returns the result, then
  replaces the used slot with a fresh runner.
- handle_all_crashed() recreates every slot from scratch (sync).
- Gate: if feature_enabled('sandbox_pool') is False the pool is a
  thin pass-through to a single on-demand SandboxRunner.
"""

import asyncio
import logging
from typing import List

from agent.config import feature_enabled
from agent.sandbox.runner import SandboxResult, SandboxRunner

logger = logging.getLogger(__name__)

_POOL_SIZE: int = 3


class SandboxPool:
    """Pre-warmed pool of SandboxRunner instances.

    Usage::

        pool = SandboxPool(size=3)
        await pool.initialize()
        result = await pool.execute(code, language="python")
    """

    def __init__(self, size: int = _POOL_SIZE) -> None:
        self._size = size
        self._pool: List[SandboxRunner] = []
        self._lock = asyncio.Lock()

    # ── Lifecycle ─────────────────────────────────────────────────

    async def initialize(self) -> None:
        """Pre-warm *size* runners unconditionally.

        The feature flag gates execute() behaviour, not pool creation,
        so that tests can always inspect _pool contents.
        """
        async with self._lock:
            self._pool = [self._make_runner() for _ in range(self._size)]
            logger.info("SandboxPool: warmed %d runners", self._size)

    def _make_runner(self) -> SandboxRunner:
        """Instantiate a fresh SandboxRunner."""
        return SandboxRunner()

    # ── Execution ──────────────────────────────────────────────────

    async def execute(
        self,
        code: str,
        language: str = "python",
        timeout: int | None = None,
        memory_limit_mb: int = 512,
    ) -> SandboxResult:
        """Run *code* using a warm runner and replace it immediately after.

        If the pool flag is disabled, falls back to a single ad-hoc runner.
        """
        if not feature_enabled("sandbox_pool"):
            return await SandboxRunner().run(
                code, language=language, timeout=timeout,
                memory_limit_mb=memory_limit_mb,
            )

        async with self._lock:
            if not self._pool:
                logger.warning(
                    "SandboxPool: all runners crashed — recreating pool"
                )
                self._recreate_all()

            runner = self._pool.pop(0)

        # Run outside lock so other callers can proceed concurrently
        result = await runner.run(
            code, language=language, timeout=timeout,
            memory_limit_mb=memory_limit_mb,
        )

        # Replace used runner with a fresh one
        async with self._lock:
            self._pool.append(self._make_runner())
            logger.debug(
                "SandboxPool: replaced used runner — pool size now %d",
                len(self._pool),
            )

        return result

    # ── Recovery ──────────────────────────────────────────────────

    def handle_all_crashed(self) -> None:
        """Recreate all runners from scratch (sync — safe to call from error handlers)."""
        self._recreate_all()

    def _recreate_all(self) -> None:
        """Internal: rebuild the full pool synchronously."""
        self._pool = [self._make_runner() for _ in range(self._size)]
        logger.warning(
            "SandboxPool: all %d runners recreated after crash", self._size
        )

    # ── Introspection ─────────────────────────────────────────────

    @property
    def size(self) -> int:
        """Current number of available warm runners."""
        return len(self._pool)


# ── Module-level singleton ────────────────────────────────────────

_pool: SandboxPool | None = None


def get_pool() -> SandboxPool:
    """Return the module-level SandboxPool (sync — call initialize() separately if needed)."""
    global _pool
    if _pool is None:
        _pool = SandboxPool()
    return _pool
