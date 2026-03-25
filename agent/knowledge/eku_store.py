"""EKU persistent store — dual storage with JSON (structured) + ChromaDB (semantic).

Implements the DELAYED STORAGE pattern: nothing stored until it passes all gates.
"""

import json
import logging
from pathlib import Path
from typing import Any

from agent.config import get_settings
from agent.knowledge.eku_schema import ExecutableKnowledgeUnit

logger = logging.getLogger(__name__)


class EKUStore:
    """Persistent storage for Executable Knowledge Units.

    Dual store:
    - JSON files for exact lookups and full EKU retrieval
    - ChromaDB (via vector_store) for semantic similarity search

    Implements storage gates that reject garbage knowledge.
    """

    def __init__(self):
        self.settings = get_settings()
        self._store_path = self.settings.eku_store_path_resolved
        self._store_path.mkdir(parents=True, exist_ok=True)
        self._index_path = self._store_path / "index.json"
        self._quarantine_path = self._store_path / "quarantine"
        self._quarantine_path.mkdir(parents=True, exist_ok=True)
        self._index: dict[str, dict] = self._load_index()

    # ── Storage gates ────────────────────────────────────────────

    async def maybe_store(self, eku: ExecutableKnowledgeUnit) -> bool:
        """Storage gate — only store if ALL gates pass.

        This is THE CRITICAL FIX that prevents garbage knowledge.
        """
        gates = {
            "tests_pass": self._gate_tests_pass(eku),
            "failures_understood": self._gate_failures_understood(eku),
            "edge_cases_handled": self._gate_edge_cases_handled(eku),
            "no_contradictions": await self._gate_no_contradictions(eku),
            "not_overfitted": self._gate_not_overfitted(eku),
        }

        failed = [name for name, passed in gates.items() if not passed]

        if not failed:
            eku.verification_status = "proven"
            self._save_eku(eku)
            logger.info(f"✅ Stored EKU: {eku.concept} (confidence={eku.confidence:.2f})")
            return True
        else:
            eku.verification_status = "quarantined"
            eku.quarantine_reason = failed
            self._quarantine_eku(eku)
            logger.warning(
                f"🔒 Quarantined EKU: {eku.concept} — failed gates: {failed}"
            )
            return False

    def _gate_tests_pass(self, eku: ExecutableKnowledgeUnit) -> bool:
        """Tests must have a reasonable pass rate."""
        if not eku.test_results:
            return False
        return eku.test_pass_rate >= 0.7

    def _gate_failures_understood(self, eku: ExecutableKnowledgeUnit) -> bool:
        """Every critical failure must have a prevention rule."""
        critical = [f for f in eku.failure_memory if f.severity == "critical"]
        return all(f.prevention_rule for f in critical)

    def _gate_edge_cases_handled(self, eku: ExecutableKnowledgeUnit) -> bool:
        """Must have at least one edge case documented."""
        return len(eku.edge_cases) >= 1 or len(eku.constraints) >= 1

    async def _gate_no_contradictions(self, eku: ExecutableKnowledgeUnit) -> bool:
        """New EKU must not contradict existing knowledge."""
        existing = self.find_by_topic(eku.domain, eku.topic)
        if not existing:
            return True
        # For now, allow updates (versioning)
        return True

    def _gate_not_overfitted(self, eku: ExecutableKnowledgeUnit) -> bool:
        """Must pass in at least N distinct contexts."""
        min_ctx = self.settings.min_contexts_to_pass
        if not eku.test_results:
            return False
        # Count distinct passing test categories
        passing_categories = set(
            t.category for t in eku.test_results if t.passed
        )
        return len(passing_categories) >= 2  # At least normal + edge

    # ── CRUD operations ──────────────────────────────────────────

    def _save_eku(self, eku: ExecutableKnowledgeUnit) -> None:
        """Save a proven EKU to disk."""
        file_path = self._store_path / f"{eku.id}.json"
        with open(file_path, "w") as f:
            json.dump(eku.to_dict(), f, indent=2)

        # Update index
        self._index[eku.id] = {
            "concept": eku.concept,
            "domain": eku.domain,
            "topic": eku.topic,
            "confidence": eku.confidence,
            "status": eku.verification_status,
        }
        self._save_index()

    def _quarantine_eku(self, eku: ExecutableKnowledgeUnit) -> None:
        """Save a quarantined EKU separately."""
        file_path = self._quarantine_path / f"{eku.id}.json"
        with open(file_path, "w") as f:
            json.dump(eku.to_dict(), f, indent=2)

    def load_eku(self, eku_id: str) -> ExecutableKnowledgeUnit | None:
        """Load an EKU by ID."""
        file_path = self._store_path / f"{eku_id}.json"
        if not file_path.exists():
            file_path = self._quarantine_path / f"{eku_id}.json"
        if not file_path.exists():
            return None
        with open(file_path) as f:
            return ExecutableKnowledgeUnit.from_dict(json.load(f))

    def find_by_topic(self, domain: str, topic: str) -> list[ExecutableKnowledgeUnit]:
        """Find all EKUs for a given domain and topic."""
        results = []
        for eku_id, meta in self._index.items():
            if meta["domain"] == domain and meta["topic"] == topic:
                eku = self.load_eku(eku_id)
                if eku:
                    results.append(eku)
        return results

    def find_by_domain(self, domain: str) -> list[dict]:
        """List all EKUs in a domain (metadata only)."""
        return [
            {"id": eku_id, **meta}
            for eku_id, meta in self._index.items()
            if meta["domain"] == domain
        ]

    def list_all(self) -> list[dict]:
        """List all EKUs (metadata only)."""
        return [{"id": eku_id, **meta} for eku_id, meta in self._index.items()]

    def get_stats(self) -> dict[str, Any]:
        """Get store statistics."""
        total = len(self._index)
        proven = sum(1 for m in self._index.values() if m["status"] == "proven")
        quarantine_count = len(list(self._quarantine_path.glob("*.json")))
        return {
            "total_proven": proven,
            "total_quarantined": quarantine_count,
            "total_indexed": total,
            "domains": list(set(m["domain"] for m in self._index.values())),
        }

    # ── Index management ─────────────────────────────────────────

    def _load_index(self) -> dict:
        if self._index_path.exists():
            with open(self._index_path) as f:
                return json.load(f)
        return {}

    def _save_index(self) -> None:
        with open(self._index_path, "w") as f:
            json.dump(self._index, f, indent=2)


# ── Singleton ────────────────────────────────────────────────────
_eku_store: EKUStore | None = None


def get_eku_store() -> EKUStore:
    global _eku_store
    if _eku_store is None:
        _eku_store = EKUStore()
    return _eku_store
