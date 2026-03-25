"""Pre-Learning Validator — Phase 0.

THE MOST CRITICAL MODULE.
Without this → agent learns the wrong thing deeply → worse than not learning.

Responsibilities:
1. Disambiguate topic (e.g., "variable" in math vs programming)
2. Define scope (depth, boundaries, prerequisites)
3. Define mastery criteria (explain, implement, debug)
"""

import logging
from dataclasses import dataclass, field

from agent.llm.helpers import llm_complete_json
from agent.llm.prompts import (
    PRE_VALIDATOR_DISAMBIGUATE,
    PRE_VALIDATOR_MASTERY,
    PRE_VALIDATOR_SCOPE,
)

logger = logging.getLogger(__name__)


@dataclass
class LearningContract:
    """The output of pre-validation — defines EXACTLY what will be learned."""
    subject: str
    topic: str
    resolved_domain: str = ""
    resolved_meaning: str = ""
    depth_level: str = "intermediate"
    core_subtopics: list[str] = field(default_factory=list)
    boundaries: list[str] = field(default_factory=list)
    prerequisites: list[str] = field(default_factory=list)
    mastery_explain: list[str] = field(default_factory=list)
    mastery_implement: list[str] = field(default_factory=list)
    mastery_debug: list[str] = field(default_factory=list)
    mastery_tests: list[str] = field(default_factory=list)
    estimated_complexity: int = 5
    is_valid: bool = True
    abort_reason: str = ""


class PreLearningValidator:
    """Validates and scopes learning BEFORE any knowledge collection begins."""

    async def validate(self, subject: str, topic: str) -> LearningContract:
        """Full pre-validation pipeline.

        Returns a LearningContract that precisely defines what to learn.
        """
        contract = LearningContract(subject=subject, topic=topic)

        # Step 1: Disambiguate
        logger.info(f"🔍 Disambiguating: {subject}/{topic}")
        disambiguation = await self._disambiguate(subject, topic)
        contract.resolved_domain = disambiguation.get("resolved_domain", subject)
        contract.resolved_meaning = disambiguation.get("resolved_meaning", topic)

        if disambiguation.get("is_ambiguous"):
            meanings = disambiguation.get("possible_meanings", [])
            logger.info(f"  ⚠️  Ambiguous topic detected: {len(meanings)} possible meanings")
            logger.info(f"  ✅ Resolved to: {contract.resolved_meaning}")

        # Step 2: Scope Control
        logger.info(f"📐 Defining scope for: {contract.resolved_meaning}")
        scope = await self._define_scope(
            subject, topic, contract.resolved_domain, contract.resolved_meaning
        )
        contract.depth_level = scope.get("depth_level", "intermediate")
        contract.core_subtopics = scope.get("core_subtopics", [])
        contract.boundaries = scope.get("boundaries", [])
        contract.prerequisites = scope.get("prerequisites", [])
        contract.estimated_complexity = scope.get("estimated_complexity", 5)

        # Step 3: Mastery Definition
        logger.info(f"🎯 Defining mastery criteria")
        mastery = await self._define_mastery(subject, topic, scope)
        contract.mastery_explain = mastery.get("can_explain", [])
        contract.mastery_implement = mastery.get("can_implement", [])
        contract.mastery_debug = mastery.get("can_debug", [])
        contract.mastery_tests = mastery.get("mastery_test_cases", [])

        logger.info(f"✅ Learning contract ready:")
        logger.info(f"   Domain: {contract.resolved_domain}")
        logger.info(f"   Depth: {contract.depth_level}")
        logger.info(f"   Subtopics: {len(contract.core_subtopics)}")
        logger.info(f"   Prerequisites: {contract.prerequisites}")
        logger.info(f"   Complexity: {contract.estimated_complexity}/10")

        return contract

    async def _disambiguate(self, subject: str, topic: str) -> dict:
        prompt = PRE_VALIDATOR_DISAMBIGUATE.format(subject=subject, topic=topic)
        return await llm_complete_json(prompt)

    async def _define_scope(
        self, subject: str, topic: str, domain: str, meaning: str
    ) -> dict:
        prompt = PRE_VALIDATOR_SCOPE.format(
            subject=subject, topic=topic, domain=domain, meaning=meaning
        )
        return await llm_complete_json(prompt)

    async def _define_mastery(self, subject: str, topic: str, scope: dict) -> dict:
        import json
        prompt = PRE_VALIDATOR_MASTERY.format(
            subject=subject, topic=topic, scope=json.dumps(scope, indent=2)
        )
        return await llm_complete_json(prompt)
