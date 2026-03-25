"""Execution-Based Learner — Phase 3.

Theory means NOTHING until code runs, passes, and handles edge cases.
Generates test cases, runs them in sandbox, captures everything.
"""

import logging
from dataclasses import dataclass, field

from agent.knowledge.eku_schema import TestResult
from agent.llm.helpers import llm_complete_json
from agent.llm.prompts import TEST_GENERATOR
from agent.modules.verifier import VerificationResult
from agent.sandbox.runner import SandboxResult, get_sandbox

logger = logging.getLogger(__name__)


@dataclass
class ExecutionResults:
    """Results of execution-based learning."""
    passed: list[TestResult] = field(default_factory=list)
    failed: list[TestResult] = field(default_factory=list)
    crashes: list[TestResult] = field(default_factory=list)
    total_execution_time_ms: float = 0.0

    @property
    def pass_rate(self) -> float:
        total = len(self.passed) + len(self.failed) + len(self.crashes)
        return len(self.passed) / total if total else 0.0

    @property
    def all_results(self) -> list[TestResult]:
        return self.passed + self.failed + self.crashes


class ExecutionLearner:
    """Learns by generating and running test cases.

    The autoresearch pattern applied to learning:
    Run → evaluate → keep/discard knowledge that produced the test.
    """

    def __init__(self):
        self.sandbox = get_sandbox()

    async def learn_by_doing(
        self,
        verified: VerificationResult,
        language: str = "python",
    ) -> ExecutionResults:
        """Generate tests and run them in sandbox."""
        import json

        raw = verified.raw
        if not raw:
            return ExecutionResults()

        results = ExecutionResults()

        # Generate test cases
        logger.info("🧪 Generating test cases...")
        knowledge_summary = json.dumps({
            "definitions": raw.definitions,
            "invariants": raw.invariants,
            "code_patterns": raw.code_patterns,
            "edge_cases": raw.edge_cases,
        }, indent=2)

        tests = await self._generate_tests(
            raw.topic, raw.domain, language, knowledge_summary
        )

        # Run each category
        for category in ["normal", "edge", "extreme"]:
            test_cases = tests.get(category, [])
            logger.info(f"  ▶ Running {len(test_cases)} {category} tests...")

            for test in test_cases:
                description = test.get("description", "unnamed test")
                code = test.get("code", "")
                expected = test.get("expected_behavior", "")

                if not code:
                    continue

                # Run in sandbox
                sandbox_result = await self.sandbox.run(code, language)

                # Classify result
                test_result = TestResult(
                    description=description,
                    code=code,
                    category=category,
                    passed=sandbox_result.passed,
                    output=sandbox_result.stdout[:500],
                    error=sandbox_result.stderr[:500],
                    execution_time_ms=sandbox_result.execution_time_ms,
                    context=f"{category}:{description}",
                )

                results.total_execution_time_ms += sandbox_result.execution_time_ms

                if sandbox_result.timed_out:
                    test_result.passed = False
                    test_result.error = "TIMEOUT"
                    results.crashes.append(test_result)
                    logger.warning(f"    ⏰ TIMEOUT: {description}")
                elif sandbox_result.passed:
                    results.passed.append(test_result)
                    logger.info(f"    ✅ PASS: {description}")
                elif sandbox_result.return_code != 0:
                    results.crashes.append(test_result)
                    logger.warning(f"    💥 CRASH: {description}")
                else:
                    results.failed.append(test_result)
                    logger.warning(f"    ❌ FAIL: {description}")

        logger.info(
            f"🧪 Execution complete: "
            f"{len(results.passed)} passed, "
            f"{len(results.failed)} failed, "
            f"{len(results.crashes)} crashed "
            f"({results.total_execution_time_ms:.0f}ms total)"
        )

        return results

    async def _generate_tests(
        self, topic: str, domain: str, language: str, knowledge: str
    ) -> dict:
        prompt = TEST_GENERATOR.format(
            topic=topic, domain=domain, language=language, knowledge=knowledge
        )
        return await llm_complete_json(prompt)
