"""Constraint Extractor — MASTER_PLAN Task 1.9.

Three sources of hard constraints:
  1. Failure inversion — every failure implies a constraint
  2. Passing test confirmation — passing test confirms expected behaviour
  3. Documentation parsing — explicit rule extraction via regex
"""

import logging
import re

logger = logging.getLogger(__name__)


class ConstraintExtractor:
    """Extract hard constraints from failures, passing tests, and documentation.

    Constraints are wired into ``eku.hard_constraints`` during the
    collection phase so the EKU stores what cannot be violated.
    """

    async def extract_from_failure(self, failure) -> list[str]:
        """Failure inversion: every failure implies a constraint.

        Args:
            failure: A TestResult object or dict with 'error' / 'error_message'.

        Returns:
            List of 'X must Y' constraint strings.
        """
        error_msg = (
            failure.get("error_message", "")
            if isinstance(failure, dict)
            else getattr(failure, "error", "") or ""
        )

        constraints: list[str] = []

        if "TypeError" in error_msg:
            # Try LLM inversion — lazy import to avoid circular deps
            try:
                from agent.llm.client import get_llm_client
                client = get_llm_client()
                prompt = (
                    f"This failure: '{error_msg[:200]}' implies what constraint? "
                    "Reply with ONE 'X must Y' rule. Be concise."
                )
                result = await client.generate(prompt=prompt, temperature=0.0, json_mode=False)
                constraint = result.strip()
                if constraint and len(constraint) < 200:
                    constraints.append(constraint)
            except Exception as exc:
                logger.debug("LLM constraint extraction failed: %s", exc)

        if "IndexError" in error_msg:
            constraints.append("Must check list is non-empty before indexing")

        if "KeyError" in error_msg:
            constraints.append("Must verify key exists in dict before accessing")

        if "AttributeError" in error_msg:
            constraints.append("Must check attribute exists before accessing")

        return constraints

    async def extract_from_passing_test(
        self, code: str, actual_output: str
    ) -> list[str]:
        """Passing test confirms expected behaviour — extract the implied rule.

        Args:
            code: The code that was run successfully.
            actual_output: The stdout from the sandbox run.

        Returns:
            List of constraint strings (usually one).
        """
        if not code.strip() or not actual_output.strip():
            return []

        try:
            from agent.llm.client import get_llm_client
            client = get_llm_client()
            prompt = (
                f"Code:\n{code[:400]}\n\n"
                f"Output: {actual_output[:200]}\n\n"
                "What behaviour rule does this passing test confirm? "
                "Reply with ONE constraint in the form 'X always Y' or 'X returns Y'."
            )
            result = await client.generate(prompt=prompt, temperature=0.0, json_mode=False)
            constraint = result.strip()
            if constraint and len(constraint) < 200:
                return [constraint]
        except Exception as exc:
            logger.debug("LLM passing-test extraction failed: %s", exc)

        return []

    def extract_from_documentation(self, doc_text: str) -> list[str]:
        """Parse explicit rules from documentation via regex.

        Args:
            doc_text: Raw documentation or scraped page text.

        Returns:
            Up to 10 constraint strings found in the text.
        """
        patterns = [
            r"must\s+\w+[^.]+\.",
            r"always\s+\w+[^.]+\.",
            r"never\s+\w+[^.]+\.",
            r"raises\s+\w+Error[^.]+\.",
            r"returns\s+None[^.]*\.",
        ]
        constraints: list[str] = []
        for pattern in patterns:
            matches = re.findall(pattern, doc_text, re.IGNORECASE)
            constraints.extend(m.strip() for m in matches if len(m.strip()) < 200)

        return constraints[:10]  # Max 10 per document to prevent noise
