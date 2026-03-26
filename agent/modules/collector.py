"""Knowledge Collector — Phase 1.

Multi-source knowledge collection with entropy filtering.
Uses web search and extraction to gather raw knowledge,
and semantic embeddings to deduplicate it.
"""

import asyncio
import logging
from dataclasses import dataclass, field

import numpy as np

from agent.config import get_settings
from agent.llm.helpers import llm_complete_json
from agent.llm.prompts import KNOWLEDGE_EXTRACTOR, KNOWLEDGE_VERIFIER
from agent.modules.pre_validator import LearningContract
from agent.services.embedder import get_embedder
from agent.services.web_scraper import scrape_page
from agent.services.web_search import search_web

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
    """Collects knowledge from multiple sources with entropy filtering."""

    def __init__(self):
        self.settings = get_settings()

    async def collect(self, contract: LearningContract) -> RawKnowledge:
        """Collect and extract knowledge for the given contract.

        Pipeline:
        1. Search web for the topic -> URLs
        2. Fetch page content
        3. Extract structured primitives using LLM
        4. Apply semantic entropy filter to deduplicate
        """
        raw = RawKnowledge(
            topic=contract.topic,
            domain=contract.resolved_domain,
        )

        logger.info("🌐 Initiating web collection pipeline")
        
        # 1. Get URLs via Scrapling search
        search_query = f"{contract.resolved_domain} {contract.topic}"
        urls = search_web(search_query, max_results=self.settings.max_sources)
        
        if not urls:
            logger.warning("No URLs found, falling back to LLM internal knowledge.")
            extracted = await self._extract_from_llm(
                contract.resolved_domain, contract.topic, 
                content=f"Provide comprehensive knowledge about {contract.topic} in {contract.resolved_domain}."
            )
            self._merge_knowledge(raw, extracted)
            raw.source_count += 1
        else:
            # 2 & 3. Fetch and extract
            from agent.services.chunker import get_chunker
            chunker = get_chunker()
            
            for url in urls:
                content = scrape_page(url)
                if not content:
                    continue
                    
                chunks = chunker.chunk_text(content)
                logger.info(f"🧠 Extracting primitives from {len(chunks)} chunks of: {url}")
                
                for chunk in chunks:
                    extracted = await self._extract_from_llm(
                        contract.resolved_domain, contract.topic, chunk
                    )
                    self._merge_knowledge(raw, extracted)
                raw.source_count += 1

        # 4. Apply semantic entropy filter
        raw = self._entropy_filter(raw)

        logger.info(
            f"✅ Collected: {len(raw.definitions)} definitions, "
            f"{len(raw.invariants)} invariants, "
            f"{len(raw.edge_cases)} edge cases, "
            f"{len(raw.code_patterns)} code patterns"
        )
        return raw

    async def collect_from_web(self, contract: LearningContract) -> RawKnowledge:
        """Alias for backward compatibility."""
        return await self.collect(contract)

    async def _extract_from_llm(self, domain: str, topic: str, content: str) -> dict:
        """Use LLM to extract structured knowledge iteratively."""
        prompt = KNOWLEDGE_EXTRACTOR.format(
            topic=topic,
            domain=domain,
            content=content,
        )
        extracted = await llm_complete_json(prompt)
        
        # Iterative verification loop (up to 2 more times)
        max_attempts = 2
        for _ in range(max_attempts):
            verify_prompt = KNOWLEDGE_VERIFIER.format(
                content=content,
                extracted=str(extracted)
            )
            verification = await llm_complete_json(verify_prompt)
            if verification.get("all_extracted", True):
                break
                
            # Merge missed knowledge
            for key in ["definitions", "invariants", "constraints", "edge_cases", "failure_scenarios", "code_patterns"]:
                if key in verification and isinstance(verification[key], list):
                    if key not in extracted:
                        extracted[key] = []
                    extracted[key].extend(verification[key])
                    
        return extracted

    def _merge_knowledge(self, raw: RawKnowledge, extracted: dict) -> None:
        """Merge extracted data into raw knowledge."""
        for key in ["definitions", "invariants", "constraints", "edge_cases",
                     "failure_scenarios"]:
            existing = getattr(raw, key)
            for item in extracted.get(key, []):
                if item and item not in existing:
                    existing.append(item)

        for pattern in extracted.get("code_patterns", []):
            # Check unique codes
            existing_codes = [p.get("code") for p in raw.code_patterns if isinstance(p, dict)]
            if pattern and isinstance(pattern, dict) and pattern.get("code") not in existing_codes:
                raw.code_patterns.append(pattern)

    def _entropy_filter(self, raw: RawKnowledge) -> RawKnowledge:
        """Remove semantically duplicate information using Embedder."""
        logger.info("🧹 Applying semantic entropy filter (Embeddings)")
        raw.definitions = self._semantic_dedup(raw.definitions)
        raw.invariants = self._semantic_dedup(raw.invariants)
        raw.constraints = self._semantic_dedup(raw.constraints)
        raw.edge_cases = self._semantic_dedup(raw.edge_cases)
        raw.failure_scenarios = self._semantic_dedup(raw.failure_scenarios)
        return raw

    def _semantic_dedup(self, items: list[str]) -> list[str]:
        """Remove near-duplicate strings using Cosine Similarity > Threshold."""
        if len(items) <= 1:
            return items

        try:
            embedder = get_embedder()
            
            # Embed all items in batch
            vectors = embedder.embed_texts(items)
            vectors = np.array(vectors)
            
            # Compute cosine similarity matrix (embeddings are normalized)
            similarity = np.dot(vectors, vectors.T)
            
            unique_indices = []
            for i in range(len(items)):
                is_duplicate = False
                for j in unique_indices:
                    # Threshold: 0.92 default
                    if similarity[i, j] >= self.settings.entropy_threshold:
                        is_duplicate = True
                        # Replace if current is longer/more detailed than existing
                        if len(items[i]) > len(items[j]):
                            unique_indices[unique_indices.index(j)] = i
                        break
                
                if not is_duplicate:
                    unique_indices.append(i)
                    
            return [items[i] for i in unique_indices]

        except Exception as e:
            logger.warning(f"Semantic deduplication failed, using text fallback: {e}")
            return self._text_dedup(items)

    def _text_dedup(self, items: list[str]) -> list[str]:
        """Simple word-overlap similarity (Jaccard) fallback."""
        if len(items) <= 1:
            return items
        unique = [items[0]]
        for item in items[1:]:
            is_dup = False
            for existing in unique:
                words_a = set(item.lower().split())
                words_b = set(existing.lower().split())
                if not words_a or not words_b:
                    continue
                intersection = words_a & words_b
                union = words_a | words_b
                similarity = len(intersection) / len(union)
                
                if similarity > 0.8:
                    is_dup = True
                    if len(item) > len(existing):
                        unique[unique.index(existing)] = item
                    break
            if not is_dup:
                unique.append(item)
        return unique
