"""Self-Verifier — Phase 2.

Challenges the agent's own knowledge BEFORE practice.
Generates counter-questions, finds contradictions, checks logic consistency.
"""

import logging
from dataclasses import dataclass, field
from typing import Any

from agent.llm.helpers import llm_complete_json
from agent.llm.prompts import SELF_VERIFIER_CHALLENGE
from agent.modules.collector import RawKnowledge

logger = logging.getLogger(__name__)


@dataclass
class VerificationResult:
    """Output of self-verification."""
    confidence_score: float = 0.0
    verified_facts: list[str] = field(default_factory=list)
    uncertain_facts: list[str] = field(default_factory=list)
    contradictions: list[dict] = field(default_factory=list)
    gaps: list[str] = field(default_factory=list)
    counter_questions: list[str] = field(default_factory=list)

    # Pass through the raw knowledge for downstream use
    raw: RawKnowledge | None = None


class SelfVerifier:
    """Challenges knowledge before it's used for practice or storage.

    This module separates 'I think I know' from 'I proved I know'.
    """

    async def verify(self, raw: RawKnowledge) -> VerificationResult:
        """Full verification pipeline."""
        import json

        result = VerificationResult(raw=raw)

        # Build knowledge summary for challenge
        knowledge_summary = json.dumps({
            "definitions": raw.definitions,
            "invariants": raw.invariants,
            "constraints": raw.constraints,
            "edge_cases": raw.edge_cases,
            "failure_scenarios": raw.failure_scenarios,
        }, indent=2)

        # Ask LLM to challenge this knowledge
        logger.info("⚔️  Self-verification: challenging knowledge...")
        challenge = await self._challenge(raw.topic, knowledge_summary)

        result.counter_questions = challenge.get("counter_questions", [])
        result.gaps = challenge.get("unaddressed_edge_cases", [])
        result.contradictions = challenge.get("contradictions", [])
        potential_breaks = challenge.get("potential_breaks", [])

        # Score confidence based on challenge results
        confidence = 1.0
        confidence -= len(result.contradictions) * 0.15
        confidence -= len(result.gaps) * 0.05
        confidence -= len(potential_breaks) * 0.10
        result.confidence_score = max(0.0, min(1.0, confidence))

        # Classify facts
        for defn in raw.definitions:
            if result.confidence_score >= 0.6:
                result.verified_facts.append(defn)
            else:
                result.uncertain_facts.append(defn)

        for inv in raw.invariants:
            # Check if any contradiction involves this invariant
            is_contradicted = any(
                inv.lower() in str(c).lower() for c in result.contradictions
            )
            if is_contradicted:
                result.uncertain_facts.append(f"[CONTRADICTED] {inv}")
            else:
                result.verified_facts.append(inv)

        logger.info(f"✅ Verification complete:")
        logger.info(f"   Confidence: {result.confidence_score:.2f}")
        logger.info(f"   Verified facts: {len(result.verified_facts)}")
        logger.info(f"   Uncertain facts: {len(result.uncertain_facts)}")
        logger.info(f"   Contradictions: {len(result.contradictions)}")
        logger.info(f"   Knowledge gaps: {len(result.gaps)}")

        return result

    async def _challenge(self, topic: str, knowledge: str) -> dict:
        prompt = SELF_VERIFIER_CHALLENGE.format(
            topic=topic, knowledge=knowledge
        )
        return await llm_complete_json(prompt)
