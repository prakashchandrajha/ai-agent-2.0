"""Knowledge Collector — Phase 1.

Multi-source knowledge collection with entropy filtering.
Uses web search and extraction to gather raw knowledge.
"""

import logging
from dataclasses import dataclass, field

from agent.llm.helpers import llm_complete_json
from agent.llm.prompts import KNOWLEDGE_EXTRACTOR
from agent.modules.pre_validator import LearningContract

logger = logging.getLogger(__name__)


@dataclass
class RawKnowledge:
    """Raw extracted knowledge before verification."""
    topic: str = ""
    domain: str = ""
    definitions: list[str] = field(default_factory=list)
    invariants: list[str] = field(default_factory=list)
    constraints: list[str] = field(default_factory=list)
    edge_cases: list[str] = field(default_factory=list)
    failure_scenarios: list[str] = field(default_factory=list)
    code_patterns: list[dict] = field(default_factory=list)
    source_count: int = 0


class KnowledgeCollector:
    """Collects knowledge from multiple sources with entropy filtering.

    Uses Scrapling for web fetching when available, falls back to
    LLM's internal knowledge.
    """

    async def collect(self, contract: LearningContract) -> RawKnowledge:
        """Collect and extract knowledge for the given contract.

        Pipeline:
        1. Generate comprehensive knowledge using LLM
        2. For each subtopic, extract structured primitives
        3. Apply entropy filter to deduplicate
        """
        raw = RawKnowledge(
            topic=contract.topic,
            domain=contract.resolved_domain,
        )

        # Collect knowledge for main topic + each subtopic
        topics_to_collect = [contract.topic] + contract.core_subtopics[:5]

        for subtopic in topics_to_collect:
            logger.info(f"📚 Collecting knowledge: {subtopic}")
            extracted = await self._extract_from_llm(
                contract.resolved_domain, subtopic
            )
            self._merge_knowledge(raw, extracted)
            raw.source_count += 1

        # Apply entropy filter
        raw = self._entropy_filter(raw)

        logger.info(
            f"✅ Collected: {len(raw.definitions)} definitions, "
            f"{len(raw.invariants)} invariants, "
            f"{len(raw.edge_cases)} edge cases, "
            f"{len(raw.code_patterns)} code patterns"
        )
        return raw

    async def collect_from_web(self, contract: LearningContract) -> RawKnowledge:
        """Collect from web sources using Scrapling.

        NOTE: This is the advanced pipeline — requires Scrapling installed
        with fetchers. Falls back to LLM-only if unavailable.
        """
        try:
            from scrapling.fetchers import Fetcher
            # Future: implement web-based collection
            logger.info("🌐 Web collection available but delegating to LLM for now")
        except ImportError:
            logger.info("📝 Scrapling not available, using LLM knowledge only")

        return await self.collect(contract)

    async def _extract_from_llm(self, domain: str, topic: str) -> dict:
        """Use LLM to extract structured knowledge about a topic."""
        prompt = KNOWLEDGE_EXTRACTOR.format(
            topic=topic,
            domain=domain,
            content=f"Provide comprehensive knowledge about {topic} in {domain}. "
                    f"Include definitions, rules, constraints, edge cases, common "
                    f"mistakes, and minimal working code examples.",
        )
        return await llm_complete_json(prompt)

    def _merge_knowledge(self, raw: RawKnowledge, extracted: dict) -> None:
        """Merge extracted data into raw knowledge, avoiding exact duplicates."""
        for key in ["definitions", "invariants", "constraints", "edge_cases",
                     "failure_scenarios"]:
            existing = getattr(raw, key)
            for item in extracted.get(key, []):
                if item and item not in existing:
                    existing.append(item)

        for pattern in extracted.get("code_patterns", []):
            if pattern and pattern not in raw.code_patterns:
                raw.code_patterns.append(pattern)

    def _entropy_filter(self, raw: RawKnowledge) -> RawKnowledge:
        """Remove semantically duplicate information.

        Uses simple string similarity for now. Future: use embeddings
        from LocalMind's Embedder for cosine similarity dedup.

        Threshold: items > 80% similar → remove the shorter one.
        """
        raw.definitions = self._dedup_list(raw.definitions)
        raw.invariants = self._dedup_list(raw.invariants)
        raw.constraints = self._dedup_list(raw.constraints)
        raw.edge_cases = self._dedup_list(raw.edge_cases)
        raw.failure_scenarios = self._dedup_list(raw.failure_scenarios)
        return raw

    def _dedup_list(self, items: list[str]) -> list[str]:
        """Remove near-duplicate strings from a list."""
        if len(items) <= 1:
            return items

        unique = [items[0]]
        for item in items[1:]:
            is_dup = False
            for existing in unique:
                similarity = self._simple_similarity(item.lower(), existing.lower())
                if similarity > 0.8:
                    is_dup = True
                    # Keep the longer (more detailed) version
                    if len(item) > len(existing):
                        unique[unique.index(existing)] = item
                    break
            if not is_dup:
                unique.append(item)
        return unique

    @staticmethod
    def _simple_similarity(a: str, b: str) -> float:
        """Simple word-overlap similarity (Jaccard index)."""
        words_a = set(a.split())
        words_b = set(b.split())
        if not words_a or not words_b:
            return 0.0
        intersection = words_a & words_b
        union = words_a | words_b
        return len(intersection) / len(union)
