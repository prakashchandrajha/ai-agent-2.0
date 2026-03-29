"""EKU Compressor — MASTER_PLAN Tasks 1.7 + 1.NEW-F.

Two-pass lossless compression:
  Pass 1 — structured data merged directly (no LLM, zero data loss)
  Pass 2 — LLM synthesises ONLY prose fields (definition, invariants)

Confidence is capped by evidence count (EVIDENCE_CEILING).
"""

import json
import logging
from dataclasses import dataclass, field

from agent.knowledge.eku_schema import (
    CodeTemplate,
    EdgeCase,
    ExecutableKnowledgeUnit,
    FailureKnowledgeUnit,
    Transformation,
)
from agent.llm.helpers import llm_complete_json
from agent.llm.prompts import EKU_COMPRESSOR
from agent.modules.collector import RawKnowledge
from agent.modules.executor import ExecutionResults
from agent.modules.verifier import VerificationResult

logger = logging.getLogger(__name__)

# ── MASTER_PLAN 1.NEW-F: Confidence Ceiling by Evidence Count ─────────────
EVIDENCE_CEILING: dict[int, float] = {
    1: 0.60,   # Single source → max 60 %
    2: 0.75,   # Two sources  → max 75 %
    3: 0.85,   # Three sources → max 85 %
}


def calculate_confidence(
    test_pass_rate: float,
    source_authority: float,
    source_count: int,
    robustness_score: float,
) -> float:
    """Calculate EKU confidence with source-count ceiling.

    Weights per MASTER_PLAN:
      test_pass_rate   0.40
      source_authority 0.25
      robustness_score 0.35

    Args:
        test_pass_rate:   Fraction of tests that passed (0–1).
        source_authority: Mean authority score of all scraped sources (0–1).
        source_count:     Number of distinct sources used.
        robustness_score: Mean robustness score from sandbox results (0–1).

    Returns:
        confidence in [0, ceiling] where ceiling is from EVIDENCE_CEILING.
    """
    raw = (
        test_pass_rate   * 0.40
        + source_authority * 0.25
        + robustness_score * 0.35
    )
    ceiling = EVIDENCE_CEILING.get(source_count, 0.95)
    return round(min(raw, ceiling), 4)


class EKUCompressor:
    """Compresses all learning artefacts into a single EKU.

    MASTER_PLAN Task 1.7 — two-pass lossless compressor:
    - Pass 1: direct merge of structured data (no LLM involved)
    - Pass 2: LLM synthesises prose (definition, invariants)
    """

    async def compress(
        self,
        raw: RawKnowledge,
        verified: VerificationResult,
        executed: ExecutionResults,
        failures: list[FailureKnowledgeUnit],
        transformations: list[Transformation] | None = None,
    ) -> ExecutableKnowledgeUnit:
        """Compress multi-phase learning into a single EKU."""
        logger.info("🗜️  Compressing knowledge into EKU (2-pass lossless)…")

        # ── PASS 1: Direct structured merge (zero data loss, no LLM) ──────
        structured = self._merge_structured(raw, executed, failures, transformations)

        # ── PASS 2: LLM synthesises prose fields only ──────────────────────
        prose = await self._synthesise_prose(raw)

        # ── Build the EKU ──────────────────────────────────────────────────
        eku = ExecutableKnowledgeUnit(
            concept=prose.get("concept", raw.topic),
            domain=raw.domain,
            topic=raw.topic,
            definition=prose.get("definition", ""),
            invariants=prose.get("invariants", raw.invariants),
            constraints=prose.get("constraints", raw.constraints),
        )

        # Structured fields (lossless from Pass 1)
        for tmpl in structured["execution_templates"]:
            eku.execution_templates.append(tmpl)
        for ec in structured["edge_cases"]:
            eku.edge_cases.append(ec)
        eku.failure_memory = structured["failure_memory"]
        for tf in structured["transformations"]:
            eku.transformations.append(tf)
        for tr in executed.all_results:
            eku.add_test_result(tr)
        eku.source_urls = list(set(structured["source_urls"]))
        eku.hard_constraints = list(set(structured["hard_constraints"]))

        # ── Confidence with evidence ceiling ──────────────────────────────
        source_count = len(eku.source_urls)
        avg_authority = getattr(raw, "avg_source_authority", 0.5)
        avg_robustness = (
            sum(
                getattr(r, "robustness_score", 1.0)
                for r in executed.all_results
            ) / len(executed.all_results)
            if executed.all_results else 1.0
        )
        eku.confidence = calculate_confidence(
            test_pass_rate=executed.pass_rate,
            source_authority=avg_authority,
            source_count=source_count,
            robustness_score=avg_robustness,
        )

        logger.info(
            "✅ EKU compressed: '%s' "
            "(confidence=%.2f, ceiling=%s sources, "
            "invariants=%d, templates=%d, failures=%d)",
            eku.concept,
            eku.confidence,
            source_count,
            len(eku.invariants),
            len(eku.execution_templates),
            len(eku.failure_memory),
        )
        return eku

    # ── Pass 1 ────────────────────────────────────────────────────────────

    def _merge_structured(
        self,
        raw: RawKnowledge,
        executed: ExecutionResults,
        failures: list[FailureKnowledgeUnit],
        transformations: list[Transformation] | None,
    ) -> dict:
        """Merge structured data from all phases — no LLM involved."""
        templates: list[CodeTemplate] = []
        edge_cases: list[EdgeCase] = []
        source_urls: list[str] = list(getattr(raw, "source_urls", []))
        hard_constraints: list[str] = list(getattr(raw, "constraints", []))
        tfs: list[Transformation] = list(transformations or [])

        # Pull code patterns from raw as execution templates
        for pattern in getattr(raw, "code_patterns", []):
            if isinstance(pattern, str) and pattern.strip():
                templates.append(CodeTemplate(
                    description="Extracted code pattern",
                    code=pattern,
                    language="python",
                    verified=True,
                ))

        # Edge cases from raw knowledge
        for ec in getattr(raw, "edge_cases", []):
            if isinstance(ec, str) and ec.strip():
                edge_cases.append(EdgeCase(
                    scenario=ec,
                    behavior="See documentation",
                    handling="Handle as described",
                ))

        return {
            "execution_templates": templates,
            "edge_cases": edge_cases,
            "failure_memory": failures,
            "transformations": tfs,
            "source_urls": source_urls,
            "hard_constraints": hard_constraints,
        }

    # ── Pass 2 ────────────────────────────────────────────────────────────

    async def _synthesise_prose(self, raw: RawKnowledge) -> dict:
        """Ask LLM to synthesise ONLY prose fields."""
        try:
            result = await llm_complete_json(
                EKU_COMPRESSOR.format(
                    topic=raw.topic,
                    domain=raw.domain,
                    definitions=json.dumps(raw.definitions),
                    invariants=json.dumps(raw.invariants),
                    constraints=json.dumps(raw.constraints),
                    execution_results=json.dumps({}),
                    failures=json.dumps([]),
                    transformations=json.dumps([]),
                )
            )
            return result or {}
        except Exception as exc:
            logger.warning("Prose synthesis failed (%s) — using raw data", exc)
            return {
                "concept": raw.topic,
                "definition": "; ".join(raw.definitions[:2]) if raw.definitions else "",
                "invariants": raw.invariants,
                "constraints": raw.constraints,
            }
