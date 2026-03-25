"""CLI interface — the agent's command line entry point."""

import asyncio
import logging
import sys

import typer
from rich.console import Console
from rich.logging import RichHandler

app = typer.Typer(
    name="agent",
    help="🧠 AI Autonomous Engineer — learns, validates, and evolves knowledge.",
    add_completion=False,
)
console = Console()


def _setup_logging(verbose: bool = False) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(message)s",
        handlers=[RichHandler(
            console=console,
            show_time=False,
            show_path=False,
            markup=True,
        )],
    )


@app.command()
def learn(
    subject: str = typer.Argument(..., help="Subject domain (e.g., 'python', 'javascript')"),
    topic: str = typer.Argument(..., help="Topic to learn (e.g., 'decorators', 'closures')"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable debug logging"),
):
    """🧠 Learn a topic — full pipeline from collection to verified storage."""
    _setup_logging(verbose)

    from agent.orchestrator import LearningOrchestrator

    orchestrator = LearningOrchestrator()

    try:
        eku = asyncio.run(orchestrator.learn(subject, topic))
        if eku and eku.is_proven:
            console.print("\n[bold green]✅ Learning complete. Knowledge proven and stored.[/bold green]")
            raise typer.Exit(0)
        elif eku:
            console.print(f"\n[yellow]⚠️  Learning complete. Status: {eku.verification_status}[/yellow]")
            raise typer.Exit(0)
        else:
            console.print("\n[red]❌ Learning failed.[/red]")
            raise typer.Exit(1)
    except KeyboardInterrupt:
        console.print("\n[yellow]⏹  Learning interrupted.[/yellow]")
        raise typer.Exit(130)


@app.command()
def status(
    verbose: bool = typer.Option(False, "--verbose", "-v"),
):
    """📊 Show knowledge store status."""
    _setup_logging(verbose)

    from agent.orchestrator import LearningOrchestrator
    orchestrator = LearningOrchestrator()
    asyncio.run(orchestrator.status())


@app.command("list")
def list_knowledge(
    domain: str = typer.Option(None, "--domain", "-d", help="Filter by domain"),
    verbose: bool = typer.Option(False, "--verbose", "-v"),
):
    """📚 List all stored knowledge."""
    _setup_logging(verbose)

    from agent.orchestrator import LearningOrchestrator
    orchestrator = LearningOrchestrator()
    asyncio.run(orchestrator.list_knowledge(domain))


@app.command()
def health(
    verbose: bool = typer.Option(False, "--verbose", "-v"),
):
    """🏥 Check LLM backend health."""
    _setup_logging(verbose)

    from agent.llm.client import get_llm_client

    async def _check():
        client = get_llm_client()
        result = await client.check_health()
        if result["status"] == "healthy":
            console.print(f"[green]✅ LLM backend healthy ({result['backend']})[/green]")
        else:
            console.print(f"[red]❌ LLM backend unhealthy: {result}[/red]")

    asyncio.run(_check())


@app.command()
def inspect(
    eku_id: str = typer.Argument(..., help="EKU ID to inspect"),
    verbose: bool = typer.Option(False, "--verbose", "-v"),
):
    """🔍 Inspect a stored EKU in detail."""
    _setup_logging(verbose)

    import json
    from agent.knowledge.eku_store import get_eku_store

    store = get_eku_store()
    eku = store.load_eku(eku_id)

    if eku:
        console.print_json(json.dumps(eku.to_dict(), indent=2, default=str))
    else:
        console.print(f"[red]❌ EKU not found: {eku_id}[/red]")


def main():
    app()


if __name__ == "__main__":
    main()
