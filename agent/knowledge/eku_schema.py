"""Executable Knowledge Unit (EKU) schema — the agent's permanent memory format.

No raw text. Every field is structured, queryable, and executable.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class CodeTemplate:
    """Minimal working code example."""
    description: str
    code: str
    language: str = "python"
    verified: bool = False


@dataclass
class Transformation:
    """Decision logic — WHEN/WHY/WHEN-NOT."""
    action: str
    when: str
    why: str
    when_not: str
    alternative: str = ""
    trade_offs: dict[str, float] = field(default_factory=dict)


@dataclass
class FailureKnowledgeUnit:
    """Structured failure lesson."""
    failure_type: str          # TypeError, LogicError, RuntimeError, EdgeCase
    root_cause: str
    fix_applied: str
    prevention_rule: str
    severity: str = "warning"  # critical, warning, info
    reproducible: bool = True
    context_tags: list[str] = field(default_factory=list)


@dataclass
class EdgeCase:
    """Known edge case with expected behavior."""
    scenario: str
    behavior: str
    handling: str


@dataclass
class Divergence:
    """Record of when knowledge worked in one context but failed in another."""
    context: str
    expected: str
    actual: str
    unstable_assumption: str


@dataclass
class TestResult:
    """Result of a single test execution."""
    description: str
    code: str
    category: str              # normal, edge, extreme
    passed: bool
    output: str = ""
    error: str = ""
    execution_time_ms: float = 0.0
    context: str = ""


@dataclass
class ExecutableKnowledgeUnit:
    """THE fundamental unit of agent memory.

    Every piece of knowledge the agent stores must be in this format.
    No raw text. No vague descriptions. Structured, queryable, executable.
    """

    # Identity
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    concept: str = ""
    domain: str = ""
    topic: str = ""

    # 1. WHAT it is
    definition: str = ""
    invariants: list[str] = field(default_factory=list)
    constraints: list[str] = field(default_factory=list)

    # 2. HOW to use it
    transformations: list[Transformation] = field(default_factory=list)
    execution_templates: list[CodeTemplate] = field(default_factory=list)

    # 3. WHAT breaks
    failure_memory: list[FailureKnowledgeUnit] = field(default_factory=list)
    edge_cases: list[EdgeCase] = field(default_factory=list)
    divergences: list[Divergence] = field(default_factory=list)

    # 4. TEST history
    test_results: list[TestResult] = field(default_factory=list)

    # 5. META
    confidence: float = 0.0
    verification_status: str = "unverified"  # unverified|proven|quarantined|unstable|illusion_detected
    quarantine_reason: list[str] = field(default_factory=list)
    last_tested: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    version: int = 1

    # 6. DEPENDENCIES
    dependencies: list[str] = field(default_factory=list)  # EKU IDs this depends on
    prerequisites: list[str] = field(default_factory=list)  # Topic names needed first

    # 7. CROSS-LANGUAGE generalization
    language_mappings: dict[str, CodeTemplate] = field(default_factory=dict)

    # ── Computed properties ──────────────────────────────────────

    @property
    def test_pass_rate(self) -> float:
        if not self.test_results:
            return 0.0
        passed = sum(1 for t in self.test_results if t.passed)
        return passed / len(self.test_results)

    @property
    def unique_test_contexts(self) -> int:
        return len(set(t.context for t in self.test_results if t.context))

    @property
    def is_proven(self) -> bool:
        return self.verification_status == "proven"

    @property
    def is_quarantined(self) -> bool:
        return self.verification_status == "quarantined"

    # ── Mutation helpers ─────────────────────────────────────────

    def add_failure(self, fku: FailureKnowledgeUnit) -> None:
        self.failure_memory.append(fku)
        # Each unresolved failure reduces confidence
        if fku.severity == "critical":
            self.confidence = max(0.0, self.confidence - 0.15)
        elif fku.severity == "warning":
            self.confidence = max(0.0, self.confidence - 0.05)

    def add_test_result(self, result: TestResult) -> None:
        self.test_results.append(result)
        self.last_tested = datetime.now(timezone.utc)
        # Recalculate confidence from test pass rate
        self._recalculate_confidence()

    def mark_unstable(self, assumption: str, context: str) -> None:
        self.divergences.append(Divergence(
            context=context,
            expected="(see assumption)",
            actual="(divergence detected)",
            unstable_assumption=assumption,
        ))
        if self.verification_status == "proven":
            self.verification_status = "unstable"
        self.confidence = max(0.0, self.confidence - 0.1)

    def add_constraint(self, constraint: str) -> None:
        if constraint not in self.constraints:
            self.constraints.append(constraint)

    def _recalculate_confidence(self) -> None:
        """Recompute confidence from test results and failure history."""
        if not self.test_results:
            return

        base = self.test_pass_rate

        # Penalize for unresolved critical failures
        critical_count = sum(
            1 for f in self.failure_memory if f.severity == "critical"
        )
        base -= critical_count * 0.05

        # Bonus for diverse passing contexts
        if self.unique_test_contexts >= 4:
            base += 0.05

        self.confidence = max(0.0, min(1.0, base))

    # ── Serialization ────────────────────────────────────────────

    def to_dict(self) -> dict[str, Any]:
        """Serialize to JSON-safe dict."""
        return {
            "id": self.id,
            "concept": self.concept,
            "domain": self.domain,
            "topic": self.topic,
            "definition": self.definition,
            "invariants": self.invariants,
            "constraints": self.constraints,
            "transformations": [
                {
                    "action": t.action, "when": t.when, "why": t.why,
                    "when_not": t.when_not, "alternative": t.alternative,
                    "trade_offs": t.trade_offs,
                }
                for t in self.transformations
            ],
            "execution_templates": [
                {"description": t.description, "code": t.code,
                 "language": t.language, "verified": t.verified}
                for t in self.execution_templates
            ],
            "failure_memory": [
                {
                    "failure_type": f.failure_type, "root_cause": f.root_cause,
                    "fix_applied": f.fix_applied, "prevention_rule": f.prevention_rule,
                    "severity": f.severity, "context_tags": f.context_tags,
                }
                for f in self.failure_memory
            ],
            "edge_cases": [
                {"scenario": e.scenario, "behavior": e.behavior, "handling": e.handling}
                for e in self.edge_cases
            ],
            "confidence": self.confidence,
            "verification_status": self.verification_status,
            "quarantine_reason": self.quarantine_reason,
            "test_pass_rate": self.test_pass_rate,
            "last_tested": self.last_tested.isoformat(),
            "created_at": self.created_at.isoformat(),
            "version": self.version,
            "dependencies": self.dependencies,
            "prerequisites": self.prerequisites,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ExecutableKnowledgeUnit:
        """Deserialize from dict."""
        eku = cls(
            id=data.get("id", str(uuid.uuid4())),
            concept=data.get("concept", ""),
            domain=data.get("domain", ""),
            topic=data.get("topic", ""),
            definition=data.get("definition", ""),
            invariants=data.get("invariants", []),
            constraints=data.get("constraints", []),
            confidence=data.get("confidence", 0.0),
            verification_status=data.get("verification_status", "unverified"),
            quarantine_reason=data.get("quarantine_reason", []),
            version=data.get("version", 1),
            dependencies=data.get("dependencies", []),
            prerequisites=data.get("prerequisites", []),
        )

        for t in data.get("transformations", []):
            eku.transformations.append(Transformation(**t))

        for t in data.get("execution_templates", []):
            eku.execution_templates.append(CodeTemplate(**t))

        for f in data.get("failure_memory", []):
            eku.failure_memory.append(FailureKnowledgeUnit(**f))

        for e in data.get("edge_cases", []):
            eku.edge_cases.append(EdgeCase(**e))

        if "last_tested" in data:
            eku.last_tested = datetime.fromisoformat(data["last_tested"])
        if "created_at" in data:
            eku.created_at = datetime.fromisoformat(data["created_at"])

        return eku
