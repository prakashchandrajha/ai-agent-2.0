"""Failure Analyzer — Phase 4.

Every failure is a lesson. Converts raw failures into structured
FailureKnowledgeUnits — the agent's experience memory.
"""

import logging

from agent.knowledge.eku_schema import FailureKnowledgeUnit, TestResult
from agent.llm.helpers import llm_complete_json
from agent.llm.prompts import FAILURE_ANALYZER
from agent.modules.executor import ExecutionResults

logger = logging.getLogger(__name__)


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
