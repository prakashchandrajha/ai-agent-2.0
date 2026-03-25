"""EKU Compressor — Phase 7.

Converts all gathered, verified, executed knowledge into a compact
Executable Knowledge Unit. No raw text storage allowed.
"""

import json
import logging

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


class EKUCompressor:
    """Compresses all learning artifacts into a single EKU."""

    async def compress(
        self,
        raw: RawKnowledge,
        verified: VerificationResult,
        executed: ExecutionResults,
        failures: list[FailureKnowledgeUnit],
        transformations: list[Transformation] | None = None,
    ) -> ExecutableKnowledgeUnit:
        """Compress multi-phase learning into a single EKU."""
        logger.info("🗜️  Compressing knowledge into EKU...")

        # Ask LLM to compress
        compressed = await llm_complete_json(
            EKU_COMPRESSOR.format(
                topic=raw.topic,
                domain=raw.domain,
                definitions=json.dumps(raw.definitions),
                invariants=json.dumps(raw.invariants),
                constraints=json.dumps(raw.constraints),
                execution_results=json.dumps({
                    "pass_rate": executed.pass_rate,
                    "passed_count": len(executed.passed),
                    "failed_count": len(executed.failed),
                    "crash_count": len(executed.crashes),
                }),
                failures=json.dumps([
                    {"type": f.failure_type, "cause": f.root_cause,
                     "prevention": f.prevention_rule}
                    for f in failures
                ]),
                transformations=json.dumps([
                    {"action": t.action, "when": t.when, "why": t.why,
                     "when_not": t.when_not}
                    for t in (transformations or [])
                ]),
            )
        )

        # Build EKU from compressed data
        eku = ExecutableKnowledgeUnit(
            concept=compressed.get("concept", raw.topic),
            domain=raw.domain,
            topic=raw.topic,
            definition=compressed.get("definition", ""),
            invariants=compressed.get("invariants", raw.invariants),
            constraints=compressed.get("constraints", raw.constraints),
        )

        # Add execution templates
        for tmpl in compressed.get("execution_templates", []):
            eku.execution_templates.append(CodeTemplate(
                description=tmpl.get("description", ""),
                code=tmpl.get("code", ""),
                language=tmpl.get("language", "python"),
                verified=True,
            ))

        # Add edge cases
        for ec in compressed.get("edge_cases", []):
            eku.edge_cases.append(EdgeCase(
                scenario=ec.get("scenario", ""),
                behavior=ec.get("behavior", ""),
                handling=ec.get("handling", ""),
            ))

        # Add failure memory
        eku.failure_memory = failures

        # Add transformations
        for tf in compressed.get("transformations", []):
            eku.transformations.append(Transformation(
                action=tf.get("action", ""),
                when=tf.get("when", ""),
                why=tf.get("why", ""),
                when_not=tf.get("when_not", ""),
                alternative=tf.get("alternative", ""),
                trade_offs=tf.get("trade_offs", {}),
            ))

        # Copy test results from execution
        for tr in executed.all_results:
            eku.add_test_result(tr)

        # Set initial confidence from verification + execution
        base_confidence = (verified.confidence_score + executed.pass_rate) / 2
        eku.confidence = max(0.0, min(1.0, base_confidence))

        logger.info(
            f"✅ EKU compressed: '{eku.concept}' "
            f"(confidence={eku.confidence:.2f}, "
            f"invariants={len(eku.invariants)}, "
            f"templates={len(eku.execution_templates)}, "
            f"failures={len(eku.failure_memory)})"
        )

        return eku
