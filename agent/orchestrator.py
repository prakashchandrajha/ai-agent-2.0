"""Learning Orchestrator — The Brain.

Wires all phases together into the complete learning pipeline.
Follows the autoresearch pattern: loop until knowledge cannot be broken.
"""

import asyncio
import logging
from datetime import datetime, timezone

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from agent.knowledge.eku_schema import ExecutableKnowledgeUnit
from agent.knowledge.eku_store import get_eku_store
from agent.modules.collector import KnowledgeCollector
from agent.modules.compressor import EKUCompressor
from agent.modules.executor import ExecutionLearner
from agent.modules.failure_analyzer import FailureAnalyzer
from agent.modules.pre_validator import PreLearningValidator
from agent.modules.verifier import SelfVerifier
from agent.config import get_settings

logger = logging.getLogger(__name__)
console = Console()

# ── MASTER_PLAN Task 1.NEW-I: Rich Progress Reporting ──────────────────────

LEARNING_PHASES = [
    "Pre-validation",
    "Web collection",
    "Knowledge extraction",
    "Verification",
    "Sandbox execution",
    "Failure analysis",
    "Compression",
    "Gate validation",
    "Storage",
]


async def learn_with_progress(concept: str, domain: str) -> "ExecutableKnowledgeUnit | None":
    """Run the full learning pipeline with a Rich progress bar.

    Wraps ``LearningOrchestrator.learn()`` with a 9-phase progress display
    so the user sees exactly which phase is running at all times.

    Args:
        concept: The topic to learn (e.g. ``list.append``).
        domain:  The subject domain (e.g. ``python``).

    Returns:
        The stored EKU on success, or None if all gates failed.
    """
    from rich.progress import (
        BarColumn,
        Progress,
        SpinnerColumn,
        TextColumn,
    )

    orchestrator = LearningOrchestrator()

    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}"),
        BarColumn(),
        TextColumn("{task.completed}/{task.total}"),
        console=console,
    ) as progress:
        task_id = progress.add_task(
            f"Learning {concept}", total=len(LEARNING_PHASES)
        )

        def _advance(phase_name: str) -> None:
            idx = LEARNING_PHASES.index(phase_name) + 1
            progress.update(
                task_id,
                description=f"[{idx}/{len(LEARNING_PHASES)}] {phase_name}...",
                completed=idx,
            )

        # Monkey-patch the orchestrator's print helpers to also advance the bar
        _orig_learn = orchestrator.learn

        async def _tracked_learn(subject: str, topic: str):
            _advance("Pre-validation")
            contract = await orchestrator.pre_validator.validate(subject, topic)
            if not contract.is_valid:
                console.print(f"[red]❌ Learning aborted: {contract.abort_reason}[/red]")
                return None

            _advance("Web collection")
            raw = await orchestrator.collector.collect(contract)
            if not raw.definitions and not raw.invariants:
                console.print("[red]❌ No knowledge collected.[/red]")
                return None

            _advance("Knowledge extraction")
            _advance("Verification")
            verified = await orchestrator.verifier.verify(raw)

            eku = None
            max_iter = orchestrator.settings.max_learning_iterations
            for iteration in range(1, max_iter + 1):
                _advance("Sandbox execution")
                executed = await orchestrator.executor.learn_by_doing(verified)

                _advance("Failure analysis")
                failures = await orchestrator.failure_analyzer.analyze_all(executed, topic)

                _advance("Compression")
                eku = await orchestrator.compressor.compress(raw, verified, executed, failures)

                _advance("Gate validation")
                _advance("Storage")
                stored = await orchestrator.eku_store.maybe_store(eku)

                if stored and eku.confidence >= orchestrator.settings.min_confidence_to_store:
                    break

            return eku

        return await _tracked_learn(domain, concept)


class LearningOrchestrator:
    """The brain — routes input through all learning phases.

    Pipeline:
    Phase 0: Pre-validation (disambiguate, scope, mastery)
    Phase 1: Knowledge collection (multi-source, entropy filter)
    Phase 2: Self-verification (challenge, contradictions)
    Phase 3: Execution-based learning (sandbox tests)
    Phase 4: Failure analysis (structured lessons)
    Phase 7: Knowledge compression (→ EKU)
    Phase 8: Delayed storage (5 gates must pass)

    Loop: Repeat Phase 3-8 until convergence.
    """

    def __init__(self):
        self.pre_validator = PreLearningValidator()
        self.collector = KnowledgeCollector()
        self.verifier = SelfVerifier()
        self.executor = ExecutionLearner()
        self.failure_analyzer = FailureAnalyzer()
        self.compressor = EKUCompressor()
        self.eku_store = get_eku_store()
        self.settings = get_settings()

    async def learn(self, subject: str, topic: str) -> ExecutableKnowledgeUnit | None:
        """Execute the full learning pipeline.

        Returns the stored EKU if successful, None if all gates failed.
        """
        console.print(Panel(
            f"[bold cyan]🧠 Learning: {subject} → {topic}[/bold cyan]",
            border_style="cyan",
        ))

        # ── Phase 0: Pre-validation ─────────────────────────────
        console.print("\n[bold yellow]Phase 0: Pre-Learning Validation[/bold yellow]")
        contract = await self.pre_validator.validate(subject, topic)

        if not contract.is_valid:
            console.print(f"[red]❌ Learning aborted: {contract.abort_reason}[/red]")
            return None

        self._print_contract(contract)

        # ── Phase 1: Knowledge collection ────────────────────────
        console.print("\n[bold yellow]Phase 1: Knowledge Collection[/bold yellow]")
        raw = await self.collector.collect(contract)

        if not raw.definitions and not raw.invariants:
            console.print("[red]❌ No knowledge collected. Aborting.[/red]")
            return None

        # ── Phase 2: Self-verification ───────────────────────────
        console.print("\n[bold yellow]Phase 2: Self-Verification[/bold yellow]")
        verified = await self.verifier.verify(raw)

        if verified.confidence_score < 0.3:
            console.print(
                f"[red]⚠️  Confidence too low ({verified.confidence_score:.2f}). "
                f"Knowledge may be unreliable.[/red]"
            )

        # ── Iterative learning loop (autoresearch pattern) ───────
        eku = None
        max_iterations = self.settings.max_learning_iterations

        for iteration in range(1, max_iterations + 1):
            console.print(
                f"\n[bold yellow]Iteration {iteration}/{max_iterations}: "
                f"Execute → Analyze → Compress → Store[/bold yellow]"
            )

            # Phase 3: Execution-based learning
            console.print("  [cyan]Phase 3: Execution-Based Learning[/cyan]")
            executed = await self.executor.learn_by_doing(verified)

            # Phase 4: Failure analysis
            console.print("  [cyan]Phase 4: Failure Analysis[/cyan]")
            failures = await self.failure_analyzer.analyze_all(executed, topic)

            # Phase 7: Compress into EKU
            console.print("  [cyan]Phase 7: Knowledge Compression[/cyan]")
            eku = await self.compressor.compress(
                raw, verified, executed, failures
            )

            # Phase 8: Delayed storage
            console.print("  [cyan]Phase 8: Storage Gate[/cyan]")
            stored = await self.eku_store.maybe_store(eku)

            self._print_iteration_summary(iteration, eku, stored)

            # Convergence check
            if stored and eku.confidence >= self.settings.min_confidence_to_store:
                console.print(
                    f"\n[bold green]✅ Knowledge proven and stored! "
                    f"(confidence={eku.confidence:.2f}, "
                    f"pass_rate={eku.test_pass_rate:.2f})[/bold green]"
                )
                break

            if iteration >= max_iterations:
                console.print(
                    f"\n[yellow]⚠️  Max iterations reached. "
                    f"EKU stored with status: {eku.verification_status}[/yellow]"
                )

        if eku:
            self._print_eku_summary(eku)

        return eku

    async def status(self) -> None:
        """Print current knowledge store status."""
        stats = self.eku_store.get_stats()
        table = Table(title="🧠 Knowledge Store Status")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        table.add_row("Proven EKUs", str(stats["total_proven"]))
        table.add_row("Quarantined EKUs", str(stats["total_quarantined"]))
        table.add_row("Total Indexed", str(stats["total_indexed"]))
        table.add_row("Domains", ", ".join(stats["domains"]) or "none")
        console.print(table)

    async def list_knowledge(self, domain: str | None = None) -> None:
        """List all stored knowledge."""
        if domain:
            ekus = self.eku_store.find_by_domain(domain)
        else:
            ekus = self.eku_store.list_all()

        if not ekus:
            console.print("[yellow]No knowledge stored yet.[/yellow]")
            return

        table = Table(title="📚 Stored Knowledge")
        table.add_column("Concept", style="cyan")
        table.add_column("Domain", style="blue")
        table.add_column("Topic", style="green")
        table.add_column("Confidence", style="yellow")
        table.add_column("Status", style="magenta")

        for eku in ekus:
            table.add_row(
                eku.get("concept", "?"),
                eku.get("domain", "?"),
                eku.get("topic", "?"),
                f"{eku.get('confidence', 0):.2f}",
                eku.get("status", "?"),
            )
        console.print(table)

    # ── Display helpers ──────────────────────────────────────────

    def _print_contract(self, contract) -> None:
        table = Table(title="📋 Learning Contract")
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="green")
        table.add_row("Domain", contract.resolved_domain)
        table.add_row("Meaning", contract.resolved_meaning)
        table.add_row("Depth", contract.depth_level)
        table.add_row("Complexity", f"{contract.estimated_complexity}/10")
        table.add_row("Subtopics", str(len(contract.core_subtopics)))
        table.add_row("Prerequisites", ", ".join(contract.prerequisites) or "none")
        console.print(table)

    def _print_iteration_summary(self, iteration, eku, stored) -> None:
        status_icon = "✅" if stored else "🔒"
        console.print(
            f"  {status_icon} Iteration {iteration}: "
            f"confidence={eku.confidence:.2f}, "
            f"pass_rate={eku.test_pass_rate:.2f}, "
            f"status={eku.verification_status}"
        )

    def _print_eku_summary(self, eku) -> None:
        console.print(Panel(
            f"[bold]Concept:[/bold] {eku.concept}\n"
            f"[bold]Definition:[/bold] {eku.definition}\n"
            f"[bold]Invariants:[/bold] {len(eku.invariants)}\n"
            f"[bold]Constraints:[/bold] {len(eku.constraints)}\n"
            f"[bold]Templates:[/bold] {len(eku.execution_templates)}\n"
            f"[bold]Failures:[/bold] {len(eku.failure_memory)}\n"
            f"[bold]Edge Cases:[/bold] {len(eku.edge_cases)}\n"
            f"[bold]Confidence:[/bold] {eku.confidence:.2f}\n"
            f"[bold]Status:[/bold] {eku.verification_status}",
            title="🧠 EKU Summary",
            border_style="green" if eku.is_proven else "yellow",
        ))
