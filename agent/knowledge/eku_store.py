"""EKU persistent store — dual storage with JSON (structured) + ChromaDB (semantic).

Implements the DELAYED STORAGE pattern: nothing stored until it passes all gates.
"""

import asyncio
import json
import logging
import os
from pathlib import Path
from typing import Any

from agent.config import get_settings
from agent.knowledge.eku_schema import ExecutableKnowledgeUnit, GateDiagnostic
from agent.utils.file_lock import file_lock, atomic_json_write

logger = logging.getLogger(__name__)

# ── MASTER_PLAN 1.NEW-E: Quarantine with Re-Learning Hints ──────────────
GATE_FIX_HINTS: dict[str, list[str]] = {
    "_gate_not_trivial": [
        "EKU is missing concept, topic or definition — ensure extraction produced output",
        "Try: python -m agent learn {concept} --sources official",
    ],
    "_gate_entropy": [
        "Knowledge confidence too low: python -m agent similar {concept}",
        "Consider if this is genuinely new or an alias for existing knowledge",
    ],
    "_gate_tests_pass": [
        "Try: MAX_LEARNING_ITERATIONS=5 python -m agent learn {concept}",
        "Try: python -m agent learn {concept} --sources official",
        "Check prerequisites: python -m agent deps {concept}",
    ],
    "_gate_not_overfitted": [
        "Knowledge too narrow — learn broader topic first",
        "Try: python -m agent suggest-prereqs {concept}",
    ],
    "_gate_no_contradictions": [
        "Run more iterations to improve confidence: MAX_LEARNING_ITERATIONS=5",
        "Inspect existing EKU: python -m agent inspect {concept}",
    ],
    "_gate_mastery_contract": [
        "Re-learn with more iterations: MAX_LEARNING_ITERATIONS=5",
        "Add specific documentation URL: python -m agent learn {concept} --url <url>",
    ],
}


# ── MASTER_PLAN 1.NEW-D: Graduated Gate Thresholds ─────────────────────
_BASE_THRESHOLDS: dict[str, float | int] = {
    "tests_pass":     0.70,
    "entropy":        0.85,
    "not_trivial":    0.30,  # definition length ratio
    "not_overfitted": 2,    # distinct passing categories (int, no scaling)
}


def get_gate_threshold(
    gate_name: str,
    iteration: int = 1,
    is_relearn: bool = False,
) -> float | int:
    """Return the effective gate threshold given context.

    - First attempt (iteration==1, not relearn): slightly lenient (-0.10).
    - Re-learning (replacing existing EKU): stricter (+0.10).
    - Otherwise: base threshold.
    """
    base = _BASE_THRESHOLDS.get(gate_name, 0.70)
    if isinstance(base, int):
        return base  # Integer thresholds don't scale
    if is_relearn:
        return min(base + 0.10, 0.99)
    if iteration == 1:
        return max(base - 0.10, 0.0)
    return base



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

        Uses short-circuit evaluation: stops on first failure.
        """
        if await self._validate_all_gates(eku):
            eku.verification_status = "proven"
            self._save_eku(eku)
            logger.info(f"✅ Stored EKU: {eku.concept} (confidence={eku.confidence:.2f})")
            return True
        else:
            eku.verification_status = "quarantined"
            # Quarantine reason is now populated by the specific gate that failed
            self._quarantine_eku(eku)
            logger.warning(
                f"🔒 Quarantined EKU: {eku.concept} — failed gates: {eku.quarantine_reason}"
            )
            return False

    async def _validate_all_gates(self, eku: ExecutableKnowledgeUnit) -> bool:
        """Run gates in order: cheapest first, expensive last.
        
        Short-circuit: return False on first failure.
        """
        # Reset quarantine reason for fresh validation
        eku.quarantine_reason = []

        # Order: trivial, entropy, tests, overfit, contradict, contract
        gates = [
            ("_gate_not_trivial", self._gate_not_trivial),
            ("_gate_entropy", self._gate_entropy),
            ("_gate_tests_pass", self._gate_tests_pass),
            ("_gate_not_overfitted", self._gate_not_overfitted),
            ("_gate_no_contradictions", self._gate_no_contradictions),
            ("_gate_mastery_contract", self._gate_mastery_contract),
        ]

        for name, gate in gates:
            try:
                result = gate(eku)
                if asyncio.iscoroutine(result):
                    passed = await result
                else:
                    passed = result
                
                if not passed:
                    eku.quarantine_reason.append(name)
                    return False
            except Exception as e:
                logger.error(f"Error in gate {name}: {e}")
                eku.quarantine_reason.append(f"{name}_error")
                return False
        
        return True

    def _gate_not_trivial(self, eku: ExecutableKnowledgeUnit) -> bool:
        """Basic checks: Must have concept, topic, and definition."""
        threshold = get_gate_threshold("not_trivial")
        if not eku.concept or not eku.topic or not eku.definition:
            eku.gate_diagnostics.append(GateDiagnostic(
                gate_name="not_trivial",
                failure_reason="EKU missing concept, topic, or definition",
                actual_value=0.0,
                required_value=float(threshold),
                suggested_fix=GATE_FIX_HINTS["_gate_not_trivial"][0],
                is_retryable=True,
            ))
            return False
        if len(eku.definition.strip()) < 10:
            eku.gate_diagnostics.append(GateDiagnostic(
                gate_name="not_trivial",
                failure_reason=f"Definition too short ({len(eku.definition.strip())} chars, need >= 10)",
                actual_value=float(len(eku.definition.strip())),
                required_value=10.0,
                suggested_fix=GATE_FIX_HINTS["_gate_not_trivial"][1],
                is_retryable=True,
            ))
            return False
        return True

    def _gate_entropy(self, eku: ExecutableKnowledgeUnit) -> bool:
        """Check if EKU meets the required entropy/confidence threshold."""
        threshold = get_gate_threshold("entropy")
        if eku.confidence < threshold:
            eku.gate_diagnostics.append(GateDiagnostic(
                gate_name="entropy",
                failure_reason=(
                    f"Confidence {eku.confidence:.2f} below threshold {threshold:.2f}"
                ),
                actual_value=eku.confidence,
                required_value=float(threshold),
                suggested_fix=GATE_FIX_HINTS["_gate_entropy"][0],
                is_retryable=True,
            ))
            return False
        return True

    def _gate_tests_pass(self, eku: ExecutableKnowledgeUnit) -> bool:
        """Tests must have a reasonable pass rate."""
        threshold = get_gate_threshold("tests_pass")
        if not eku.test_results:
            eku.gate_diagnostics.append(GateDiagnostic(
                gate_name="tests_pass",
                failure_reason="No test results recorded",
                actual_value=0.0,
                required_value=float(threshold),
                suggested_fix=GATE_FIX_HINTS["_gate_tests_pass"][0],
                is_retryable=True,
            ))
            return False
        pass_rate = eku.test_pass_rate
        if pass_rate < threshold:
            total = len(eku.test_results)
            passed = sum(1 for t in eku.test_results if t.passed)
            eku.gate_diagnostics.append(GateDiagnostic(
                gate_name="tests_pass",
                failure_reason=(
                    f"Only {passed}/{total} tests passed "
                    f"({pass_rate:.0%}). Required: >= {threshold:.0%}"
                ),
                actual_value=pass_rate,
                required_value=float(threshold),
                suggested_fix=GATE_FIX_HINTS["_gate_tests_pass"][0],
                is_retryable=True,
            ))
            return False
        return True

    def _gate_failures_understood(self, eku: ExecutableKnowledgeUnit) -> bool:
        """Every critical failure must have a prevention rule."""
        critical = [f for f in eku.failure_memory if f.severity == "critical"]
        return all(f.prevention_rule for f in critical)

    def _gate_edge_cases_handled(self, eku: ExecutableKnowledgeUnit) -> bool:
        """Must have at least one edge case documented."""
        return len(eku.edge_cases) >= 1 or len(eku.constraints) >= 1

    async def _gate_no_contradictions(self, eku: ExecutableKnowledgeUnit) -> bool:
        """New EKU must not contradict existing knowledge.

        Reject if existing EKU for same topic has confidence > new + 0.15.
        If new is equal or better, allow replacement and bump version.
        """
        existing = self.find_by_topic(eku.domain, eku.topic)
        if not existing:
            return True

        best_existing = max(existing, key=lambda e: e.confidence)

        if best_existing.confidence > eku.confidence + 0.15:
            eku.gate_diagnostics.append(GateDiagnostic(
                gate_name="no_contradictions",
                failure_reason=(
                    f"Existing EKU is significantly better "
                    f"({best_existing.confidence:.2f} vs {eku.confidence:.2f})"
                ),
                actual_value=eku.confidence,
                required_value=best_existing.confidence,
                suggested_fix=GATE_FIX_HINTS["_gate_no_contradictions"][0],
                is_retryable=True,
            ))
            return False

        # New EKU is equal or better — allow replacement, bump version
        eku.version = best_existing.version + 1
        return True

    def _gate_not_overfitted(self, eku: ExecutableKnowledgeUnit) -> bool:
        """Must pass in at least N distinct test categories (not_overfitted)."""
        required = int(get_gate_threshold("not_overfitted"))
        if not eku.test_results:
            eku.gate_diagnostics.append(GateDiagnostic(
                gate_name="not_overfitted",
                failure_reason="No test results — cannot verify category diversity",
                actual_value=0.0,
                required_value=float(required),
                suggested_fix=GATE_FIX_HINTS["_gate_not_overfitted"][0],
                is_retryable=True,
            ))
            return False
        passing_categories = {t.category for t in eku.test_results if t.passed}
        if len(passing_categories) < required:
            eku.gate_diagnostics.append(GateDiagnostic(
                gate_name="not_overfitted",
                failure_reason=(
                    f"Only {len(passing_categories)} distinct category(ies) passed "
                    f"({passing_categories}). Need >= {required}."
                ),
                actual_value=float(len(passing_categories)),
                required_value=float(required),
                suggested_fix=GATE_FIX_HINTS["_gate_not_overfitted"][0],
                is_retryable=True,
            ))
            return False
        return True

    async def _gate_mastery_contract(self, eku: ExecutableKnowledgeUnit) -> bool:
        """Check every criterion in mastery_criteria_unmet; emit diagnostic if any unmet."""
        unmet = list(eku.mastery_criteria_unmet)  # already populated by compressor

        # Also check that at least 1 criterion is met
        if not eku.mastery_criteria_met and not unmet:
            # No contract at all — trivially pass (contract not generated yet)
            return True

        if unmet:
            eku.gate_diagnostics.append(GateDiagnostic(
                gate_name="mastery_contract",
                failure_reason=f"Unmet criteria: {unmet}",
                actual_value=float(len(eku.mastery_criteria_met)),
                required_value=float(
                    len(eku.mastery_criteria_met) + len(unmet)
                ),
                suggested_fix=GATE_FIX_HINTS["_gate_mastery_contract"][0],
                is_retryable=True,
            ))
            return False
        return True

    # ── CRUD operations ──────────────────────────────────────────

    def _save_eku(self, eku: ExecutableKnowledgeUnit) -> None:
        """Save a proven EKU to disk."""
        file_path = self._store_path / f"{eku.id}.json"
        atomic_json_write(file_path, eku.to_dict())

        # Update index
        with file_lock(str(self._index_path)):
            self._index = self._load_index_no_lock()  # Safe reload
            self._index[eku.id] = {
                "concept": eku.concept,
                "domain": eku.domain,
                "topic": eku.topic,
                "confidence": eku.confidence,
                "status": eku.verification_status,
            }
            # Lock acquired!
            try:
                self._save_index_no_lock()
            except (IOError, OSError) as e:
                # EACCES and EAGAIN are the expected errors when lock is held
                logger.error(f"Failed to save index: {e}")
                raise

    def _quarantine_eku(self, eku: ExecutableKnowledgeUnit) -> None:
        """Save a quarantined EKU separately."""
        file_path = self._quarantine_path / f"{eku.id}.json"
        
        with file_lock(str(file_path)):
            with open(file_path, "w") as f:
                json.dump(eku.to_dict(), f, indent=2)

    def load_eku(self, eku_id: str) -> ExecutableKnowledgeUnit | None:
        """Load an EKU by ID."""
        file_path = self._store_path / f"{eku_id}.json"
        if not file_path.exists():
            file_path = self._quarantine_path / f"{eku_id}.json"
        if not file_path.exists():
            return None
        
        with file_lock(str(file_path)):
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

    def calculate_effective_confidence(self, eku_id: str) -> tuple[float, str]:
        """Calculate the real effective confidence considering dependency chain.
        Returns (effective_confidence, chain_description).
        
        Example: A(0.95) -> B(0.90) -> C(0.85)
        Using C: effective = 0.85 * 0.90 * 0.95 = 0.73
        """
        eku = self.load_eku(eku_id)
        if not eku:
            return 0.0, f"EKU {eku_id} not found"
        
        if not eku.dependencies:
            return eku.confidence, f"{eku.concept}({eku.confidence:.2f})"
        
        # We collect ALL unique dependencies in the chain (BFS)
        visited = {eku_id}
        queue = list(eku.dependencies)
        chain_ekus = [eku]
        
        idx = 0
        while idx < len(queue):
            dep_id = queue[idx]
            idx += 1
            if dep_id in visited:
                continue
            visited.add(dep_id)
            
            dep_eku = self.load_eku(dep_id)
            if dep_eku:
                chain_ekus.append(dep_eku)
                queue.extend(dep_eku.dependencies)
        
        # Calculation: Product of all confidences in the unique chain set
        effective = 1.0
        chain_parts = []
        for reku in chain_ekus:
            effective *= reku.confidence
            chain_parts.append(f"{reku.concept}({reku.confidence:.2f})")
            
        chain_desc = " * ".join(chain_parts) + f" = {effective:.2f}"
        return effective, chain_desc

    def rollback_eku(self, eku_id: str, dry_run: bool = False) -> list[str]:
        """Evolutionary rollback: delete an EKU and all its downstream dependents.
        
        Cascades DOWNSTREAM: if B depends on A, rolling back A also rolls back B.
        Returns a list of dependent IDs that were (or would be) affected.
        """
        if eku_id not in self._index:
            return []
            
        # 1. Find all affected IDs recursively
        affected_ids = self._find_all_downstream(eku_id)
        
        # 2. Prepare result (dependents only)
        dependents_only = sorted(list(set(affected_ids) - {eku_id}))
        
        if dry_run:
            return dependents_only
            
        # 3. Perform actual deletion for everyone in affected_ids
        with file_lock(str(self._index_path)):
            self._index = self._load_index_no_lock()
            
            for rid in affected_ids:
                # Delete files
                file_path = self._store_path / f"{rid}.json"
                quarantine_path = self._quarantine_path / f"{rid}.json"
                
                if file_path.exists():
                    file_path.unlink()
                if quarantine_path.exists():
                    quarantine_path.unlink()
                
                # Remove from index memory
                if rid in self._index:
                    del self._index[rid]
                
                logger.warning(f"⏪ Rolled back EKU {rid}")
            
            # Save index once
            self._save_index_no_lock()
            
        return dependents_only

    def _find_all_downstream(self, eku_id: str) -> list[str]:
        """Find all EKUs that recursively depend on the given ID."""
        # 1. Build the full dependency map from disk
        all_ids = list(self._index.keys())
        dependents_map: dict[str, list[str]] = {eid: [] for eid in all_ids}
        
        for eid in all_ids:
            eku = self.load_eku(eid)
            if eku:
                # eku depends on its 'dependencies'
                for foundation_id in eku.dependencies:
                    if foundation_id in dependents_map:
                        dependents_map[foundation_id].append(eid)
        
        # 2. Recursive collection
        affected = set()
        
        def collect(current_id: str):
            if current_id in affected:
                return
            affected.add(current_id)
            for dep_id in dependents_map.get(current_id, []):
                collect(dep_id)
                
        collect(eku_id)
        return list(affected)

    def _delete_single_eku(self, eku_id: str) -> None:
        """Internal helper to delete one EKU from all store locations."""
        file_path = self._store_path / f"{eku_id}.json"
        quarantine_path = self._quarantine_path / f"{eku_id}.json"
        
        if file_path.exists():
            with file_lock(str(file_path)):
                file_path.unlink()
        if quarantine_path.exists():
            with file_lock(str(quarantine_path)):
                quarantine_path.unlink()
            
        with file_lock(str(self._index_path)):
            self._index = self._load_index_no_lock()
            if eku_id in self._index:
                del self._index[eku_id]
                self._save_index_no_lock()
            
        logger.warning(f"⏪ Rolled back EKU {eku_id}")

    # ── Index management ─────────────────────────────────────────

    def _load_index(self) -> dict:
        """Thread-safe index load."""
        with file_lock(str(self._index_path)):
            return self._load_index_no_lock()

    def _load_index_no_lock(self) -> dict:
        """Internal load without locking (caller must lock)."""
        if self._index_path.exists():
            with open(self._index_path) as f:
                return json.load(f)
        return {}

    def _save_index(self) -> None:
        """Thread-safe index save."""
        with file_lock(str(self._index_path)):
            self._save_index_no_lock()

    def _save_index_no_lock(self) -> None:
        """Internal save without locking (caller must lock)."""
        # Raw atomic write without lock (caller holds it)
        import tempfile
        dir_path = self._index_path.parent
        with tempfile.NamedTemporaryFile("w", dir=dir_path, delete=False) as tf:
            json.dump(self._index, tf, indent=2)
            temp_name = tf.name
        os.replace(temp_name, self._index_path)


# ── Singleton ────────────────────────────────────────────────────
_eku_store: EKUStore | None = None


def get_eku_store() -> EKUStore:
    global _eku_store
    if _eku_store is None:
        _eku_store = EKUStore()
    return _eku_store
