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
class ExecutionTrace:
    code: str
    actual_output: str
    elapsed_ms: float
    test_category: str       # "normal", "edge", "extreme"
    passed: bool
    robustness_score: float


@dataclass
class Constraint:
    rule: str
    is_hard: bool            # True=hard, False=soft
    source: str              # "failure_inversion", "test_implication", "documentation"
    confidence: float
    violation_count: int = 0


@dataclass
class GateDiagnostic:
    gate_name: str
    failure_reason: str
    actual_value: float
    required_value: float
    suggested_fix: str
    is_retryable: bool


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
    _schema_version: str = "2.0.0"

    # 6. DEPENDENCIES
    dependencies: list[str] = field(default_factory=list)  # EKU IDs this depends on
    parent_ekus: list[str] = field(default_factory=list)   # EKU IDs that depend on this
    prerequisites: list[str] = field(default_factory=list)  # Topic names needed first

    # 7. CONFIDENCE & CONSTRAINTS
    confidence_breakdown: dict = field(default_factory=dict)
    hard_constraints: list[str] = field(default_factory=list)
    soft_constraints: list[str] = field(default_factory=list)
    violated_constraints_log: list[str] = field(default_factory=list)

    # 8. EXECUTION TRACES
    canonical_traces: list[ExecutionTrace] = field(default_factory=list)
    trace_patterns: list[str] = field(default_factory=list)

    # 9. PREDICTION TRACKING
    prediction_accuracy: float = 0.0
    prediction_history: list[dict] = field(default_factory=list)
    confusion_gaps: list[str] = field(default_factory=list)

    # 10. TRANSFER & LIFECYCLE
    micro_skills: list[str] = field(default_factory=list)
    last_used_timestamp: str = ""
    usage_count: int = 0
    decay_score: float = 0.0

    # 11. SAFETY & QUALITY
    state_sensitive: bool = False
    context_dependencies: list[str] = field(default_factory=list)
    avg_robustness_score: float = 1.0
    fragility_flags: list[str] = field(default_factory=list)

    # 12. SOURCE & MASTERY
    source_urls: list[str] = field(default_factory=list)
    avg_source_authority: float = 0.0
    mastery_criteria_met: list[str] = field(default_factory=list)
    mastery_criteria_unmet: list[str] = field(default_factory=list)
    gate_diagnostics: list[GateDiagnostic] = field(default_factory=list)

    # 13. VERSIONING & FINGERPRINT
    version_bounds: dict = field(default_factory=dict)
    context_fingerprint: dict = field(default_factory=dict)

    # 14. CROSS-LANGUAGE generalization
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
            "_schema_version": self._schema_version,
            "dependencies": self.dependencies,
            "parent_ekus": self.parent_ekus,
            "prerequisites": self.prerequisites,
            "confidence_breakdown": self.confidence_breakdown,
            "hard_constraints": self.hard_constraints,
            "soft_constraints": self.soft_constraints,
            "violated_constraints_log": self.violated_constraints_log,
            "canonical_traces": [
                {
                    "code": t.code, "actual_output": t.actual_output,
                    "elapsed_ms": t.elapsed_ms, "test_category": t.test_category,
                    "passed": t.passed, "robustness_score": t.robustness_score
                }
                for t in self.canonical_traces
            ],
            "trace_patterns": self.trace_patterns,
            "prediction_accuracy": self.prediction_accuracy,
            "prediction_history": self.prediction_history,
            "confusion_gaps": self.confusion_gaps,
            "micro_skills": self.micro_skills,
            "last_used_timestamp": self.last_used_timestamp,
            "usage_count": self.usage_count,
            "decay_score": self.decay_score,
            "state_sensitive": self.state_sensitive,
            "context_dependencies": self.context_dependencies,
            "avg_robustness_score": self.avg_robustness_score,
            "fragility_flags": self.fragility_flags,
            "source_urls": self.source_urls,
            "avg_source_authority": self.avg_source_authority,
            "mastery_criteria_met": self.mastery_criteria_met,
            "mastery_criteria_unmet": self.mastery_criteria_unmet,
            "gate_diagnostics": [
                {
                    "gate_name": t.gate_name, "failure_reason": t.failure_reason,
                    "actual_value": t.actual_value, "required_value": t.required_value,
                    "suggested_fix": t.suggested_fix, "is_retryable": t.is_retryable
                }
                for t in self.gate_diagnostics
            ],
            "version_bounds": self.version_bounds,
            "context_fingerprint": self.context_fingerprint,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ExecutableKnowledgeUnit:
        """Deserialize from dict."""
        from agent.knowledge.migrations import migrate_eku
        data = migrate_eku(data)
        
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
            _schema_version=data.get("_schema_version", "2.0.0"),
            dependencies=data.get("dependencies", []),
            parent_ekus=data.get("parent_ekus", []),
            prerequisites=data.get("prerequisites", []),
            confidence_breakdown=data.get("confidence_breakdown", {}),
            hard_constraints=data.get("hard_constraints", []),
            soft_constraints=data.get("soft_constraints", []),
            violated_constraints_log=data.get("violated_constraints_log", []),
            trace_patterns=data.get("trace_patterns", []),
            prediction_accuracy=data.get("prediction_accuracy", 0.0),
            prediction_history=data.get("prediction_history", []),
            confusion_gaps=data.get("confusion_gaps", []),
            micro_skills=data.get("micro_skills", []),
            last_used_timestamp=data.get("last_used_timestamp", ""),
            usage_count=data.get("usage_count", 0),
            decay_score=data.get("decay_score", 0.0),
            state_sensitive=data.get("state_sensitive", False),
            context_dependencies=data.get("context_dependencies", []),
            avg_robustness_score=data.get("avg_robustness_score", 1.0),
            fragility_flags=data.get("fragility_flags", []),
            source_urls=data.get("source_urls", []),
            avg_source_authority=data.get("avg_source_authority", 0.0),
            mastery_criteria_met=data.get("mastery_criteria_met", []),
            mastery_criteria_unmet=data.get("mastery_criteria_unmet", []),
            version_bounds=data.get("version_bounds", {}),
            context_fingerprint=data.get("context_fingerprint", {}),
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

        for t in data.get("canonical_traces", []):
            eku.canonical_traces.append(ExecutionTrace(**t))

        for t in data.get("gate_diagnostics", []):
            eku.gate_diagnostics.append(GateDiagnostic(**t))

        return eku
