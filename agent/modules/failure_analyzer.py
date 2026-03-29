"""Failure Analyzer — Phase 4.

Every failure is a lesson. Converts raw failures into structured
FailureKnowledgeUnits — the agent's experience memory.
"""

import logging
import re
from collections import defaultdict

from agent.knowledge.eku_schema import FailureKnowledgeUnit, TestResult
from agent.llm.helpers import llm_complete_json
from agent.llm.prompts import FAILURE_ANALYZER
from agent.modules.executor import ExecutionResults

logger = logging.getLogger(__name__)

# ── MASTER_PLAN 1.NEW-H: Failure Pattern Clustering ───────────────────
FAILURE_PATTERNS: dict[str, str] = {
    "type_error":      r"TypeError:.*(?:NoneType|'int'|'str'|'list'|'dict')",
    "attribute_error": r"AttributeError:.*has no attribute",
    "import_error":    r"ModuleNotFoundError|ImportError",
    "timeout":         r"TimeoutError|timed out",
    "assertion":       r"AssertionError",
    "index_error":     r"IndexError",
    "key_error":       r"KeyError",
    "runtime_error":   r"RuntimeError",
}


def cluster_failures(failures: list) -> dict[str, list]:
    """Group failures by root-cause pattern.

    Args:
        failures: List of failure dicts with an 'error_message' key,
                  or any objects with an .error attribute.

    Returns:
        Dict mapping pattern_name → list of failures.
    """
    clusters: dict[str, list] = defaultdict(list)

    for failure in failures:
        error_msg = (
            failure.get("error_message", "")
            if isinstance(failure, dict)
            else getattr(failure, "error", "") or ""
        )
        matched = False
        for pattern_name, regex in FAILURE_PATTERNS.items():
            if re.search(regex, error_msg, re.IGNORECASE):
                clusters[pattern_name].append(failure)
                matched = True
                break
        if not matched:
            clusters["unknown"].append(failure)

    return dict(clusters)


def get_root_cause_summary(clusters: dict[str, list]) -> str:
    """Human-readable summary of what's failing and why."""
    if not clusters:
        return "No failures recorded."

    dominant_name, dominant_list = max(
        clusters.items(), key=lambda kv: len(kv[1])
    )
    total = sum(len(v) for v in clusters.values())
    return (
        f"Primary failure pattern: {dominant_name} "
        f"({len(dominant_list)}/{total} failures)"
    )


class FailureAnalyzer:
    """Converts raw failures into structured knowledge.

    These FKUs become the MOST VALUABLE knowledge — more than
    textbook definitions. They are the agent's experience memory.
    """

    async def analyze_all(
        self, results: ExecutionResults, topic: str
    ) -> list[FailureKnowledgeUnit]:
        """Analyze all failures and crashes from execution."""
        failures_to_analyze = results.failed + results.crashes
        fkus = []

        for test_result in failures_to_analyze:
            logger.info(f"🔍 Analyzing failure: {test_result.description}")
            fku = await self._analyze_single(test_result, topic)
            if fku:
                fkus.append(fku)

        logger.info(f"🔥 Analyzed {len(fkus)} failures into structured lessons")
        return fkus

    async def _analyze_single(
        self, test_result: TestResult, topic: str
    ) -> FailureKnowledgeUnit | None:
        """Analyze a single failure."""
        try:
            analysis = await llm_complete_json(
                FAILURE_ANALYZER.format(
                    code=test_result.code,
                    error=test_result.error or test_result.output,
                    topic=topic,
                )
            )

            if not analysis:
                return None

            return FailureKnowledgeUnit(
                failure_type=analysis.get("failure_type", "Unknown"),
                root_cause=analysis.get("root_cause", "Analysis failed"),
                fix_applied=analysis.get("fix", ""),
                prevention_rule=analysis.get("prevention_rule", ""),
                severity=analysis.get("severity", "warning"),
                context_tags=[topic, test_result.category],
            )
        except Exception as e:
            logger.error(f"Failure analysis error: {e}")
            return None
