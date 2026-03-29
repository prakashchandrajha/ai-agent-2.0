"""Execution-Based Learner — Phase 3.

Theory means NOTHING until code runs, passes, and handles edge cases.
Generates test cases, runs them in sandbox, captures everything.
"""

import logging
from dataclasses import dataclass, field

from agent.knowledge.eku_schema import TestResult
from agent.llm.helpers import llm_complete_json
from agent.llm.prompts import CODE_GENERATOR_PROMPT, ASSERTION_GENERATOR_PROMPT
from agent.modules.code_validator import validate_code
from agent.modules.verifier import VerificationResult
from agent.sandbox.runner import SandboxResult, get_sandbox

logger = logging.getLogger(__name__)

# ── MASTER_PLAN Task 1.NEW-C: Test Category Balancing ──────────────────────

TEST_REQUIREMENTS: dict[str, dict[str, int]] = {
    "normal":  {"min": 3, "max": 4},   # Happy-path — deterministic
    "edge":    {"min": 3, "max": 4},   # Boundary / None / empty
    "extreme": {"min": 2, "max": 3},   # Adversarial / wrong types / huge input
}

CATEGORY_TEMPERATURES: dict[str, float] = {
    "normal":  0.0,   # Same happy path every time
    "edge":    0.3,   # Some variation — find different edges
    "extreme": 0.5,   # High variation — creativity needed
}


def generate_balanced_tests(
    concept: str,
    tests_by_category: dict[str, list],
    session_logger=None,
) -> list:
    """Validate and flatten per-category tests, enforcing min/max.

    Args:
        concept: The concept being tested (for log messages).
        tests_by_category: Dict mapping category → list of test dicts,
            as returned by the LLM test-generation prompt.
        session_logger: Optional SessionLogger — receives a warning event
            when a category has fewer tests than its minimum.

    Returns:
        Flat list of test dicts, each annotated with 'category'.
    """
    balanced: list = []

    for category, reqs in TEST_REQUIREMENTS.items():
        category_tests = tests_by_category.get(category, [])

        # Warn when below minimum — do NOT crash; some concepts have few edge cases
        if len(category_tests) < reqs["min"]:
            msg = (
                f"Insufficient {category} test coverage for '{concept}': "
                f"generated {len(category_tests)}, needed {reqs['min']}"
            )
            logger.warning("    ⚠️  %s", msg)
            if session_logger:
                try:
                    session_logger.log(
                        "execution",
                        "insufficient_test_coverage",
                        {
                            "category": category,
                            "generated": len(category_tests),
                            "needed": reqs["min"],
                            "concept": concept,
                        },
                    )
                except Exception:
                    pass

        # Cap at maximum
        for test in category_tests[: reqs["max"]]:
            test["category"] = category  # Ensure category tag is present
            balanced.append(test)

    return balanced



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


def verify_assertion_uses_actual_output(assertions: str, actual_output: str) -> bool:
    """Verify assertions reference the real output not a contradicting value."""
    import ast
    try:
        tree = ast.parse(assertions)
        for node in ast.walk(tree):
            if isinstance(node, ast.Compare):
                items = [node.left] + node.comparators
                for item in items:
                    if isinstance(item, (ast.Constant, ast.List, ast.Tuple, ast.Dict, ast.Set)):
                        if isinstance(item, ast.Constant):
                            if item.value is None or isinstance(item.value, bool):
                                continue
                            val_str = str(item.value)
                        else:
                            val_str = ast.unparse(item)
                            
                        clean_val = "".join(val_str.split())
                        clean_out = "".join(actual_output.split())
                        
                        if len(clean_val) > 1 and clean_val not in clean_out:
                            return False
    except Exception:
        # Unparseable assertions contradict reality by being broken
        return False
    return True


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

                # Pre-execution code validation (Task 0.4)
                validation = validate_code(code)
                if not validation.is_safe:
                    logger.warning(f"    🛡️ CODE BLOCKED: {description} — {validation.violations}")
                    test_result = TestResult(
                        description=description,
                        code=code,
                        category=category,
                        passed=False,
                        error=f"Code validation failed: {validation.violations}",
                        context=f"{category}:{description}",
                    )
                    results.failed.append(test_result)
                    continue

                # Run in sandbox (Call 1)
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
                    logger.warning(f"    ⏰ TIMEOUT (Code Gen): {description}")
                    continue
                elif sandbox_result.return_code != 0:
                    results.crashes.append(test_result)
                    logger.warning(f"    💥 CRASH (Code Gen): {description}")
                    continue

                # Call 2: Generate assertions from real output
                combined_output = sandbox_result.stdout + "\n" + sandbox_result.stderr
                max_retries = 3
                assertions_valid = False
                assertions_code = ""

                for attempt in range(max_retries):
                    assertions_code = await self._generate_assertions(raw.topic, description, code, combined_output)
                    if verify_assertion_uses_actual_output(assertions_code, combined_output):
                        assertions_valid = True
                        break
                    logger.warning(f"    ⚠️ Invalid assertions generated (contradicts output), regenerating... ({attempt+1}/{max_retries})")

                if not assertions_valid:
                    logger.warning(f"    ❌ Failed to generate valid assertions after {max_retries} attempts.")
                    results.failed.append(test_result)
                    continue
                
                # Append assertions to code and run again
                full_code = code + "\n\n" + assertions_code
                test_result.code = full_code
                
                sandbox_result_2 = await self.sandbox.run(full_code, language)
                test_result.execution_time_ms += sandbox_result_2.execution_time_ms
                results.total_execution_time_ms += sandbox_result_2.execution_time_ms
                
                test_result.passed = sandbox_result_2.passed
                test_result.output = sandbox_result_2.stdout[:500]
                test_result.error = sandbox_result_2.stderr[:500]

                if sandbox_result_2.timed_out:
                    test_result.passed = False
                    test_result.error = "TIMEOUT"
                    results.crashes.append(test_result)
                    logger.warning(f"    ⏰ TIMEOUT (With Assertions): {description}")
                elif sandbox_result_2.passed:
                    results.passed.append(test_result)
                    logger.info(f"    ✅ PASS: {description}")
                elif sandbox_result_2.return_code != 0:
                    results.crashes.append(test_result)
                    logger.warning(f"    💥 CRASH (With Assertions): {description}")
                else:
                    results.failed.append(test_result)
                    logger.warning(f"    ❌ FAIL (With Assertions): {description}")

        logger.info(
            f"🧪 Execution complete: "
            f"{len(results.passed)} passed, "
            f"{len(results.failed)} failed, "
            f"{len(results.crashes)} crashed "
            f"({results.total_execution_time_ms:.0f}ms total)"
        )

        return results

# ── MASTER_PLAN Task 1.8: Temperature Stratification (build_test_gen_prompt) ─────

def build_test_gen_prompt(
    concept: str,
    category: str,
    knowledge: str,
    already_tested: list[str] | None = None,
) -> str:
    """Build a per-category test generation prompt.

    On iteration 2+, injects an 'avoid' section so the LLM explores
    untested territory instead of repeating the same happy-path tests.

    Args:
        concept:         The topic/concept under test.
        category:        'normal', 'edge', or 'extreme'.
        knowledge:       JSON-serialised knowledge summary.
        already_tested:  List of test descriptions from previous iterations.

    Returns:
        Full prompt string to send to the LLM.
    """
    from agent.llm.prompts import CODE_GENERATOR_PROMPT  # lazy import avoids cycles

    avoid_section = ""
    if already_tested:
        avoid_lines = "\n".join(f"- {t}" for t in already_tested)
        avoid_section = (
            f"\n\nDo NOT generate tests similar to:\n{avoid_lines}\n"
            "Focus on untested scenarios and edge cases not yet covered."
        )

    base = CODE_GENERATOR_PROMPT.format(
        topic=concept,
        domain="",          # filled by caller when available
        language="python",  # overridden by caller
        knowledge=knowledge,
    )
    return base + avoid_section


    async def _generate_tests(
        self,
        topic: str,
        domain: str,
        language: str,
        knowledge: str,
        already_tested: list[str] | None = None,
    ) -> dict:
        """Generate per-category test cases.

        On iteration 2+ (already_tested is non-empty), injects an avoid
        section via build_test_gen_prompt() so the model explores new ground.
        """
        if already_tested:
            prompt = build_test_gen_prompt(
                concept=topic,
                category="all",
                knowledge=knowledge,
                already_tested=already_tested,
            )
        else:
            prompt = CODE_GENERATOR_PROMPT.format(
                topic=topic, domain=domain, language=language, knowledge=knowledge
            )
        return await llm_complete_json(prompt)

    async def _generate_assertions(
        self, topic: str, description: str, code: str, output: str
    ) -> str:
        prompt = ASSERTION_GENERATOR_PROMPT.format(
            topic=topic, description=description, code=code, output=output
        )
        from agent.llm.client import get_llm_client
        client = get_llm_client()
        return await client.generate(prompt=prompt, temperature=0.0, json_mode=False)
