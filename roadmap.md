# ULTIMATE ENGINEER AGENT ROADMAP
## The Single Source of Truth. Supersedes Every Previous Document.
## Compiled: 2026-03-30
## Goal: AI agent that thinks, plans, codes, debugs, and builds like a real senior CS engineer.
## Can work on any project. Any language. Any size. Any situation.
Autonomous
---

# HOW TO READ THIS DOCUMENT

Every phase has exactly five things:
- WHERE YOU ARE — current honest state
- WHAT YOU BUILD — exact files, exact logic
- BEHAVIOR CHECKS — exact CLI commands, exact expected terminal output
- WHAT AGENT CAN DO AFTER — real verified capability
- EXIT CRITERIA — hard gates, not suggestions

Test passing does not equal phase done.
Behavior check passing equals phase done.
Never move to Phase N+1 until Phase N exit criteria all pass.

---

# THE THREE LAWS — NEVER BREAK THESE

Law 1 — LLM is used in exactly 3 modes:
  Mode A LEARN: Extract structured knowledge from raw content. Once per concept. Never again for same concept.
  Mode B ROUTE: Classify incoming task to select adapters. One lightweight call.
  Mode C GENERATE: Produce code or design using KB as constraint layer. KB guides, LLM produces.
  Everything else uses KB. If LLM is called for anything outside these three modes, something is wrong.

Law 2 — Phase gates are not suggestions:
  Without demonstrated exit criteria you are building on unknown ground.
  Skipping a gate means the next phase has a hidden crack in its foundation.

Law 3 — Dangerous zones require human confirmation. Always. No exceptions:
  Auth logic, payment processing, schema migration, secret management, encryption.
  Not even at confidence 0.99. Not even if the task looks trivial.
  A senior engineer who touches auth alone without review is not a senior engineer.

---

# WHAT YOU HAVE RIGHT NOW

39 of 39 tests passing. Infrastructure complete.

Agent has NEVER:
- Learned one real concept end to end
- Stored an EKU with all fields populated
- Answered a question from its own KB with LLM calls: 0
- Practiced anything in sandbox
- Understood a real project structure
- Fixed a real bug
- Created a real file

You have a perfectly built empty container.
Five silent problems will corrupt everything built on top. Fix them first.

---

# THINGS NO PREVIOUS DOCUMENT CAUGHT — READ BEFORE ANYTHING ELSE

These are the insights that will make the difference between a good agent and a 1000x agent.
Every one is practical, buildable, and will silently fail the system if ignored.

## Gap 1 — The Engineer Mental Model is Missing
Every previous document describes what the agent stores and what it executes. Nobody described how an engineer actually thinks before doing anything.

A real engineer receives a task and goes through this mental sequence automatically:
Do I understand the goal completely? Do I understand the constraints? What could go wrong? What do I not know? What is the minimum safe change? What will I verify when done?

This mental sequence must be the first thing that runs before any task execution. Not as a checklist the agent skips. As a structured internal monologue that generates a task brief the agent commits to before touching anything. Call it the Engineer Pre-Task Protocol.

## Gap 2 — The Project Onboarding Process is Missing
Every document talks about PMM. None describes how the agent onboards to a project the way a real engineer does on their first day.

A real engineer on day one does not just scan files. They ask: What is this system supposed to do? Who are the users? What are the invariants that must never be violated? What are the known problems the team lives with? What changed recently and why?

The agent needs a structured onboarding that produces a Project Brief — a one-page understanding of the project that every subsequent task references.

## Gap 3 — The Code Review Brain is Missing
A real senior engineer does not just write code. They review code. They read code and immediately see: this will fail under concurrent access, this has a SQL injection risk, this will be slow at scale, this is correct but nobody will understand it in six months.

The agent needs a code review mode that is separate from the implementation mode. When asked to implement something, the agent first reviews the area it will touch the same way a senior would before making changes.

## Gap 4 — The Estimation Brain is Missing
Engineers estimate. Before starting any task a senior engineer says: this is a 2-hour task, this is a 2-day task, this needs an architecture decision before any code is written.

The agent needs an estimation engine. Not for time (it has no sense of time) but for complexity, risk, and whether a task needs design-first or can go straight to implementation.

## Gap 5 — The Dependency Hell Handler is Missing
Every real project eventually hits: you upgrade library A, and libraries B, C, and D break because they pin different versions of A's dependencies. No previous document handles this.

The agent needs a dependency conflict analyzer that runs before any dependency change and maps the full transitive dependency tree for potential conflicts.

## Gap 6 — The Database Safety Brain is Missing
Schema migrations are the most dangerous thing a developer does to a production system. A migration that drops a column, changes a type, or adds a NOT NULL constraint without a default can take down production.

The agent needs a migration safety analyzer that classifies every schema change as: safe to run live, requires maintenance window, requires data backfill first, requires rollback plan.

## Gap 7 — The Test Generation Brain is Missing
Previous documents mention testing. None describe how the agent generates tests the way a senior engineer would. A senior does not write one test per function. They write tests for invariants, tests for edge cases from their experience, tests for the specific failures they have seen before.

The agent needs to generate tests from three sources: the EKU failure_modes field (known edge cases), the failure library (cases that actually failed before), and invariants extracted from business logic comments.

## Gap 8 — The Documentation Reader is Missing
A real project has documentation that is partly right, partly wrong, and partly outdated. An engineer reads docs knowing this. They cross-reference docs against the actual code. They trust the code over the docs when they conflict.

The agent needs a documentation trust engine: when docs and code disagree, code wins. When docs describe behavior that does not exist in code, flag it. When code does something docs do not mention, extract it as tribal knowledge.

## Gap 9 — The Rollback Planner is Missing
Before making any significant change, a senior engineer knows how to undo it. They think: if this goes wrong, what is the rollback plan?

The agent needs a rollback planner that runs before any action scoring below 7 on reversibility. The rollback plan must be created and stored before execution begins.

## Gap 10 — The Architecture Smell Detector is Missing
Over time, projects accumulate architectural debt that is not obvious in any single file. God services that do too much, circular dependencies between modules, layers that talk to the wrong other layers, missing abstraction boundaries.

The agent needs an architecture smell detector that runs when onboarding to a project and periodically as the project evolves. It reports smells to the PMM observation queue, never fixes them without being asked.

---

# COMPLETE FILE STRUCTURE
## Every file referenced in this document. Build this tree first.

```
agent/
├── adapters/
│   ├── __init__.py
│   ├── base_adapter.py                 # Abstract interface ALL adapters implement
│   ├── coding_adapter.py               # Sandbox execution practice
│   ├── framework_adapter.py            # Minimal working example practice
│   ├── system_design_adapter.py        # Self-critique loop practice
│   ├── reasoning_adapter.py            # Chain validation practice
│   ├── router.py                       # Selects 1-4 adapters per task
│   ├── language_detector.py            # Detects project language from files
│   ├── language_registry.py            # Per-language EKU namespaces
│   └── personality_detector.py         # Startup / balanced / enterprise profiles
├── execution/
│   ├── __init__.py
│   ├── engineer_protocol.py            # NEW: Pre-task mental model (Gap 1)
│   ├── estimation_engine.py            # NEW: Complexity/risk estimation (Gap 4)
│   ├── decomposer.py                   # Task → DAG of subtasks
│   ├── closed_loop.py                  # Expect → Act → Observe → Revise
│   ├── reversibility.py                # Score 0-10, block score 0-3
│   ├── rollback_planner.py             # NEW: Create rollback before execute (Gap 9)
│   ├── preemptive_check.py             # Red-team own plan before running
│   ├── composition_verifier.py         # Re-run all assertions after file change
│   ├── progress_validator.py           # Technical + directional + efficiency
│   ├── minimum_change.py               # Scope creep prevention
│   ├── stop_condition.py               # Goal-achieved + diminishing-returns
│   └── goal_gradient.py                # Are we moving toward the goal?
├── knowledge/
│   ├── __init__.py
│   ├── eku_schema.py                   # EKU data structure (extend existing)
│   ├── eku_store.py                    # EKU storage (extend existing)
│   ├── knowledge_graph.py              # Dependency edges between EKUs
│   ├── confidence_cascade.py           # Real chain confidence (product not last)
│   ├── execution_trace.py              # Traces as first-class knowledge
│   ├── context_classifier.py           # CODEBASE_LOCAL vs CROSS_PROJECT vs CANONICAL
│   ├── cross_adapter_propagator.py     # Coding learns → system design gets hint
│   ├── pattern_compiler.py             # Tier 2: auto-derive patterns from 5+ EKUs
│   ├── heuristic_compiler.py           # Tier 3: auto-derive heuristics from 3+ patterns
│   ├── version_registry.py             # Track exact version per project
│   ├── vector_store.py                 # ChromaDB integration (replace stub)
│   ├── hybrid_retrieval.py             # BM25 + semantic search combined
│   ├── decay_scheduler.py              # Fine-grained per-category decay
│   ├── dead_knowledge.py               # Detect and quarantine unused EKUs
│   ├── verification_queue.py           # Background verification scheduler
│   └── dependency_conflict_analyzer.py # NEW: Transitive dependency mapping (Gap 5)
├── project_memory/
│   ├── __init__.py
│   ├── pmm.py                          # Project Memory Module
│   ├── onboarding.py                   # NEW: Day-one project understanding (Gap 2)
│   ├── architecture_smell_detector.py  # NEW: God services, circular deps (Gap 10)
│   └── documentation_trust_engine.py  # NEW: Code wins over docs on conflict (Gap 8)
├── engineer/
│   ├── __init__.py
│   ├── code_reviewer.py                # NEW: Review before touching (Gap 3)
│   ├── migration_safety_analyzer.py    # NEW: Schema change classification (Gap 6)
│   └── test_generator.py              # NEW: Tests from EKU + failure library (Gap 7)
├── senior/
│   ├── __init__.py
│   ├── unknown_unknown_detector.py     # Declare uncertainty before task
│   ├── meta_adapter.py                 # Orchestrate 4 adapters, enforce sequencing
│   ├── incremental_verifier.py         # Checkpoint every 3-5 subtasks
│   ├── input_noise_detector.py         # One clarifying question if ambiguous
│   └── dangerous_zone_guard.py         # Detect + block auth/payment/schema/secrets
├── testing/
│   ├── __init__.py
│   ├── adversarial_tester.py           # Break own success
│   ├── false_positive_detector.py      # Three categories of false success
│   ├── fragility_tracker.py            # High-change files → shadow tests
│   └── semantic_diff.py                # Business rule extraction + assertion
├── self_improvement/
│   ├── __init__.py
│   ├── assessment_error_log.py         # Gap: claimed vs found
│   ├── bias_detector.py                # Error type 3+ times = systematic bias
│   └── cross_project_learner.py        # Pattern across 3+ projects → Tier 2/3
├── llm/
│   ├── client.py                       # Extend: heartbeat monitor
│   ├── cache.py                        # Existing
│   └── helpers.py                      # Extend: structured JSON prompts
├── services/
│   ├── web_search.py                   # Extend: DDG rate limit guard
│   ├── web_scraper.py                  # Extend: per-URL timeout + version detection
│   ├── chunker.py                      # Existing
│   └── embedder.py                     # Existing
├── orchestrator.py                     # Extend: global session timeout + bulk learn
├── health_check.py                     # Full system health before every session
├── cli.py                              # CLI entry point (extend with all new commands)
└── config/
    └── seed_manifest.yaml              # Bootstrap: what to learn first

data/
├── ekus/                               # One JSON per EKU
├── traces/                             # One JSON per execution trace
├── patterns/                           # Tier 2 compiled patterns
├── heuristics/                         # Tier 3 compiled heuristics
├── failure_library/                    # Structured failure records
├── project_memory/                     # One directory per project
│   └── {project_name}/
│       ├── brief.json                  # Project Brief from onboarding
│       ├── pmm.json                    # Full PMM
│       ├── architecture_smells.json    # Detected architecture issues
│       └── tribal_knowledge.json       # Project-specific knowledge
├── assessment_errors/                  # Wrong initial assessments log
├── rollback_plans/                     # Rollback plans before execution
└── verification_queue.json             # Background verification scheduler
```

---

# EMERGENCY BLOCK — DO THIS BEFORE ANY CODE CHANGES
## Time: 2-3 hours
## Gate: Nothing else starts until all 5 pass

---

## Emergency Fix 1 — Enable GPU

```bash
pkill ollama && sleep 2 && nvidia-smi
# Must show RTX 5050. If not: sudo apt install nvidia-driver-535 && sudo reboot

curl -fsSL https://ollama.com/install.sh | sh
ollama serve &
sleep 5 && ollama pull phi3:medium

ollama run phi3:medium "say hello in one word"
ollama ps
# GPU column must show non-zero memory
```

Behavior check:
```bash
time ollama run phi3:medium "write a 200-word paragraph about python lists"
```
Expected: Completes under 20 seconds. If 60+ seconds: still on CPU. Do not proceed.

Exit criteria: ollama ps shows GPU memory greater than 0. 200-word generation under 20 seconds.

---

## Emergency Fix 2 — Global Session Timeout

File: agent/orchestrator.py

```python
import asyncio, time
MAX_LEARN_TIME_SECONDS = 300

async def learn_concept_with_timeout(concept: str, domain: str):
    start = time.time()
    try:
        async with asyncio.timeout(MAX_LEARN_TIME_SECONDS):
            return await learn_with_progress(concept, domain)
    except asyncio.TimeoutError:
        elapsed = int(time.time() - start)
        print(f"\nTIMEOUT: '{concept}' exceeded {MAX_LEARN_TIME_SECONDS}s (ran {elapsed}s)")
        print("Likely: 1) GPU off  2) URL hung  3) DDG rate limited  4) LLM stuck")
        return None
```

Exit criteria: Previously hanging learn command exits after 5 minutes with specific error message.

---

## Emergency Fix 3 — Per-URL 15-Second Timeout

File: agent/services/web_scraper.py

```python
async def scrape_with_timeout(url: str) -> str:
    try:
        async with asyncio.timeout(15):
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(None, scrape_page, url) or ""
    except asyncio.TimeoutError:
        print(f"  TIMEOUT: {url} (>15s) — skipping, continuing with other URLs")
        return ""
    except Exception as e:
        print(f"  ERROR: {url} — {type(e).__name__}: {e}")
        return ""
```

Exit criteria: Non-responding URL times out after 15 seconds. Other URLs continue normally.

---

## Emergency Fix 4 — DDG Rate Limit Guard

File: agent/services/web_search.py

```python
import time
_last_search_time = 0.0
DDG_MIN_INTERVAL = 2.5

def _rate_limit_ddg():
    global _last_search_time
    elapsed = time.time() - _last_search_time
    if elapsed < DDG_MIN_INTERVAL:
        time.sleep(DDG_MIN_INTERVAL - elapsed)
    _last_search_time = time.time()

# Call _rate_limit_ddg() at start of search()
# After search, before returning:
if not results:
    print(f"  WARNING: DDG returned 0 results for '{query}'")
    print("  Possible rate limiting. If recurring: wait 60s and retry.")
```

Exit criteria: Three learn commands back-to-back never silently produce empty search results.

---

## Emergency Fix 5 — LLM Heartbeat Monitor

File: agent/llm/client.py

```python
import threading

def complete_with_heartbeat(prompt: str, model: str = "phi3:medium", timeout: int = 90) -> str:
    result = [None]
    error = [None]

    def _call():
        try:
            result[0] = complete(prompt, model=model)
        except Exception as e:
            error[0] = e

    t = threading.Thread(target=_call, daemon=True)
    t.start()
    t.join(timeout=timeout)

    if t.is_alive():
        raise TimeoutError(
            f"LLM did not respond in {timeout}s — Ollama may be unresponsive.\n"
            f"Run: ollama ps\n"
            f"If frozen: pkill ollama && ollama serve &"
        )
    if error[0]:
        raise error[0]
    return result[0]
```

Exit criteria: Killing Ollama mid-call raises clear TimeoutError with recovery instructions.

---

## After Emergency Block — Agent Capability

Cannot think yet. But runs reliably. Always reports what failed. Never hangs forever.
Every future phase builds on this reliability.

---

# PHASE 1G — FIRST COMPLETE INTEGRATION RUN
## Time: 1 hour
## Depends on: Emergency block complete
## Purpose: Prove the 39 tests represent a real working loop

---

## What you build

No new code. Prove existing code works end to end.

```bash
python -m agent learn python "list operations"
```

Expected terminal output (every line must appear):
```
[COLLECT] Fetching URLs for: list operations (python)
[COLLECT] URL 1: https://docs.python.org/... — 4823 words extracted
[CHUNK] Splitting into 8 chunks
[EMBED] Batch embedding 8 chunks
[COMPRESS] LLM call 1 of 3 — extracting structured knowledge
[COMPRESS] LLM call 2 of 3
[COMPRESS] LLM call 3 of 3
[GATE] Running mastery contract gate...
[GATE] PASS — storing EKU
[STORE] EKU stored: list_operations_python — confidence 0.72
[DONE] Learning complete. LLM calls: 3. Time: 47s
```

If TIMEOUT or ERROR appears at any line: fix that specific issue before proceeding.

```bash
python -m agent ask "how do I add an item to a list in python"
```

Expected:
```
[QUERY] Searching KB for: add item list python
[FOUND] EKU: list_operations_python — confidence 0.72
[ANSWER] Use list.append(item) to add a single item to end of list.
[SOURCE] KB only — LLM calls: 0
```

The LLM calls: 0 line is the proof. If LLM is called, retrieval is broken.

## Exit Criteria Phase 1G
1. Learn command completes under 5 minutes without hang
2. EKU file exists in data/ekus/ with all required fields: concept, what, how, when_to_use, why, failure_modes, confidence, source_urls, learned_at
3. Ask command returns with LLM calls: 0
4. python -m agent status shows KB Tier 1 count greater than 0

## What agent can do after Phase 1G
Learn one concept and answer questions about it from memory. Nothing else.
Level: student who read one chapter of a textbook.

---

# PHASE 1.5 — SEED MANIFEST AND BULK LEARNING ENGINE
## Time: 3-4 hours
## Depends on: Phase 1G complete
## Purpose: Bootstrap KB with 50-100 concepts so every later phase has real data

Without this phase, Phase 2.5 pattern compiler has no data to work with.
Pattern compiler needs 5+ EKUs. Heuristic compiler needs 15+ EKUs.
A KB with 1 EKU cannot produce intelligence. This phase is building on rock instead of sand.

---

## Task 1.5.1 — Create Seed Manifest

File: agent/config/seed_manifest.yaml

```yaml
python:
  docs_base_url: "https://docs.python.org/3/"
  tier1_core:
    - "list operations"
    - "dict operations"
    - "string operations"
    - "set operations"
    - "tuple operations"
    - "for loop patterns"
    - "exception handling"
    - "file operations"
    - "class definition"
    - "generators and iterators"
    - "decorators"
    - "context managers"
    - "type hints"
    - "dataclasses"
    - "async and await"
  tier2_stdlib:
    - "collections module"
    - "itertools module"
    - "pathlib operations"
    - "json module"
    - "logging module"
    - "threading module"
    - "subprocess module"
    - "os and sys"
    - "re module"
    - "datetime module"
    - "unittest module"
    - "abc module"
  tier3_packages:
    - "requests library"
    - "pydantic v2"
    - "sqlalchemy core"
    - "pytest basics"
    - "fastapi basics"

javascript:
  docs_base_url: "https://developer.mozilla.org/en-US/docs/Web/JavaScript/"
  tier1_core:
    - "array methods"
    - "object operations"
    - "promise patterns"
    - "closure and scope"
    - "error handling"
    - "module system"
    - "event loop"
  tier4_frameworks:
    - "react hooks basics"
    - "react component patterns"
    - "express routing"
    - "node.js fs module"

typescript:
  tier1_core:
    - "type system basics"
    - "utility types"
    - "type guards"
    - "generics"

java:
  docs_base_url: "https://docs.oracle.com/en/java/javase/17/docs/"
  tier1_core:
    - "collections framework"
    - "exception handling"
    - "streams api"
    - "concurrency basics"
    - "generics"
  tier4_frameworks:
    - "spring boot controllers"
    - "spring boot services"
    - "spring security basics"
    - "jpa repository patterns"
    - "spring data queries"

angular:
  tier4_frameworks:
    - "component lifecycle"
    - "services and dependency injection"
    - "reactive forms"
    - "rxjs observables"
    - "http client patterns"
    - "routing and guards"
    - "standalone components v17"

system_design:
  tier4_patterns:
    - "load balancing patterns"
    - "caching strategies"
    - "database sharding"
    - "rate limiting algorithms"
    - "event sourcing"
    - "circuit breaker pattern"
    - "saga pattern"
    - "api design principles"
    - "microservices communication"
    - "database indexing strategies"
```

## Task 1.5.2 — Bulk Learning Engine

File: agent/orchestrator.py (add to existing)

Logic:
1. Load seed_manifest.yaml
2. For given domain, get all concepts in specified tier
3. For each concept: check if EKU exists with confidence above 0.5, skip if yes
4. Call learn_concept_with_timeout(concept, domain)
5. Wait 3 seconds between concepts for DDG rate limit protection
6. After all concepts: run pattern_compiler
7. Print summary: X learned, Y skipped, Z failed

```bash
python -m agent seed --domain python --tier tier1_core
python -m agent seed --domain python --all-tiers
python -m agent seed --all
```

Behavior check:
```bash
python -m agent seed --domain python --tier tier1_core
```
Expected:
```
[SEED] Loading manifest for python/tier1_core — 15 concepts
[LEARN] list operations... STORED (confidence: 0.74)
[LEARN] dict operations... STORED (confidence: 0.71)
[LEARN] string operations... STORED (confidence: 0.76)
...
[PATTERN] Running pattern compiler...
[PATTERN] 2 new patterns derived (mutation_returns_none, creation_returns_new)
[SEED] Complete: 14 stored, 1 skipped, 0 failed. Time: 12m 30s
```

## Exit Criteria Phase 1.5
1. python -m agent status shows KB Tier 1 count greater than 15 after python tier1_core seed
2. Pattern compiler automatically runs and produces at least 1 pattern
3. python -m agent compile-patterns --domain python shows Tier 2 count greater than 0
4. All 15 tier1_core concepts have EKU files in data/ekus/

## What agent can do after Phase 1.5
Answer questions about 50-100 programming concepts from its own KB.
Pattern compiler has enough data to auto-derive Tier 2 patterns.
Still cannot execute tasks, understand projects, or fix bugs.
Level: student who read several textbooks and started forming mental models.

---

# PHASE 2 — KNOWLEDGE INTELLIGENCE LAYER
## Time: 5 hours
## Depends on: Phase 1.5 complete
## Purpose: KB becomes intelligent, not just a storage system

---

## Task 2.1 — Version-Aware EKU Schema Extension

File: agent/knowledge/eku_schema.py (extend existing)

Add these fields to every EKU. These are not optional. Every EKU without version data is a liability.

New required fields:
- technology_version: exact version this was learned from (e.g. "3.11", "17.2.0")
- version_range_start: version where this fact became true (e.g. "3.11")
- version_range_end: version where this stopped being true (None means still valid)
- deprecated_in_version: version where this approach became legacy (None if not deprecated)
- replaced_by: what replaced it in newer versions (None if not replaced)
- version_confidence: how certain the version detection was (0.0 to 1.0)
- adapter_type: which adapter owns this EKU (coding/framework/system_design/reasoning)
- community_warnings: list of real-world warnings from GitHub/SO
- applied_count: how many times used in actual task execution (starts at 0)
- last_applied_date: when last used in a real task

Behavior check:
```bash
python -m agent schema-validate
```
Expected: All fields listed. Any EKU missing version data flagged as needing annotation.

---

## Task 2.2 — Version Detection During Scraping

File: agent/services/web_scraper.py (extend existing)

Extract version from scraped content using these patterns:
- "New in version X.Y" → version_range_start = X.Y, version_confidence = 0.9
- "Changed in version X.Y" → note the change, update version bounds
- "Deprecated since version X.Y" → deprecated_in_version = X.Y
- Version in URL path "/3.11/" → version_confidence = 0.7
- No version signal found → technology_version = "unknown", version_confidence = 0.0

Behavior check:
```bash
python -m agent learn python "asyncio.timeout"
cat data/ekus/asyncio_timeout_python.json | python -c "import sys,json; d=json.load(sys.stdin); print(d.get('technology_version','MISSING'))"
```
Expected: "3.11" — asyncio.timeout was introduced in Python 3.11.

---

## Task 2.3 — Knowledge Graph with Dependency Edges

File: agent/knowledge/knowledge_graph.py (create new)

Purpose: when EKU A changes, all EKUs that depend on A are marked potentially stale.

Storage: data/knowledge_graph.json

Key operations:
- add_edge(from_eku_id, to_eku_id): from_eku depends on to_eku
- get_dependents(eku_id): all EKUs that depend on this one
- propagate_stale(eku_id): mark all downstream EKUs as potentially stale
- auto_detect_edges(eku): parse how and failure_modes fields for mentions of other concept names

Auto-detection logic: if the text of EKU for list.append mentions "list" or "iterator", add dependency edges to those concept EKUs automatically.

Behavior check:
```bash
python -m agent knowledge-graph --show
```
Expected: Nodes and edges printed. After learning list.append and list.extend: dependency edge exists between them.

---

## Task 2.4 — Community Warning Cross-Reference

File: agent/modules/collector.py (add function)

Runs once per concept during learning. Searches for real-world gotchas that official docs do not mention. Searches: "{concept} {domain} gotcha", "{concept} {domain} bug site:github.com", "{concept} common mistakes".

Warning severities: critical (will cause production bugs), warning (will cause confusion), info (good to know).

When agent generates code using a concept with critical community warnings, it prepends a comment:
```python
# WARNING: {warning_text}
# Source: {evidence_url}
```

Behavior check:
```bash
python -m agent learn python "mutable default arguments"
cat data/ekus/mutable_default_arguments_python.json | python -c "import sys,json; d=json.load(sys.stdin); print(d.get('community_warnings','MISSING'))"
```
Expected: Non-empty list containing the well-known Python footgun about mutable defaults.

---

## Task 2.5 — Contradiction Detection on Every Write

File: agent/knowledge/eku_store.py (extend existing)

Contradiction patterns to check:
- "returns None" vs "returns the"
- "modifies in-place" vs "returns new"
- "thread-safe" vs "not thread-safe"
- "O(1)" vs "O(n)"
- "raises" vs "does not raise"
- "immutable" vs "mutable"
- "synchronous" vs "asynchronous"

Resolution: if confidence difference is more than 0.15, higher confidence wins. Otherwise flag both as DISPUTED for human review. Loser EKU gets confidence halved.

Behavior check:
```bash
python -m agent contradiction-scan
```
Expected: Any contradicting EKUs identified with specific fields that contradict and resolution applied.

---

## Task 2.6 — Structured JSON Prompts and Token Guard

File: agent/llm/helpers.py (extend existing)

```python
MAX_PROMPT_TOKENS = 3000

def structured_json_prompt(task: str, schema: dict) -> str:
    schema_str = json.dumps(schema, indent=2)
    return f"""{task}

You MUST respond with ONLY valid JSON matching this exact structure:
{schema_str}

Rules:
- Start your response with {{
- End your response with }}
- No text before or after the JSON
- Fill every field — use null if unknown, never omit a field"""

def truncate_to_token_limit(prompt: str) -> str:
    words = prompt.split()
    estimated_tokens = len(words) / 0.75
    if estimated_tokens <= MAX_PROMPT_TOKENS:
        return prompt
    max_words = int(MAX_PROMPT_TOKENS * 0.75)
    keep_start = int(max_words * 0.65)
    keep_end = int(max_words * 0.25)
    truncated = words[:keep_start] + ["[...CONTENT_TRUNCATED...]"] + words[-keep_end:]
    return " ".join(truncated)
```

Replace all LLM calls that expect JSON with structured_json_prompt(). This reduces JSON parse failures by 40 percent.

## Phase 2 Exit Criteria
1. Learn command works without hang on any common concept
2. Knowledge graph populated after learning related concepts
3. Contradicting EKUs flagged automatically on write
4. asyncio.timeout EKU has technology_version: "3.11"
5. All JSON-expecting LLM calls use structured_json_prompt()
6. Large prompts truncated from middle preserving start and end

## What agent can do after Phase 2
Learns with version awareness. Knows when knowledge contradicts other knowledge. Cross-references community warnings against official docs. Knowledge graph tracks what depends on what. No EKU accepted without version context.
Level: student who reads critically, not just passively.

---

# PHASE 2.5 — OPERATIONAL BRAIN LAYER
## Time: 4 hours
## Depends on: Phase 2 complete
## Purpose: Agent becomes self-aware about its own knowledge quality
## Most important phase. Skipping it means smart storage with dumb usage.

---

## Task 2.5.1 — Pattern Compiler (Tier 2 Auto-Derived)

File: agent/knowledge/pattern_compiler.py (create new)

A human does not remember 50 Python facts. They remember one pattern.
The pattern compiler derives these patterns automatically. You never write them manually.

Trigger: after every learn, after bulk seeding, daily at midnight, manually via CLI.

Algorithm:
1. Load all EKUs for a domain
2. Group EKUs by structural similarity using signals:
   - returns_none: "returns None", "in-place", "modifies"
   - raises_on_empty: "raises", "empty", "IndexError", "KeyError"
   - o_n_complexity: "O(n)", "linear", "traverses", "iterates"
   - o_1_complexity: "O(1)", "constant time", "hash"
   - thread_unsafe: "not thread-safe", "race condition", "shared state"
   - version_sensitive: "Changed in version", "New in version", "deprecated"
3. For each group of 5+ EKUs sharing a structural property:
   a. Extract the shared property
   b. Identify the class it applies to
   c. Generate a pattern statement
   d. Set pattern confidence = min(contributing EKU confidences)
   e. Store in data/patterns/{domain}_patterns.json

Example: list.append returns None + list.sort returns None + dict.update returns None + set.add returns None + list.reverse returns None → PATTERN: "Python mutation methods return None. Never assign their result."

Behavior check:
```bash
python -m agent compile-patterns --domain python
python -m agent status
```
Expected: KB Tier 2 count greater than 0. No manual pattern writing. All derived automatically.

---

## Task 2.5.2 — Heuristic Compiler (Tier 3 Auto-Derived)

File: agent/knowledge/heuristic_compiler.py (create new)

Derives decision rules from 3+ patterns. This is what separates senior engineers from junior engineers. Junior knows facts. Senior knows which fact to apply under which constraint.

Trigger: called by pattern compiler when 3+ patterns exist for a domain.

Algorithm:
1. Load all Tier 2 patterns for domain
2. Group patterns by decision context: performance, safety, readability, correctness, scalability
3. For each group of 3+ patterns about the same decision context:
   a. Extract the decision rule: "use X when Y because Z"
   b. Include counter-examples: "use X but NOT when Q"
   c. Set heuristic confidence = weighted average of pattern confidences
   d. Store in data/heuristics/{domain}_heuristics.json

Example from three patterns about mutation vs creation:
HEURISTIC: "In Python, mutate (append/sort/update) when: original should change, performance matters, no chaining needed. Create new (sorted/reversed/list()) when: original must be preserved, need to chain operations, passing to function without side effects."

Behavior check:
```bash
python -m agent heuristic-report --domain python
```
Expected: At least one heuristic with decision condition, choice made, reason given, counter-example. Not a vague generalization. A concrete decision rule.

---

## Task 2.5.3 — Confidence Cascade Tracker (CRITICAL)

File: agent/knowledge/confidence_cascade.py (create new)

Problem: Your system shows confidence 0.75 for a 5-step reasoning chain.
Real confidence: 0.75 to the power of 5 = 0.24.
You are showing 3x more confidence than reality. This causes subtle production failures.

Fix: Every multi-step reasoning chain tracks confidence as a running product.

Step types with different degradation rates:
- fact_lookup: multiply directly (you are only as confident as your source)
- inference: multiply by confidence to the power 1.2 (inference degrades faster)
- assumption: multiply by confidence squared (most dangerous)
- composition: use minimum confidence in chain

Independent corroborating evidence raises confidence: new_conf = 1 - (1-current)(1-evidence times 0.5)

Behavior check:
```bash
python -c "
from agent.knowledge.confidence_cascade import ConfidenceCascade, ReasoningStep
c = ConfidenceCascade()
c.add_step(ReasoningStep('a','step1',0.8,'fact_lookup'))
c.add_step(ReasoningStep('b','step2',0.8,'fact_lookup'))
c.add_step(ReasoningStep('c','step3',0.8,'fact_lookup'))
print(c.real_confidence)
"
```
Expected output: approximately 0.512. NOT 0.8. If 0.8 prints, cascade is broken.

---

## Task 2.5.4 — Execution Trace as First-Class Knowledge

File: agent/knowledge/execution_trace.py (create new)

Every execution regardless of pass or fail produces a trace stored in data/traces/.

Trace contains:
- task: what was attempted
- reasoning_path: list of steps considered and taken
- alternatives_rejected: other approaches considered and why rejected
- outcome: success or failure
- cascade_confidence: real confidence at each step
- duration_seconds: how long each step took
- eku_ids_consulted: which EKUs were used

When similar task arrives later, trace retrieval finds the closest past trace and uses its reasoning path as a starting template. The agent adapts the old reasoning to the new context. This is experience, not just knowledge.

Behavior check:
```bash
# After any task execution
ls data/traces/
cat data/traces/{most_recent}.json
```
Expected: JSON file with all trace fields. Readable as a reasoning narrative.

---

## Task 2.5.5 — Context Poison Detection

File: agent/knowledge/context_classifier.py (create new)

Problem: Agent learning from a codebase full of bugs and tech debt will learn wrong patterns as facts.

Fix: Every pattern learned from a codebase gets tagged CODEBASE_LOCAL. These patterns override canonical EKUs only in the current project. Never transfer to other projects.

Classification tags:
- CANONICAL: from official docs, high confidence, applies everywhere
- COMMUNITY_VALIDATED: from docs + community confirmation, applies everywhere
- CODEBASE_LOCAL: learned from specific project code, applies only to that project
- CROSS_PROJECT: appeared in 3+ separate projects, higher confidence than single-project

Detection: if a pattern contradicts a canonical EKU but is consistent within one specific codebase, tag it CODEBASE_LOCAL.

Behavior check:
```bash
# Learn from a codebase with non-standard patterns
python -m agent ask "how to handle X"
```
Expected: CODEBASE_LOCAL patterns do not appear without specifying the project. With project specified, they do appear.

---

## Task 2.5.6 — Cross-Adapter Knowledge Propagation

File: agent/knowledge/cross_adapter_propagator.py (create new)

When coding adapter learns "Redis TTL uses milliseconds not seconds", system design adapter automatically gets: "Unit semantics in Redis are version-dependent. Always verify at adapter boundary."

Propagation rules:
- Thread safety issues from coding → system design gets concurrency warning
- Performance complexity from coding → system design gets scale boundary note
- Framework-specific bugs from framework adapter → reasoning adapter gets known pitfall
- Security vulnerabilities from any adapter → all adapters get security awareness note

Every propagated hint has confidence = original confidence times 0.7 (abstraction loses precision).
Hints stored as CROSS_ADAPTER tagged EKUs.

Behavior check:
```bash
# Learn a thread-safety fact in coding adapter
python -m agent learn python "threading module"
# Check system design adapter knowledge
python -m agent ask "threading considerations for system design"
```
Expected: Cross-adapter hint about concurrency automatically present in system design knowledge.

---

## Task 2.5.7 — Action Candidate Competition Engine

File: agent/execution/engineer_protocol.py (create new — Gap 1)

Before any action, generate 2-3 options and score them.

Scoring formula: score = (confidence times impact) divided by cost
- confidence: cascade confidence from KB for this approach
- impact: estimated benefit toward the final goal
- cost: execution cost plus reversibility cost (low reversibility = high cost)

Agent always chooses highest-scoring option. Always logs why alternatives rejected. This converts the agent from reactive to strategic.

Additionally, this file implements the Engineer Pre-Task Protocol. Before every task, agent runs through this mental sequence and produces a Task Brief:
1. Goal: what exactly is the task asking for?
2. Constraints: what must not change, what must be preserved, what are the boundaries?
3. Unknowns: what do I not know that could affect this?
4. Risks: what could go wrong?
5. Minimum change: what is the smallest safe change that achieves the goal?
6. Verification plan: what will I check when done?

The Task Brief is stored per task and referenced throughout execution.

Behavior check:
```bash
python -m agent task "fix login error"
```
Expected before any execution begins:
```
[BRIEF] Goal: Fix login error in auth system
[BRIEF] Constraints: Must not change existing user sessions, Must not break registration flow
[BRIEF] Unknowns: Custom JWT middleware behavior — partial understanding
[BRIEF] Risks: Auth change affects all protected endpoints
[BRIEF] Min change: Identify specific failure point, fix only that
[BRIEF] Verification: Login works, registration still works, existing sessions unaffected
[CANDIDATES] Option A: Trace JWT validation failure (score: 0.82)
[CANDIDATES] Option B: Check auth middleware configuration (score: 0.71)
[CANDIDATES] Option C: Review user table constraints (score: 0.45)
[CHOSEN] Option A — proceeding
```

## Phase 2.5 Exit Criteria
1. Confidence cascade: three EKUs at 0.8 each produce chain confidence of approximately 0.512
2. data/traces/ has JSON files after any task
3. CODEBASE_LOCAL EKUs do not appear in general queries
4. Cross-adapter hint created when threading concept learned
5. Every task shows Task Brief before execution begins
6. Action candidates shown with scores before every action

## What agent can do after Phase 2.5
Self-aware about knowledge quality. Knows real vs displayed confidence. Remembers how it solved past problems. Shares insights across reasoning modes. Plans before acting. Chooses best approach from options.
Level: junior engineer who studies hard, knows their gaps, and thinks before acting.

---

# PHASE 3 — TASK EXECUTION ENGINE
## Time: 7 hours
## Depends on: Phase 2.5 complete
## Purpose: Agent can receive any task, plan it, execute it safely, verify it worked

---

## Task 3.1 — Task Decomposition Tree

File: agent/execution/decomposer.py (create new)

Large tasks broken into a Directed Acyclic Graph of subtasks ordered by dependency.

Each subtask has:
- id: unique identifier
- description: what this subtask does
- dependencies: list of subtask IDs that must complete first
- estimated_complexity: trivial / simple / moderate / complex
- adapter_hint: which adapter handles this
- reversibility_score: 0-10

Topological sort ensures dependency-correct execution order.

"Build user authentication system" decomposes to:
1. Design data model (system_design, no dependencies)
2. Create User model (coding, depends on 1)
3. Create UserRepository (coding, depends on 2)
4. Create AuthService with password hashing (coding, depends on 3)
5. Create AuthController with endpoints (coding, depends on 4)
6. Update security config (framework, depends on 5, reversibility: 3 — needs confirmation)
7. Create frontend login component (coding, depends on 5)
8. Wire frontend to backend (framework, depends on 6 and 7)

Behavior check:
```bash
python -m agent task "build user authentication system with JWT"
```
Expected: Decomposition tree printed showing all subtasks with dependencies. No subtask before its dependencies. Adapter assigned to each. Reversibility score shown.

---

## Task 3.2 — Estimation Engine (Gap 4)

File: agent/execution/estimation_engine.py (create new)

Before any task execution, agent estimates:
- Complexity: 1-10 scale based on: number of files touched, number of layers involved, presence of dangerous zones, unknowns detected
- Risk: low/medium/high/critical based on: reversibility of required actions, proximity to dangerous zones, whether architecture decision needed first
- Approach decision: needs design-first or can go straight to implementation

Design-first threshold: if system design adapter is needed AND task touches more than 3 service boundaries, system design adapter runs first and blocks coding adapter until architecture is approved.

Behavior check:
```bash
python -m agent estimate "add a new payment method to checkout flow"
```
Expected:
```
[ESTIMATE] Complexity: 8/10 (touches: payment, order, frontend, stripe integration)
[ESTIMATE] Risk: HIGH (payment is dangerous zone, irreversible external calls)
[ESTIMATE] Approach: DESIGN FIRST (touches 4+ service boundaries)
[ESTIMATE] Dangerous zones detected: payment_processor.py, stripe_client.py
[ESTIMATE] Architecture decision needed: yes — how to handle failed payment rollback
```

---

## Task 3.3 — Closed-Loop Execution Engine

File: agent/execution/closed_loop.py (create new)

This is the most important component in Phase 3.

Every action runs through this engine:
1. Break plan into atomic actions (smallest possible unit of change)
2. Before each action: set expectation from EKU expectation library
3. Execute action
4. Observe actual result
5. Compare expected vs actual
6. If match: proceed to next action
7. If mismatch: pause, re-evaluate using actual observation, revise remaining plan, continue

The plan is not a static script. It is a living document that changes as reality reveals itself.
Agent is never surprised at the end of a task because it reads reality at every step.

Behavior check:
```bash
python -m agent task "fix the null pointer error in UserService" --verbose
```
Expected in execution log:
```
[STEP 1] Action: Check UserService.java line 67
[STEP 1] Expected: Find null check missing before user.getId()
[STEP 1] Actual: Found null check missing AND user not extracted from security context
[STEP 1] MISMATCH — plan revision triggered
[REVISED PLAN] Two issues found, not one. Adding security context extraction as step 1a.
[STEP 1a] Action: Add security context extraction before line 67
[STEP 1a] Expected: User object populated from JWT token
[STEP 1a] Actual: User object populated correctly
[STEP 1a] MATCH — continuing
```

---

## Task 3.4 — Reversibility Scoring and Rollback Planner (Gap 9)

File: agent/execution/reversibility.py (create new)
File: agent/execution/rollback_planner.py (create new)

Reversibility scores:
- 0: Deleting production data — permanent
- 1: Dropping database column — structural permanent
- 2: Changing authentication logic
- 3: Database schema migration
- 4: Modifying core configuration
- 5: Changing existing business logic
- 6: Modifying an existing service method
- 7: Adding a new method to existing class
- 8: Adding a new file
- 9: Adding a new standalone utility
- 10: Running a read-only query or analysis

Actions scoring 0 to 3: require explicit confirmation before execution regardless of confidence.
Actions scoring 0 to 6: rollback plan must be created and stored before execution begins.

Rollback plan stored in data/rollback_plans/{task_id}.json
Contains: what will change, what the rollback steps are, what commands to run to verify rollback succeeded.

Behavior check:
```bash
python -m agent task "drop the old_sessions table from the database"
```
Expected:
```
[REVERSIBILITY] Score: 1 — DROP TABLE is irreversible
[ROLLBACK] Creating rollback plan before proceeding...
[ROLLBACK] Plan: dump table to backup before dropping, provide restore command
[ROLLBACK] Stored: data/rollback_plans/task_2026_03_30_001.json
[DANGEROUS ZONE] Database schema change requires confirmation.
[CONFIRM] I will: DROP TABLE old_sessions. Rollback plan exists.
[CONFIRM] Type 'confirm drop old_sessions' to proceed or 'cancel':
```

---

## Task 3.5 — Four Separate Practice Mechanisms

File: agent/adapters/coding_adapter.py — sandbox execution
File: agent/adapters/framework_adapter.py — minimal working example
File: agent/adapters/system_design_adapter.py — self-critique loop
File: agent/adapters/reasoning_adapter.py — chain validation

Coding adapter practice: code runs in sandbox, actual output compared against expected from EKU.
Framework adapter practice: build smallest possible working example using this concept alone. Verify it follows framework conventions for current version.
System design adapter practice: generate architecture decision, adversarially critique it using trade-off heuristics from KB, score on five dimensions (correctness, scalability, maintainability, security, simplicity), store result.
Reasoning adapter practice: produce reasoning chain, verify each step's premise is supported by KB, check for logical fallacies (circular reasoning, affirming the consequent, false dichotomy).

Behavior check:
```bash
python -m agent practice --adapter system_design --concept "microservices vs monolith"
```
Expected: Architecture generated. Adversarial critique printed. Score across five dimensions shown. No sandbox involved. Self-critique loop visible.

---

## Task 3.6 — Failure Taxonomy Engine (All Ten Types)

File: agent/execution/failure_classifier.py (create new)

Every failure classified into exactly one of ten types. Each type updates a different EKU field.

Type 1 SyntaxError: how field incorrect. Update how field.
Type 2 NameError or ImportError: prerequisite missing. Update how field prerequisites and failure_modes.
Type 3 AttributeError or TypeError: wrong context usage. Update when_to_use constraints and failure_modes.
Type 4 RuntimeError or ValueError: valid input causing unexpected failure. Add specific input pattern to failure_modes.
Type 5 TimeoutError or MemoryError: scale characteristic missing. Trigger heuristic compiler. Add performance boundary to failure_modes.
Type 6 AssertionError in composition: two individually correct EKUs incompatible when combined. Register composition hazard. Add warning to both EKUs.
Type 7 Logical failure — wrong output no exception: what field behavior description inaccurate. Update what field.
Type 8 Environmental failure — works in one env fails in another: add environment dependency field.
Type 9 Flaky failure — passes sometimes fails sometimes: flag EKU as non-deterministic. Increase fuzz testing. Check concurrency hazard.
Type 10 Security failure — functionally correct but creates vulnerability: add to hazard registry. Add security requirements to how field.

Behavior check:
```bash
python -m agent failure-taxonomy-report
```
Expected: Every recorded failure listed with type from the ten types. EKU field updated shown. Zero failures listed as just "failed".

---

## Task 3.7 — Preemptive Failure Injection

File: agent/execution/preemptive_check.py (create new)

Before executing any plan, agent red-teams its own plan using the failure library.

For every step in the plan, agent queries: have tasks similar to this step failed before, and if so, under what conditions?

If failure library shows this type of step has failed three or more times, agent adjusts plan to address the known failure condition before starting.

This prevents the entire class of foreseeable failures.

Behavior check:
After building failure library through practice, give agent a task that involves a step that has failed before.
Expected:
```
[PREEMPTIVE] Step 3: Add endpoint to controller
[PREEMPTIVE] Failure library: similar steps failed 3x — all due to missing security config update
[PREEMPTIVE] Adding preventive step 3a: update security config before adding endpoint
```

---

## Task 3.8 — Stacking Bug Prevention

File: agent/execution/composition_verifier.py (create new)

When multiple fixes applied to same file sequentially, each may be individually correct but their composition breaks something.

After each fix applied to a file: re-run ALL previous test assertions for that file, not just tests for the new fix.

Behavior check:
Apply two fixes to same file in sequence. After second fix, composition verifier re-runs all tests that touched this file. Any test passing after fix 1 but failing after fix 2 caught and reported before task marked complete.

---

## Task 3.9 — Progress Validation Signal

File: agent/execution/progress_validator.py (create new)

Every three atomic actions, measure progress on three dimensions:
- Technical: tests passing more than before, errors fewer, output closer to correct
- Directional: understanding of problem improving, same question not recurring
- Efficiency: each action producing meaningful change, not becoming smaller and less impactful

If progress stalls on any dimension for three consecutive measurements: change strategy. Not the goal. The approach.

Behavior check:
Create scenario where agent gets stuck making same failing change repeatedly.
Expected:
```
[PROGRESS] Step 6: Technical dimension stalled. Same error appearing for 3 consecutive steps.
[PROGRESS] Switching strategy. Previous approach: fixing null check. New approach: tracing call chain from entry point.
```

---

## Task 3.10 — Minimum Change Principle Enforcer

File: agent/execution/minimum_change.py (create new)

Before any plan executes, review it: is every action necessary? Is there a smaller change achieving the same result?

Scope creep prevention: if agent notices other issues during execution, it does NOT fix them. It logs them to PMM observation queue and continues with original task only.

A real senior engineer fixes what they were asked to fix and logs other issues for later.

Behavior check:
Present task with large-scope and small-scope solution available. Agent should choose small-scope.
Any unrelated issues noticed should appear in PMM observation log, not as additional actions.

---

## Task 3.11 — Test Generator from KB (Gap 7)

File: agent/engineer/test_generator.py (create new)

Generates tests from three sources, not just "write tests for this function":

Source 1 — EKU failure_modes: every documented failure mode in the relevant EKU becomes a test case. If EKU for list.append says "fails when list is None", generate test for None input.

Source 2 — Failure library: every past failure involving the technology or pattern being tested becomes a test case. History of failures becomes test suite.

Source 3 — Business rule invariants: extract if-statements with business-significant conditions (thresholds, limits, roles, states) and generate tests that verify these invariants hold. This prevents semantic regressions.

Behavior check:
```bash
python -m agent generate-tests --file src/services/UserService.java
```
Expected: Tests generated from all three sources with source labeled for each test. Not generic happy-path tests. Tests specifically targeting known failure modes, past failures, and business invariants.

---

## Phase 3 Exit Criteria
1. Task decomposition: "build auth system" produces subtask tree ordered by dependency
2. Estimation engine: "add payment method" produces correct complexity and risk assessment
3. Closed loop: multi-step task shows expected vs actual comparison at every step with plan revisions visible
4. Reversibility: action scoring 0-3 stops for confirmation with rollback plan created
5. Four practice mechanisms: coding uses sandbox, system design uses critique loop
6. Failure taxonomy: every recorded failure has one of ten types
7. Preemptive check: task with previously-failed pattern adds preventive measure
8. Stacking bug: two sequential fixes to same file triggers re-run of all file assertions
9. Progress validation: stuck scenario triggers strategy change after three stalls
10. Test generator: generates tests from EKU failure_modes and failure library

## What agent can do after Phase 3
Receives any task. Estimates complexity and risk. Creates Task Brief before touching anything.
Decomposes into ordered subtasks. Executes with closed-loop correction. Creates rollback plans.
Prevents foreseeable failures. Never takes irreversible actions without confirmation.
Generates tests from KB knowledge not generic templates.
Level: careful mid-level engineer who thinks before acting, catches most mistakes early.

---

# PHASE 4 — PROJECT INTELLIGENCE (PMM + ONBOARDING)
## Time: 6 hours
## Depends on: Phase 3 complete
## Purpose: Agent understands projects as completely as a senior engineer who has worked on them

---

## Task 4.1 — Project Onboarding Process (Gap 2)

File: agent/project_memory/onboarding.py (create new)

A real engineer on day one does not just scan files. They build a mental model of the system.

Onboarding process produces a Project Brief stored in data/project_memory/{project}/brief.json

Brief contains:
- system_purpose: what this system is supposed to do (derived from README, main entry points, API routes)
- users: who uses this system (derived from auth patterns, role names, user-facing endpoints)
- invariants: things that must never be violated (derived from validation code, business rule comments, critical error handling)
- known_problems: issues the team lives with (derived from TODO, FIXME, hack comments)
- recent_changes: what changed recently (derived from git patterns if available, or comment timestamps)
- architecture_style: the dominant pattern (MVC, layered, hexagonal, event-driven — detected from structure)
- technology_stack: exact versions of every technology detected

Before any task on a project, agent reads the Project Brief first. The brief informs every decision.

Behavior check:
```bash
python -m agent onboard --project /path/to/project
cat data/project_memory/{project_name}/brief.json
```
Expected: All brief fields populated. system_purpose accurately describes the project. invariants list extracted from actual validation code. known_problems list extracted from TODO and FIXME comments.

---

## Task 4.2 — Deep Project Scanner

File: agent/project_memory/pmm.py (create new)

Reads every file. Classifies each by role using multiple signals: file location, file name, annotations, import patterns, class declaration patterns.

For SpringBoot: @RestController → controller, @Service → service, @Repository → repository, @Configuration → config, @Entity → model.
For Angular: @Component → component, @Injectable → service, @NgModule → module, CanActivate implementation → guard, HttpInterceptor → interceptor.
For FastAPI: APIRouter → router, BaseModel subclass → schema, Depends → dependency.

Also identifies: test files and what they test, migration files and what schema state they represent, configuration files per environment, utility classes, dead code with comments.

Behavior check:
```bash
python -m agent scan --project /path/to/project
```
Expected: Every file listed with classified role. Zero files listed as unknown for any standard framework convention. Classification accuracy verifiable by checking any ten files manually.

---

## Task 4.3 — Dependency Graph Builder

Reads every import in every file. Builds complete directed graph with edge types: uses, extends, implements, injects, instantiates.

Computes per file:
- in_degree: how many things depend on this file
- out_degree: how many things this file depends on
- betweenness: how many paths pass through this file (high betweenness = hub = high risk)

Identifies problematic patterns: circular dependencies (flag as architectural issue), god classes with too many dependents (flag for observation queue), deep inheritance chains (flag for observation queue).

---

## Task 4.4 — Risk Zone Classification

Derived from dependency graph.

Critical: more than 20 direct dependents or on critical path of 3+ major flows. Agent requires explicit confirmation before touching. Even for seemingly simple changes.
High: 10 to 20 direct dependents. Significant caution. Agent plans changes to minimize cascade.
Medium: 3 to 10 direct dependents. Normal caution. Verify affected dependents after change.
Low: fewer than 3 direct dependents. Standard verification.

Risk zones recalculated after every change.

---

## Task 4.5 — Request Flow Mapping

Traces every major request flow end to end.

For web apps: HTTP request arrives → middleware → controller → service → repository → database → response.

Records at each step: component name, what it receives, what it does, what it passes to next step, error handling branches.

These flows are used by the behavioral diff engine and the change impact analyzer.

---

## Task 4.6 — Tribal Knowledge Extractor

Reads every comment in the codebase. Every TODO and FIXME. Every unusual code pattern. Every magic number. Every workaround.

Derives tribal knowledge: things not written in any document but true about this specific project.
- Known issues that are tolerated
- Workarounds for third-party bugs
- Business rules encoded in code without documentation
- Historical decisions preserved for compatibility

Stores with confidence levels: high confidence from explicit comments, medium from code patterns, low from unusual approaches without explanation.

---

## Task 4.7 — Architecture Smell Detector (Gap 10)

File: agent/project_memory/architecture_smell_detector.py (create new)

Runs during onboarding and periodically. Reports to PMM observation queue. Never fixes without being asked.

Smells detected:
- God service: single service with more than 15 public methods and dependencies on 5+ other services
- Circular dependency: module A imports B which imports A
- Layer violation: repository talking directly to controller, or controller talking directly to database
- Missing abstraction: same pattern repeated 3+ times without extracting to shared utility
- Shotgun surgery: one business concept change requires touching 7+ files
- Feature envy: method that uses data from another class more than its own class
- Divergent change: one class changed for many different reasons across recent history

Behavior check:
```bash
python -m agent architecture-smells --project /path/to/project
```
Expected: Smells listed with specific files, why the smell exists, potential impact. Zero auto-fixes. All in observation queue only.

---

## Task 4.8 — Documentation Trust Engine (Gap 8)

File: agent/project_memory/documentation_trust_engine.py (create new)

Code wins over docs when they conflict. Always.

Process when reading docs alongside code:
1. Extract claims from documentation
2. Find corresponding code
3. If docs claim X and code does Y: flag as doc/code mismatch, trust code, add to tribal knowledge
4. If docs describe behavior that has no corresponding code: flag as phantom documentation
5. If code does something docs do not mention: extract as undocumented behavior, add to tribal knowledge

Behavior check:
After onboarding to a project where docs and code have minor inconsistencies:
```bash
python -m agent doc-trust-report --project /path/to/project
```
Expected: Mismatches listed. Code behavior documented as authoritative. Phantom docs flagged. Undocumented behaviors captured.

---

## Task 4.9 — Change Impact Analyzer

Before any file is modified, produces complete impact assessment:
- Files that directly depend on the target file
- Files that transitively depend on target file up to 3 levels deep
- Flows that pass through target file
- Risk level of proposed change
- Minimum verification steps after change
- Tribal knowledge associated with target file
- Known issues from failure library for this file

Behavior check:
```bash
python -m agent impact --project project-name --file src/services/UserService.java
```
Expected: Complete assessment with all components. Every dependent file listed. Every affected flow listed. Risk level with justification. Tribal knowledge shown if any.

---

## Task 4.10 — Behavioral Diff Engine with Semantic Check

Two diff modes running together after every change.

Structural diff: check that code structure and call paths are as expected.

Semantic diff: extract business rules as testable assertions BEFORE any change. Re-run after change. Any assertion that fails is a semantic regression.

Business rules extracted from:
- if statements with business-significant threshold values
- validation constraints
- pricing and fee calculations
- role and permission checks
- state machine transitions

This catches the change that looks structurally correct but breaks a business rule. Threshold going from 5000 to 50000 looks identical structurally. Semantic diff catches it.

Behavior check:
Introduce a change that breaks a business rule but looks structurally correct.
Expected: Semantic diff catches it. Structural diff does not. This proves they are different checks.

---

## Task 4.11 — Code Reviewer Mode (Gap 3)

File: agent/engineer/code_reviewer.py (create new)

Before touching any area of code, agent runs a code review of that area using senior engineer heuristics.

Review checks:
- Concurrency: any shared mutable state accessed without synchronization?
- Null safety: every external input checked for null/None before use?
- Error handling: every I/O operation and external call has error handling?
- SQL injection: any database query built with string concatenation?
- Authentication: every sensitive endpoint has auth check?
- Scale risk: any loop over unbounded collection without pagination or limit?
- Hardcoded values: any magic numbers or hardcoded strings that should be config?
- Logging: any sensitive data (passwords, tokens, PII) in log statements?
- Resource leaks: every opened resource (file, connection, stream) closed in finally or context manager?

Review produces a report before implementation begins. Critical findings block implementation until addressed. High findings are fixed as part of the task. Medium and low findings go to observation queue.

Behavior check:
```bash
python -m agent review --file src/controllers/UserController.java
```
Expected: Review report with findings by severity. Critical findings if any with specific location and fix recommendation. Observation queue updated with medium and low findings.

---

## Phase 4 Exit Criteria
1. Onboarding: Project Brief produced with all fields for any standard project
2. Scanner: Every file correctly classified by role, zero unknowns for standard frameworks
3. Architecture smells: God service and circular dependency detected in test project
4. Doc trust engine: Code/doc mismatch flagged, code treated as authoritative
5. Behavioral diff: Semantic regression caught that structural diff misses
6. Code reviewer: Runs before any implementation, critical findings block execution
7. Change impact: Complete impact assessment for any modified file

## What agent can do after Phase 4
Understands any project as a senior engineer who has worked on it for months.
Knows the architecture, risk zones, tribal knowledge, invariants, and known problems.
Reviews code before touching it. Catches semantic regressions. Detects architectural debt.
Level: senior engineer joining a new project — reads everything before writing anything.

---

# PHASE 5 — MULTI-LANGUAGE AND DEPENDENCY INTELLIGENCE
## Time: 5 hours
## Depends on: Phase 4 complete
## Purpose: Works in any language, handles dependency complexity

---

## Task 5.1 — Language Detection and Registry

File: agent/adapters/language_detector.py (create new)
File: agent/adapters/language_registry.py (create new)

Five language adapters: Python, JavaScript, TypeScript, Java, Go.

Detection signals: file extensions, import syntax, package manager files (package.json, pom.xml, go.mod, requirements.txt, Gemfile), build configuration, annotation patterns.

Each language adapter knows:
- How to execute code in sandbox (different command per language)
- How to parse error messages (each language has different format)
- How to detect version from project files
- What the common failure patterns are for this language
- What the standard project structure looks like

Each language has its own EKU namespace. Python EKUs and Java EKUs stored separately. Cross-language concepts use bridge layer.

Behavior check:
```bash
python -m agent detect-language --project /path/to/java-project
```
Expected: Primary language Java detected with confidence. Version from pom.xml shown. Framework (SpringBoot) detected. No mixing with Python EKUs.

---

## Task 5.2 — Cross-Language Concept Bridge

File: agent/knowledge/cross_language_bridge.py (create new)

Universal concepts that exist in all languages but expressed differently:
- Null pointer equivalent: NullPointerException (Java), AttributeError None (Python), TypeError undefined (JS), nil pointer (Go)
- Off-by-one: exists in all languages
- Concurrency hazards: exists in all languages with different primitives
- Algorithm complexity: language-independent concepts

When agent learns Python concurrency hazards, it auto-derives Java concurrency hint at 0.7 confidence. Not specific Java syntax. General principle about shared mutable state.

Behavior check:
Learn Python threading module. Ask about Java concurrency without explicitly teaching Java threading.
Expected: Agent derives Java concurrency hint from cross-language bridge at lower confidence, clearly labeled as derived not directly learned.

---

## Task 5.3 — Dependency Conflict Analyzer (Gap 5)

File: agent/knowledge/dependency_conflict_analyzer.py (create new)

Before any dependency change (adding, upgrading, removing), runs a transitive dependency analysis.

Process:
1. Parse dependency file (package.json, pom.xml, requirements.txt, go.mod)
2. Build full transitive dependency tree for current state
3. Simulate the proposed change
4. Build transitive dependency tree for proposed state
5. Detect conflicts: two packages requiring incompatible versions of a shared dependency
6. Detect peer dependency violations
7. Detect deprecated packages with known security issues
8. Report all conflicts before any change is made

Behavior check:
```bash
python -m agent check-deps --project /path/to/project --upgrade requests==2.32.0
```
Expected: Full analysis of what changing requests to 2.32.0 would affect. Any transitive conflicts listed. Security issues in new version if any. Safe to proceed or specific conflicts to resolve first.

---

## Task 5.4 — Migration Safety Analyzer (Gap 6)

File: agent/engineer/migration_safety_analyzer.py (create new)

Every schema migration classified before execution.

Classifications:
- SAFE_LIVE: adding a nullable column, adding an index, adding a new table — can run in production without downtime
- REQUIRES_WINDOW: adding a NOT NULL column without default, changing a column type, dropping an index — requires maintenance window
- REQUIRES_BACKFILL: adding a NOT NULL column to table with existing data — need to backfill before applying constraint
- REQUIRES_ROLLBACK_PLAN: dropping a column, dropping a table, removing a constraint — always need rollback plan documented before proceeding
- DANGEROUS_CONCURRENT: adding an index without CONCURRENTLY on PostgreSQL, or equivalent — will lock table

For each migration file, agent produces:
- Classification with reason
- What the rollback migration is
- What data validation queries to run before and after
- Estimated impact on table size and query performance

Behavior check:
```bash
python -m agent analyze-migration --file db/migrations/V20260330_add_user_status.sql
```
Expected: Classification shown with reason. If REQUIRES_BACKFILL, exact backfill steps shown. Rollback migration generated. Data validation queries provided.

---

## Phase 5 Exit Criteria
1. Language detection correctly identifies primary language for any of the five supported
2. Java EKUs and Python EKUs stored in separate namespaces, never mixed
3. Cross-language bridge derives Java concurrency hint from Python threading learning
4. Dependency conflict analyzer detects transitive conflicts before any change
5. Migration safety analyzer correctly classifies safe vs dangerous migrations

## What agent can do after Phase 5
Works on any project in Python, JavaScript, TypeScript, Java, or Go.
Analyzes dependency changes before they cause problems.
Classifies schema migrations by safety level before executing.
Works on full-stack projects with multiple languages simultaneously.
Level: polyglot senior engineer who checks dependencies and migration safety automatically.

---

# PHASE 6 — ADVERSARIAL TESTING AND QUALITY ASSURANCE
## Time: 5 hours
## Depends on: Phase 5 complete
## Purpose: Agent challenges its own success, catches false positives, ensures real quality

---

## Task 6.1 — Adversarial Self-Testing

File: agent/testing/adversarial_tester.py (create new)

After any successful execution, agent asks: how could this still be wrong?

Generates test cases designed to break the just-completed work:
- Empty inputs for every parameter
- Maximum size inputs
- Wrong type inputs
- Null/None inputs
- Concurrent access scenarios
- Network failure scenarios for external calls
- Database error scenarios for DB calls

If adversarial tests find a failure that original tests did not catch, task is marked incomplete and failure added to failure library.

Behavior check:
```bash
python -m agent adversarial-test --last-task
```
Expected: Adversarial test cases generated and run. Any failures found reported with specific what was tested and what failed.

---

## Task 6.2 — False Positive Success Detector

File: agent/testing/false_positive_detector.py (create new)

Three categories of false success:

Category 1 — Untested edge case: after every task, check if tests cover edge cases from EKU failure_modes. If EKU says "fails on empty input" and no test for empty input exists, flag it.

Category 2 — Wrong output logic: verify output against business rules, not just absence of exceptions. Code can return 200 OK and still be wrong.

Category 3 — Scale risk: check if any operation in the task has a performance EKU warning. Unbounded loops, N+1 queries, missing pagination — flag the scale risk even if it works fine now.

Behavior check:
Complete a task without testing edge cases documented in EKU failure_modes.
Expected:
```
[FALSE_POSITIVE] Success claimed but EKU failure_modes not covered by tests
[FALSE_POSITIVE] Specifically: empty input case not tested for UserRepository.findByEmail()
[FALSE_POSITIVE] Add test: test_find_by_email_empty_string_returns_none()
```

---

## Task 6.3 — Semantic Behavioral Diff

File: agent/testing/semantic_diff.py (create new)

Extracts business rules as testable assertions before any change. Re-runs after any change.

Business rules extracted from:
- if statements with numeric thresholds: "if order_total > 5000: free_shipping"
- role checks: "if user.role == 'ADMIN': allow"
- state machine transitions: valid_next_states dictionary
- validation constraints: field validators with specific limits

Each extracted rule becomes an assertion. Before change: collect assertions. After change: run assertions. Any assertion failure = semantic regression regardless of whether tests pass.

Behavior check:
Introduce a change that modifies a business threshold silently.
Semantic diff must catch it. Structural diff must not. Both run and results show the difference.

---

## Task 6.4 — Fragility Tracker

File: agent/testing/fragility_tracker.py (create new)

Files that change frequently are fragile. Calculated as: change_count divided by session_count.

High fragility files (score above 0.5) automatically get shadow tests: additional tests verifying their behavior has not changed in unexpected ways.

Shadow tests are generated from the file's current behavior, not from documentation. They capture what the code actually does and alert when it changes.

Behavior check:
```bash
python -m agent fragility-report --project project-name
```
Expected: Files listed with fragility scores. High-fragility files highlighted. Shadow tests generated for top five most fragile files.

---

## Task 6.5 — Project Personality Calibration

File: agent/adapters/personality_detector.py (create new)

Detects project personality from:
- Test coverage percentage (below 40: startup, 40-70: balanced, above 70: enterprise)
- Type annotation percentage
- Error handling density (how many try-catch per 100 lines)
- Security annotation presence
- CI configuration strictness
- Comment density and quality

Startup profile: faster pragmatic solutions, documents tech debt without blocking, simpler patterns.
Balanced profile: balances speed and quality, code review ready without excessive cycles.
Enterprise profile: fully defensive, validates every input, handles every error, adds security checks, never experimental patterns, higher confidence threshold before acting.

Behavior check:
Run same task on startup project and enterprise project.
Expected: Enterprise implementation has measurably more null checks, explicit error handling, logging, and input validation. Both correct but enterprise is more defensive.

---

## Phase 6 Exit Criteria
1. Adversarial tests auto-run after every completed task
2. False positive detector catches untested EKU failure_modes
3. Semantic diff catches business rule change that structural diff misses
4. Fragility report shows scores with shadow tests for high-fragility files
5. Same task produces different implementations on startup vs enterprise project

## What agent can do after Phase 6
Does not accept its own success at face value.
Challenges every completed task with adversarial tests.
Detects false success from untested edge cases, wrong logic, and scale risks.
Catches semantic regressions no structural check would find.
Calibrates its behavior to match the project's risk profile.
Level: senior engineer who writes tests for their own code and does not trust first-pass success.

---

# PHASE 7 — KNOWLEDGE LIFECYCLE AND SEMANTIC SEARCH
## Time: 5 hours
## Depends on: Phase 6 complete
## Purpose: KB stays accurate and fresh automatically. Agent finds knowledge from any phrasing.

---

## Task 7.1 — ChromaDB Semantic Search

File: agent/knowledge/vector_store.py (replace existing stub)

Every EKU embedded and stored in ChromaDB at write time.
Embedding uses: concept name + what field + first three verified facts concatenated.
One ChromaDB collection per domain.

When query arrives:
1. Exact match search first (BM25-style keyword matching)
2. Semantic search adds results exact match missed
3. Results ranked by weighted combination (exact match weight 0.6, semantic weight 0.4)

Behavior check:
```bash
python -m agent ask "how do I grow a collection in python"
```
Expected: list.append EKU retrieved via semantic similarity. No word in query matches EKU name exactly. Response shows both semantic score and exact score separately.

---

## Task 7.2 — Fine-Grained Confidence Decay

File: agent/knowledge/decay_scheduler.py (create new)

Different knowledge categories decay at different rates per day:
- Python core syntax (list.append, for loops): 0.0001 per day — almost never changes
- Python standard library: 0.001 per day
- Third-party packages: 0.005 per day
- Framework patterns: 0.01 per day
- Security patterns: 0.02 per day — must stay current, exploits evolve fast
- Cloud provider APIs: 0.015 per day

Decay runs nightly. Confidence floor: 0.1 — never zero but triggers re-verification when below 0.4.

Behavior check:
```bash
python -m agent decay-report --technology react
```
Expected: React EKUs show higher decay rates than Python core EKUs. Any EKU below 0.4 confidence flagged for re-verification.

---

## Task 7.3 — Dead Knowledge Detection

File: agent/knowledge/dead_knowledge.py (create new)

Tracks applied_count per EKU (how many times used in actual task execution).

An EKU with applied_count of 0 after 50 task execution opportunities is suspect.
It might be wrong, over-specific, or a hallucination from extraction.

After 50 missed opportunities: confidence halved, tagged SUSPECT.
After another 50 missed opportunities: tagged QUARANTINED, removed from active retrieval.
Quarantined EKUs are not deleted. Human can review and rehabilitate.

Behavior check:
Create an EKU artificially. Execute 50 tasks without using it.
```bash
python -m agent dead-knowledge-report
```
Expected: Unused EKU shown as SUSPECT with confidence halved.

---

## Task 7.4 — Background Verification Queue

File: agent/knowledge/verification_queue.py (create new)

Runs every 24 hours automatically. EKUs not verified in last 24 hours are queued.

Priority: lowest confidence first, then longest since last verification, then highest decay rate.

For each EKU in queue: canonical test, edge case test, mutation behavior test, fuzz test. Update confidence using four-component formula. Apply auto-fix if specific field found wrong. Re-run contradiction check after any fix.

Behavior check:
```bash
python -m agent verification-queue
```
Expected: List of EKUs scheduled with priority order and reason for each position. Queue non-empty if knowledge exists.

---

## Phase 7 Exit Criteria
1. Semantic query for paraphrased concept retrieves correct EKU
2. Decay report shows different rates for core vs framework vs security EKUs
3. Dead knowledge detection flags EKU with zero applications after 50 opportunities
4. Verification queue running automatically with priority ordering

## What agent can do after Phase 7
Finds knowledge even when user describes the problem in their own words.
KB stays accurate without human intervention.
Old stale knowledge loses confidence over time.
Unused knowledge is detected and quarantined.
Level: senior engineer whose knowledge is always current and self-organizing.

---

# PHASE 8 — SELF-IMPROVEMENT SYSTEMS
## Time: 4 hours
## Depends on: Phase 7 complete
## Purpose: Agent gets systematically smarter from its own history

---

## Task 8.1 — Assessment Error Log

File: agent/self_improvement/assessment_error_log.py (create new)

Every time agent makes an initial assessment of a task and discovers during execution that the assessment was wrong, this gap is recorded.

Record: initial assessment, evidence that supported it, what reality turned out to be, evidence that revealed the correct answer, type of reasoning error:
- incomplete_information: agent did not have enough data to make correct assessment
- wrong_pattern_match: agent matched the wrong pattern to the situation
- ignored_signal: evidence was visible but not weighted correctly
- overconfident_classification: agent was too certain about an uncertain classification
- version_confusion: agent applied knowledge from wrong version
- context_mismatch: agent applied canonical knowledge where CODEBASE_LOCAL applied

Behavior check:
```bash
python -m agent assessment-errors --last 20
```
Expected: Wrong initial assessments listed with gap between claimed and found. Error type shown for each. Systematic patterns highlighted if any error type appears 3+ times.

---

## Task 8.2 — Systematic Bias Detection and Correction

File: agent/self_improvement/bias_detector.py (create new)

Weekly analysis of assessment error log. Any reasoning error type appearing 3+ times in one week is a systematic bias. The classifier responsible gets updated to weight the signals that revealed the truth more heavily.

Over time agent becomes measurably less likely to make the same type of wrong assessment.

Behavior check:
```bash
python -m agent reasoning-quality-report --last 30-days
```
Expected: Error types listed with frequency. Classifier updates applied shown. Month-over-month improvement in recurring error types visible.

---

## Task 8.3 — Cross-Project Pattern Learning

File: agent/self_improvement/cross_project_learner.py (create new)

When agent works on 3+ projects using same technology stack, patterns appearing in all three are elevated to CROSS_PROJECT confidence tier. They feed into Tier 2 and Tier 3 KB as high-confidence entries.

A pattern seen in ten different Angular projects is not a project quirk. It is a real Angular pattern. Higher confidence than anything learned from docs alone.

Behavior check:
Work on three different Angular projects.
```bash
python -m agent cross-project-patterns --technology Angular
```
Expected: Patterns common to all three projects listed with elevated confidence. Patterns only in one project not elevated.

---

## Phase 8 Exit Criteria
1. Assessment error log records wrong initial assessments with reasoning error type
2. Systematic bias detection identifies error type appearing 3+ times per week
3. Classifier update applied after systematic bias detected
4. Cross-project patterns elevated after appearing in 3+ projects

## What agent can do after Phase 8
Gets systematically smarter from its own mistakes. Not just accumulating knowledge. Improving reasoning patterns. Diagnostic accuracy for recurring problem classes improves week over week.
Level: engineer whose instincts sharpen with experience, not just knowledge.

---

# PHASE 9 — PRODUCTION HARDENING
## Time: 4 hours
## Depends on: All previous phases complete
## Purpose: Safe and reliable enough for real projects without supervision

---

## Task 9.1 — Full Health Check System

File: agent/health_check.py (create new)

Run before every session. Checks:
- GPU available and in use (ollama ps shows GPU memory greater than 0)
- Ollama responds within 10 seconds
- KB accessible and not corrupted
- ChromaDB accessible
- All required config values present in environment
- No EKUs in corrupted state (validate JSON for every file in data/ekus/)
- No open file locks from crashed previous session
- data/ directory structure complete

Any health check failure produces specific error message with exact fix steps.

Behavior check:
```bash
python -m agent health-check
```
Expected: Every check listed with pass or fail. Failures show specific commands to fix. Green on all checks required before task execution.

---

## Task 9.2 — Dangerous Zone Guard

File: agent/senior/dangerous_zone_guard.py (create new)

Identifies dangerous zones from code signals:
- JWT handling, bcrypt, auth middleware → authentication logic
- Stripe, PayPal, payment APIs, price calculations → payment processing
- Migration files, ALTER TABLE, DROP → schema migration
- .env access, os.environ, secret managers → secret management
- Encryption/decryption functions, private keys → cryptography

Any task touching a dangerous zone:
1. Identify the dangerous zone
2. Explain what was found and what change is intended
3. Request explicit human confirmation
4. Wait for confirmation
5. Only after confirmation proceed

Hard rule. No exceptions. No confidence score overrides this.

Behavior check:
Give agent task that touches authentication.
Expected: Stops, prints dangerous zone warning, describes intended change, waits for confirmation. --auto-confirm flag must not bypass this.

---

## Task 9.3 — Session Recovery

File: agent/execution/session_recovery.py (create new)

On crash: save completed subtasks, current file states, what was in progress.
On restart: detect interrupted session, report what was in progress.
Options presented: resume from where stopped, roll back all changes, start fresh.

Behavior check:
Kill agent mid-task. Start new session.
Expected: "Interrupted task detected. Completed 4 of 8 subtasks. Options: resume / rollback / fresh start?"

---

## Phase 9 Exit Criteria
1. Health check passes on clean environment
2. Health check fails with specific error when GPU not available
3. Dangerous zone task stops for confirmation and cannot be bypassed
4. Interrupted session detected on next startup with recovery options

## What agent can do after Phase 9
Safe for real projects. Never takes irreversible dangerous actions autonomously. Recovers from crashes. Validates own health before every session. Trustworthy.
Level: engineer you can trust to work on your codebase without supervision for low and medium risk tasks.

---

# PHASE 10 — SENIOR ENGINEER LAYER
## Time: 6 hours
## Depends on: Phase 9 complete
## Purpose: Full senior engineer capability. Orchestrates all layers with wisdom.

---

## Task 10.1 — Unknown-Unknown Detector

File: agent/senior/unknown_unknown_detector.py (create new)

Before starting any task, agent declares its uncertainty boundary explicitly.

Reads the project. Classifies components:
- UNDERSTOOD: agent has high-confidence KB coverage for this component
- PARTIAL: agent has some knowledge but gaps exist for this specific project's usage
- CANNOT_ASSESS: component uses patterns, libraries, or conventions agent cannot evaluate

For CANNOT_ASSESS components: agent explicitly refuses to touch until given an explanation.
This is not a knowledge gap (missing KB entry). This is the agent knowing it cannot assess what it cannot assess.

Behavior check:
Point agent at project with custom undocumented non-standard component.
Expected:
```
[UNCERTAINTY] CANNOT ASSESS: custom_auth_middleware.py
[UNCERTAINTY] Reason: Uses non-standard session management pattern not in KB or recognizable conventions
[UNCERTAINTY] Action: I will not touch anything connected to this component until you explain how it works.
[UNCERTAINTY] Components I do understand: UserController, UserService, UserRepository
```

---

## Task 10.2 — Meta-Adapter Orchestration

File: agent/senior/meta_adapter.py (create new)

Orchestrates interaction between the four adapters.

Rules enforced:
- System design adapter must approve architecture before coding adapter begins for tasks touching 3+ service boundaries
- If framework adapter and coding adapter conflict on approach, meta-adapter runs formal trade-off analysis
- Reasoning adapter findings can override coding adapter plans when logical issues detected
- Cross-adapter knowledge flows through meta-adapter as clearinghouse
- For large tasks: adapters run in phases not all at once — design phase, then implementation phase, then verification phase

Behavior check:
Give agent task involving architecture decision.
Expected:
```
[META] Task requires 4+ service boundaries. Enforcing design-first.
[META] System Design adapter running first...
[META] Architecture decision: [decision]
[META] System Design approval required before Coding adapter starts.
[META] System Design: APPROVED — coding may begin.
[META] Coding adapter starting with architecture constraints locked in.
```

---

## Task 10.3 — Incremental Verifier

File: agent/senior/incremental_verifier.py (create new)

Every 3-5 subtasks completed triggers a verification checkpoint.

At checkpoint:
- All subtasks completed so far verified as coherent unit
- No regression introduced by the combination
- Semantic behavioral diff run against scope completed
- Only after checkpoint passes does execution continue to next chunk

If checkpoint fails: only last 3-5 subtasks need investigation. Not the entire task.

Behavior check:
Run large task with 15+ subtasks.
Expected: Checkpoint notices at steps 5, 10, 15 in execution log. Failure at step 8 means only steps 6-8 need investigation.

---

## Task 10.4 — Input Noise Detector

File: agent/senior/input_noise_detector.py (create new)

Before any task classification, check if input is clear enough.

Noise types:
- Ambiguous intent: same words could mean two different tasks
- Missing context: critical project information absent
- Conflicting signals: part suggests one task type, another suggests different
- Unclear scope: boundaries not defined

For each noise type: ask exactly ONE clarifying question. The most important one.
After answer: proceed with classification.
Never make silent assumptions about ambiguous inputs.

Behavior check:
Give deliberately ambiguous input.
Expected: Exactly one question asked. Not two. Not zero. The one question that resolves the most uncertainty.

---

## Task 10.5 — Intelligent Stop Condition

File: agent/execution/stop_condition.py (create new)

Two stop conditions:

Goal achieved: all acceptance criteria met, behavioral diff shows no regressions, all pre-existing tests still pass. Agent stops. Does not continue improving unless asked.

Diminishing returns: last three actions produced progressively smaller improvements and remaining issues are minor. Agent stops, marks main goal complete, lists minor observations separately as non-blocking.

Senior engineer ships working software. Does not hold up working feature for perfection.

Behavior check:
Complete a task. Agent stops precisely when goal-achieved conditions met.
Present task with minor remaining imperfections after main goal. Agent stops, marks goal complete, lists minor issues as observations.

---

## Phase 10 Exit Criteria
1. Unknown-unknown detector identifies undocumented non-standard component as requiring explanation
2. Meta-adapter enforces design-first sequencing for multi-boundary tasks
3. Incremental checkpoints appear every 3-5 subtasks in large task execution
4. Ambiguous input triggers exactly one clarifying question
5. Agent stops precisely at goal-achieved conditions, no over-engineering

---

# COMPLETE CAPABILITY AFTER PHASE 10

## What agent can do — Fresh Projects

Takes natural language description. Runs Engineer Pre-Task Protocol first. Analyzes requirements fully including implied ones. Reasons about architecture before writing one line. Chooses technology stack with justification. Plans database schema with migration safety. Selects versions appropriately. Creates all files in correct dependency order. Wires everything completely. Verifies consistency end to end. Generates tests from KB knowledge. Calibrates defensiveness to stated project personality.

Project types: REST API backend, Frontend SPA, Full stack monolith, Microservices, Mobile backend, Data pipeline, CLI tool, Library or SDK.

Languages: Python, JavaScript, TypeScript, Java, Go.
Frameworks: FastAPI, Django, Flask, Express, React, Angular, Vue, SpringBoot, and any framework in KB.

## What agent can do — Bug Fixing

Runs code review of affected area first. Builds change impact assessment. Classifies bug into one of ten types. Creates rollback plan before touching anything. Applies minimum change. Runs composition verifier after every file change. Runs behavioral diff. Runs adversarial tests. False positive checks. Marks complete only when all checks pass.

All ten bug types handled:
1. Crash bugs with clear stack trace
2. Wrong output bugs with no exception
3. Intermittent bugs — provides ranked candidates with explicit confidence limits, states production verification required
4. Data bugs — distinguishes code problem from data problem
5. Environment bugs — reads all configs, finds the difference
6. Integration bugs — identifies if the external party is behaving outside contract
7. Performance bugs — N+1 queries, missing indexes, algorithmic complexity, missing cache
8. Memory bugs — language-specific leak patterns
9. Security bugs — proactive audit on any touched file
10. Regression bugs — PMM change history identifies what changed recently

## What agent can do — New Functionality

Reads existing patterns before writing anything. Follows project conventions exactly, not framework defaults. Handles all functionality types: new API endpoint with full wiring, new frontend feature with full registration, new database entity with migration and indexes, new third-party integration, new background job, refactoring, performance improvement.

Nothing left half-connected. Behavioral diff runs after every change. Regression by omission caught.

## What agent is honest about

Intermittent bugs: best candidates provided, production verification explicitly required.
Unknown components: refuses to touch until explained.
Dangerous zones: always requires human confirmation.
Cascade confidence: reports real confidence, not inflated per-EKU confidence.
When it does not know: says so with confidence rather than guessing.

---

# STATUS COMMAND — EXACT EXPECTED OUTPUT PER PHASE

Run python -m agent status after every session.

After Phase 1G:
```
KB Tier 1: 1 EKUs | Tier 2: 0 patterns | Tier 3: 0 heuristics
LLM calls this session: 3 | KB answers: 1
```

After Phase 1.5 — seed python tier1:
```
KB Tier 1: 15+ EKUs | Tier 2: 2+ patterns | Tier 3: 0 heuristics
LLM calls this session: 45+ | KB answers: 8+
```

After Phase 2.5 — seed python all tiers:
```
KB Tier 1: 25+ EKUs | Tier 2: 5+ patterns | Tier 3: 2+ heuristics
Execution traces: 1+ | Cross-adapter hints: 1+
```

After Phase 3:
```
KB Tier 1: 25+ EKUs | Tier 2: 5+ patterns | Tier 3: 2+ heuristics
Failure library: entries with 10-type taxonomy
Traces stored: 5+
LLM calls this week: X | KB answers: Y | Target: Y > X
```

After Phase 10 — production state:
```
=== KNOWLEDGE BASE ===
KB Tier 1: [count] EKUs across [count] technologies
KB Tier 2: [count] patterns (auto-derived — zero manually written)
KB Tier 3: [count] heuristics (auto-derived — zero manually written)
KB Suspect: [count] EKUs under review
KB Contradictions: 0 (should always be 0)

=== PROJECT INTELLIGENCE ===
Projects in PMM: [count]
Project Briefs: [count]
Architecture Smells Detected: [count]
Tribal Knowledge Entries: [count]
Dangerous Zones Identified: [count]

=== EXECUTION QUALITY ===
Closed-loop corrections this week: [count]
Plan revisions during execution: [count]
Rollback plans created: [count]
Dangerous zone confirmations requested: [count]
False positives caught: [count]
Semantic regressions caught: [count]

=== SELF-IMPROVEMENT ===
Assessment errors this week: [count]
Systematic biases corrected: [count]
Cross-project patterns elevated: [count]

=== EFFICIENCY RATIO ===
LLM calls this week: [count]
KB answers without LLM this week: [count]
Ratio (lower = better): [ratio]
Target by month 3: ratio below 0.5
Target by month 6: ratio below 0.1
```

---

# THE RATIO THAT MEASURES EVERYTHING

Ratio = LLM calls this week divided by KB answers this week

Week 1: ratio above 5 — KB small, LLM for everything — NORMAL
Month 1: ratio below 2 — KB growing, LLM dropping — PROGRESS
Month 3: ratio below 0.5 — KB answers dominate — EXCELLENT
Month 6: ratio below 0.1 — LLM for new technology only — GOAL ACHIEVED

If ratio grows over time: agent not retaining knowledge. Fix storage or retrieval.
If KB answers not growing: agent not reusing knowledge. Fix retrieval or confidence calibration.

---

# COMPLETE PHASE TIMELINE

| Phase | Name | Time | Depends On | Agent Level After |
|---|---|---|---|---|
| EMERGENCY | Critical Hang Fixes | 2-3h | NOW | Runs reliably, never hangs |
| 1G | First Integration Run | 1h | Emergency | Learns and answers from KB |
| 1.5 | Seed Manifest + Bulk Learning | 3-4h | 1G | 50-100 concepts in KB |
| 2 | Knowledge Intelligence | 5h | 1.5 | Version-aware, contradiction-safe |
| 2.5 | Operational Brain | 4h | 2 | Self-aware, strategic, confident |
| 3 | Task Execution Engine | 7h | 2.5 | Executes tasks safely with closed-loop |
| 4 | Project Intelligence | 6h | 3 | Understands any project deeply |
| 5 | Multi-Language + Dependency | 5h | 4 | Works in 5 languages, safe deps |
| 6 | Adversarial Testing + QA | 5h | 5 | Challenges own success |
| 7 | Knowledge Lifecycle | 5h | 6 | KB stays fresh automatically |
| 8 | Self-Improvement | 4h | 7 | Gets smarter from mistakes |
| 9 | Production Hardening | 4h | All | Safe for real projects |
| 10 | Senior Engineer Layer | 6h | 9 | Full senior engineer capability |
| TOTAL | | 62-68h | | Real senior CS engineer agent |

---

# THE FIVE CORE PRINCIPLES

Principle 1 — Phase gates are not suggestions. Exit criteria demonstration is required. Tests passing does not equal phase done. Behavior check passing equals phase done.

Principle 2 — Confidence about uncertainty beats confidence about knowledge. "I don't know this, confidence 0.95" is more trustworthy than "I know this, confidence 0.8" that is sometimes wrong.

Principle 3 — Dead knowledge is worse than no knowledge. Never-applied EKUs corrupt retrieval and reduce signal-to-noise for everything else.

Principle 4 — Every failure is a lesson only if captured. Traces are the brain. Code is the mechanism. The agent that fails and learns is smarter after 100 tasks. The agent that fails and loses the trace is as dumb on task 100 as task 1.

Principle 5 — Dangerous zones require human confirmation. Always. Without exception. Regardless of confidence. Auth, payment, schema migration, secrets. A senior engineer who touches auth alone without review is not a senior engineer. Your agent will not be either.

---

*ULTIMATE_ENGINEER_AGENT_ROADMAP.md*
*Compiled: 2026-03-30*
*Synthesizes: MASTER_PLAN + ROADMAP_FINAL + rrq_audit + FINAL_COMPLETE_ROADMAP + ULTRA_ROADMAP + All conversation insights*
*Novel additions in this version: Engineer Pre-Task Protocol, Project Onboarding Process, Code Reviewer Mode, Estimation Engine, Dependency Conflict Analyzer, Migration Safety Analyzer, Rollback Planner, Documentation Trust Engine, Architecture Smell Detector, Test Generator from KB, 10 undocumented gaps identified and addressed*
*Total: 62-68 hours of disciplined execution to a real senior computer science engineer agent*
