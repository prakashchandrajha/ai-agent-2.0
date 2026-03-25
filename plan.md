# 🧠 AI Autonomous Engineer — Master Roadmap

> **From Zero to Self-Improving Autonomous Agent**
>
> Every line below is practical, buildable, and sequenced so each phase
> produces a runnable artifact before the next phase begins.

---

## 📦 Asset Inventory — What We Already Have

| Repo | What It Gives Us | Steal-Worthy Components |
|---|---|---|
| **LocalMind** | Offline RAG stack — LLM client (Ollama/LMStudio/GPT4All), ChromaDB vector store, chunker, embedder, RAG engine, document parsers (PDF/DOCX/PPTX/Excel), fine-tuning pipeline (LoRA/QLoRA/Unsloth) | `LLMClient` (unified async LLM interface), `RAGEngine` (context-building + streaming), `VectorStore` (ChromaDB wrapper), `Embedder`, `Chunker`, `Finetuner` |
| **PageIndex** | Vectorless reasoning-based RAG — hierarchical tree index from documents, LLM tree-search retrieval, TOC detection & extraction, concurrent page processing | `page_index.py` (tree structure generation), `utils.py` (LLM completion helpers, JSON extraction, token counting), reasoning-based retrieval pattern |
| **Scrapling** | Industrial web scraping — adaptive element tracking, anti-bot bypass (Cloudflare Turnstile), browser automation, MCP server, spider framework with pause/resume, proxy rotation | `Fetcher`/`StealthyFetcher`/`DynamicFetcher` (web data collection), `parser.py` (57KB — adaptive HTML parsing), `spiders/` (concurrent crawling framework) |
| **autoresearch** | Karpthy's autonomous experiment loop — modify→run→evaluate→keep/discard with git branching, results logging, crash recovery, infinite autonomous loop | `program.md` pattern (agent-as-researcher), experiment loop logic, results.tsv tracking, git-based rollback mechanism |

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    COMMAND INTERFACE                         │
│            .learn <subject> <topic>                          │
│            .apply <context>                                  │
│            .debug <code>                                     │
│            .evolve (self-improvement trigger)                │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                 ORCHESTRATOR (Brain)                         │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌───────────────┐  │
│  │ Phase    │ │ Decision │ │ Failure  │ │ Knowledge     │  │
│  │ Router   │ │ Engine   │ │ Memory   │ │ Compression   │  │
│  └──────────┘ └──────────┘ └──────────┘ └───────────────┘  │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                 COGNITIVE MODULES                            │
│                                                              │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────────┐    │
│  │ Collector   │  │ Distiller   │  │ Verifier         │    │
│  │ (Scrapling) │  │ (PageIndex) │  │ (Self-Challenge) │    │
│  └─────────────┘  └─────────────┘  └──────────────────┘    │
│                                                              │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────────┐    │
│  │ Executor    │  │ Failure     │  │ Divergence       │    │
│  │ (Sandbox)   │  │ Analyzer    │  │ Detector         │    │
│  └─────────────┘  └─────────────┘  └──────────────────┘    │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│              KNOWLEDGE STORE (EKU Database)                  │
│                                                              │
│  ┌──────────────────────────────────────────────────┐       │
│  │  Executable Knowledge Units (EKUs)                │       │
│  │  ┌─────────┐ ┌───────────┐ ┌─────────────────┐  │       │
│  │  │ Concept │ │ Invariants│ │ Transformations  │  │       │
│  │  └─────────┘ └───────────┘ └─────────────────┘  │       │
│  │  ┌──────────────┐ ┌───────────────────────────┐  │       │
│  │  │ Failure Mem  │ │ Execution Templates       │  │       │
│  │  └──────────────┘ └───────────────────────────┘  │       │
│  └──────────────────────────────────────────────────┘       │
│                                                              │
│  Storage: ChromaDB (vectors) + JSON (structured EKUs)        │
│  Source: LocalMind vector_store + custom EKU schema          │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔧 Phase 0: Project Skeleton & Infrastructure

**Goal**: Working project structure, all dependencies installable, basic CLI running.

### Steps

1. **Initialize project structure**
   ```
   ai-agent-2.0/
   ├── agent/
   │   ├── __init__.py
   │   ├── cli.py                    # Command interface
   │   ├── orchestrator.py           # Phase router + brain
   │   ├── config.py                 # Stolen from LocalMind config.py
   │   └── modules/
   │       ├── collector.py          # Web knowledge collection
   │       ├── distiller.py          # Knowledge extraction & tree indexing
   │       ├── verifier.py           # Self-verification engine
   │       ├── executor.py           # Sandbox code execution
   │       ├── failure_analyzer.py   # Failure intelligence
   │       ├── divergence_detector.py
   │       ├── decision_engine.py    # When/Why/When-NOT logic
   │       └── compressor.py         # Knowledge → EKU compression
   │   ├── knowledge/
   │   │   ├── eku_store.py          # EKU database manager
   │   │   ├── eku_schema.py         # EKU data structures
   │   │   └── vector_store.py       # Stolen from LocalMind
   │   ├── llm/
   │   │   ├── client.py             # Stolen from LocalMind LLMClient
   │   │   └── prompts.py            # All system prompts centralized
   │   └── sandbox/
   │       ├── runner.py             # Isolated code execution
   │       └── capture.py            # Output/error/perf capture
   ├── tests/
   ├── plan.md                       # This file
   └── pyproject.toml
   ```

2. **Steal & adapt from LocalMind**:
   - `config.py` → `agent/config.py` (strip document-specific stuff, add agent config)
   - `llm_client.py` → `agent/llm/client.py` (keep Ollama + OpenAI-compatible interface)
   - `vector_store.py` → `agent/knowledge/vector_store.py` (for storing concept embeddings)
   - `embedder.py` → `agent/knowledge/` (for semantic similarity checks)

3. **Steal & adapt from PageIndex**:
   - `utils.py` → extract `llm_completion`, `llm_acompletion`, `extract_json`, `count_tokens` into `agent/llm/helpers.py`
   - Tree-indexing pattern → `agent/modules/distiller.py` (adapted for knowledge trees instead of PDF pages)

4. **Dependencies** (pyproject.toml):
   ```toml
   [project]
   name = "ai-autonomous-engineer"
   requires-python = ">=3.11"
   dependencies = [
       "httpx>=0.26.0",
       "openai>=1.10.0",
       "chromadb>=0.4.22",
       "sentence-transformers>=2.3.1",
       "scrapling>=0.2.0",
       "pydantic>=2.0",
       "rich>=13.0",     # Beautiful CLI output
       "typer>=0.9.0",   # CLI framework
   ]
   ```

**Deliverable**: `python -m agent learn python "list comprehensions"` starts without crashing.

---

## 🧠 Phase 1: Pre-Learning Validation (Your Phase 0)

**Goal**: Before learning ANYTHING, the agent must know EXACTLY what it's about to learn.

### What the agent does when you type `.learn python "decorators"`:

```python
# agent/modules/pre_validator.py

class PreLearningValidator:
    """
    THE MOST CRITICAL MODULE.
    Skip this = learn the wrong thing deeply = worse than not learning.
    """

    async def validate(self, subject: str, topic: str) -> LearningContract:
        # Step 1: Disambiguate
        disambiguation = await self.disambiguate(subject, topic)
        # "decorators" → Python decorators (@ syntax) vs Design Pattern Decorator
        # If ambiguous → resolve via context or raise for clarification

        # Step 2: Scope Control
        scope = await self.define_scope(disambiguation)
        # depth_level: "intermediate"
        # boundaries: ["NOT Java annotations", "NOT TypeScript decorators"]
        # prerequisites: ["functions", "closures", "first-class functions"]

        # Step 3: Mastery Definition
        mastery = await self.define_mastery(disambiguation, scope)
        # can_explain: ["what a decorator is", "how wrapping works"]
        # can_implement: ["basic decorator", "decorator with arguments", "class decorator"]
        # can_debug: ["decorator ordering issues", "lost function metadata"]

        return LearningContract(
            resolved_topic=disambiguation,
            scope=scope,
            mastery_criteria=mastery,
            abort_conditions=["topic too broad", "prerequisites missing"]
        )
```

### The Hidden Thing Nobody Builds (But We Will)

> **Prerequisite Detection**: Before learning "decorators", check if the agent
> already has EKUs for "functions", "closures", "first-class functions". If not,
> queue those first. This is how humans learn — bottom-up, not random-access.

**Steal from PageIndex**: The tree-indexing logic already handles hierarchical
relationships. We adapt it to build a **Concept Dependency Tree** instead of a
document tree.

---

## 📚 Phase 2: Controlled Learning (Your Phase 1)

**Goal**: Collect raw knowledge from multiple sources, filter noise, extract structured primitives.

### Data Collection Pipeline

```python
# agent/modules/collector.py
# STOLEN FROM: Scrapling (fetchers + adaptive parsing)

class KnowledgeCollector:
    async def collect(self, contract: LearningContract) -> RawKnowledge:
        # 1. Multi-source fetching (Scrapling StealthyFetcher)
        sources = await self.fetch_sources(contract.resolved_topic)

        # 2. Entropy Filter — THE KEY INNOVATION
        #    Most sources say the same thing 10 different ways.
        #    Only keep information with NEW semantic content.
        filtered = self.entropy_filter(sources)

        # 3. Extract structured primitives
        return RawKnowledge(
            definitions=[],      # "A decorator is..."
            invariants=[],       # "Decorators always wrap functions"
            constraints=[],      # "Must be callable"
            edge_cases=[],       # "Decorating a class method vs function"
            failure_scenarios=[] # "Using mutable default in decorator"
        )
```

### Entropy Filter (The Thing Other Agents Miss)

```python
def entropy_filter(self, sources: list[SourceContent]) -> list[SourceContent]:
    """
    If 5 sources all say 'a decorator wraps a function',
    keep ONE instance. If source #3 adds 'functools.wraps preserves metadata',
    that's NEW information — keep it.

    Uses embeddings from LocalMind's Embedder to measure semantic distance.
    Threshold: if cosine_similarity > 0.92 → duplicate → discard.
    """
```

**Steal from Scrapling**: Use `Fetcher` for fast HTTP docs, `StealthyFetcher` when
sources have anti-bot (StackOverflow, Medium). Use `parser.py`'s adaptive element
tracking to reliably extract code blocks even when page structures change.

**Steal from LocalMind**: Use `Embedder` for semantic dedup in the entropy filter.

---

## ⚠️ Phase 3: Self-Verification (Your Phase 2)

**Goal**: The agent must CHALLENGE its own understanding BEFORE it practices.

```python
# agent/modules/verifier.py

class SelfVerifier:
    """
    THE MOST IMPORTANT MODULE.
    This is what separates 'I think I know' from 'I proved I know'.
    """

    async def verify(self, raw: RawKnowledge) -> VerificationResult:
        # 1. Generate counter-questions
        counters = await self.generate_counter_questions(raw)
        # "If decorators wrap functions, what happens to the original function object?"
        # "Can you decorate a lambda?"
        # "What's the execution order of stacked decorators?"

        # 2. Find contradictions across sources
        contradictions = await self.find_contradictions(raw)
        # Source A says "decorators are syntactic sugar"
        # Source B says "decorators are a design pattern"
        # → Both correct in different contexts → MARK with context tags

        # 3. Cross-check logic consistency
        logic_gaps = await self.logic_check(raw)
        # "If decorator must be callable, and classes are callable,
        #  then classes can be decorators" → verify this holds

        return VerificationResult(
            confidence_score=0.0_to_1.0,
            verified_facts=[],
            uncertain_facts=[],    # These get flagged, not stored
            contradictions=[],     # These get resolved or quarantined
            gaps=[]                # These trigger more collection
        )
```

### The Nuclear Option: Quarantine

> If a fact cannot be verified and cannot be disproved, it goes into
> **Quarantine** — a separate store where it's tagged as "unproven".
> Quarantined knowledge is NEVER used in code generation.
> It can only graduate to verified status by passing execution tests.

---

## 🧪 Phase 4: Execution-Based Learning (Your Phase 3)

**Goal**: Theory means NOTHING until code runs, passes, and handles edge cases.

```python
# agent/modules/executor.py + agent/sandbox/runner.py
# STOLEN FROM: autoresearch (run→evaluate→keep/discard loop)

class ExecutionLearner:
    async def learn_by_doing(self, verified: VerificationResult) -> ExecutionResults:
        test_cases = await self.generate_test_cases(verified)
        # normal:  @my_decorator def hello(): ...
        # edge:    stacked decorators, decorating async functions
        # extreme: decorator that modifies function signature, recursive decorators

        results = []
        for test in test_cases:
            result = await self.sandbox.run(test)
            # Capture: stdout, stderr, return value, execution time, memory usage
            results.append(result)

        # THE AUTORESEARCH PATTERN:
        # If test passes → keep the knowledge that produced it
        # If test fails → analyze WHY, store the failure, try again
        # If test crashes → this is GOLD — a real edge case discovered

        return ExecutionResults(
            passed=passed_tests,
            failed=failed_tests,
            crashes=crashes,
            performance_metrics=metrics
        )
```

### Sandbox Design

```python
# agent/sandbox/runner.py

class Sandbox:
    """
    Isolated execution environment.
    NEVER runs untested code in the main process.
    """

    async def run(self, code: str, timeout: int = 30) -> SandboxResult:
        # Uses subprocess with:
        # - timeout (kill after N seconds)
        # - memory limit (ulimit)
        # - no network access
        # - no filesystem write access outside /tmp/sandbox/
        # - capture ALL output (stdout, stderr, return code)

        proc = await asyncio.create_subprocess_exec(
            sys.executable, '-c', code,
            stdout=PIPE, stderr=PIPE,
            preexec_fn=self._set_limits
        )
        stdout, stderr = await asyncio.wait_for(
            proc.communicate(), timeout=timeout
        )
        return SandboxResult(
            stdout=stdout.decode(),
            stderr=stderr.decode(),
            return_code=proc.returncode,
            execution_time=elapsed,
            memory_peak=peak_mem
        )
```

---

## 🔥 Phase 5: Failure Intelligence (Your Phase 4)

**Goal**: Every failure is a lesson. Store it as structured knowledge, not raw error text.

```python
# agent/modules/failure_analyzer.py

class FailureAnalyzer:
    """
    Converts raw failures into Failure Knowledge Units (FKUs).
    These are the MOST VALUABLE knowledge — more than textbook definitions.
    """

    async def analyze(self, failure: SandboxResult) -> FailureKnowledgeUnit:
        return FailureKnowledgeUnit(
            failure_type=self.classify(failure),     # TypeError, LogicError, EdgeCase
            root_cause=await self.find_root_cause(failure),
            # "functools.wraps was not applied, __name__ was lost"
            fix_applied=await self.generate_fix(failure),
            prevention_rule=await self.derive_rule(failure),
            # "ALWAYS use @functools.wraps(func) inside decorator"
            related_concept=failure.concept_id,
            severity="critical" | "warning" | "info",
            reproducible=True,
            context_tags=["decorator", "metadata", "functools"]
        )
```

### Experience Memory (What Makes This Agent Different)

> Most agents forget their failures. This one doesn't.
> When the agent encounters a similar situation in the future,
> it checks Experience Memory FIRST:
>
> "I tried this before. It failed because X. The fix was Y."
>
> This is how human engineers work — not by re-reading documentation,
> but by remembering what broke last time.

---

## 🔄 Phase 6: Divergence Detection (Your Phase 5)

**Goal**: Detect when knowledge that worked in one context fails in another.

```python
# agent/modules/divergence_detector.py

class DivergenceDetector:
    """
    THE HIDDEN KILLER OF BAD AGENTS:
    Something works for 3 test cases. Agent marks it 'learned'.
    Case #4 breaks. But agent already 'knows' it.

    This module catches that.
    """

    async def detect(self, eku: ExecutableKnowledgeUnit) -> list[Divergence]:
        # 1. Generate VARIANT contexts
        variants = await self.generate_variants(eku)
        # Original: decorator on sync function
        # Variant 1: decorator on async function
        # Variant 2: decorator on class method
        # Variant 3: decorator on staticmethod
        # Variant 4: decorator on property

        # 2. Run each variant
        results = await self.executor.run_batch(variants)

        # 3. Find divergences
        divergences = []
        for variant, result in zip(variants, results):
            if result.differs_from_expected():
                divergences.append(Divergence(
                    context=variant.context,
                    expected=variant.expected_output,
                    actual=result.output,
                    unstable_assumption=await self.isolate_assumption(eku, variant)
                ))

        # 4. Mark unstable knowledge
        for d in divergences:
            eku.mark_unstable(d.unstable_assumption, d.context)

        return divergences
```

---

## ⚙️ Phase 7: Transformation Learning (Your Phase 6)

**Goal**: Store WHEN/WHY/WHEN-NOT, not just WHAT.

```python
# agent/modules/decision_engine.py

class TransformationLearner:
    """
    KEY INNOVATION: Don't store 'use decorator'.
    Store 'use decorator WHEN X, BECAUSE Y, NOT WHEN Z'.
    """

    async def learn_transformations(self, eku: EKU) -> list[Transformation]:
        return [
            Transformation(
                action="use decorator",
                when="need to add behavior to multiple functions without modifying them",
                why="separation of concerns, DRY principle",
                when_not="when the function only needs the behavior once",
                alternative="use a simple wrapper function or if/else",
                trade_offs={
                    "readability": "+1 (cleaner than manual wrapping)",
                    "debugging": "-1 (stack trace shows wrapper, not original)",
                    "performance": "-0.5 (extra function call overhead)"
                }
            )
        ]
```

---

## 🧠 Phase 8: Knowledge Compression → EKU (Your Phase 7)

**Goal**: Convert all learning into Executable Knowledge Units — the agent's permanent memory.

```python
# agent/knowledge/eku_schema.py

@dataclass
class ExecutableKnowledgeUnit:
    """
    THE fundamental unit of agent memory.
    No raw text. No vague descriptions.
    Every field is structured, queryable, and executable.
    """
    id: str                          # UUID
    concept: str                     # "Python Decorator"
    domain: str                      # "python"
    topic: str                       # "decorators"

    # 1. WHAT it is
    definition: str                  # Precise, one-sentence definition
    invariants: list[str]            # Rules that NEVER change
    # ["Decorator must be callable",
    #  "Original function is replaced by wrapper's return value",
    #  "@decorator is equivalent to func = decorator(func)"]

    # 2. HOW to use it
    transformations: list[Transformation]  # When/Why/When-not decision logic
    execution_templates: list[CodeTemplate] # Minimal working examples

    # 3. WHAT breaks
    failure_memory: list[FailureKnowledgeUnit]
    edge_cases: list[EdgeCase]
    constraints: list[str]           # Hard limits

    # 4. META
    confidence: float                # 0.0 to 1.0
    verification_status: str         # "proven" | "quarantined" | "unstable"
    last_tested: datetime
    test_pass_rate: float
    dependencies: list[str]          # EKU IDs this depends on
    created_at: datetime
    version: int                     # Incremented on updates

    # 5. CROSS-LANGUAGE (for generalization)
    language_mappings: dict[str, CodeTemplate]
    # {"javascript": "function decorator...", "rust": "proc_macro..."}
```

### Storage Strategy (Dual Store)

```
ChromaDB (vector store — from LocalMind)
├── Semantic search: "find concepts similar to 'function wrapper'"
├── Used for: retrieval, similarity, dedup
└── Each EKU embedded with concept + invariants as text

JSON/SQLite (structured store)
├── Exact lookups: "get EKU for python.decorators"
├── Used for: dependency resolution, failure memory queries
└── Full EKU objects serialized
```

---

## 💾 Phase 9: Delayed Storage (Your Phase 8)

**Goal**: NEVER store knowledge immediately. Only after it passes all verification gates.

```python
# agent/knowledge/eku_store.py

class EKUStore:
    async def maybe_store(self, eku: EKU) -> bool:
        """
        Storage Gate — THE CRITICAL FIX.
        Most agents dump everything into memory immediately.
        This creates garbage knowledge that poisons future reasoning.
        """
        gates = [
            self.gate_tests_pass(eku),        # All test cases pass
            self.gate_failures_understood(eku), # Failures analyzed, not ignored
            self.gate_edge_cases_handled(eku),  # Not just happy-path knowledge
            self.gate_no_contradictions(eku),   # Doesn't conflict with existing EKUs
            self.gate_not_overfitted(eku),      # Passes > 3 variant contexts
        ]

        results = await asyncio.gather(*gates)

        if all(results):
            eku.verification_status = "proven"
            await self.store(eku)
            return True
        else:
            failed = [g.__name__ for g, r in zip(gates, results) if not r]
            eku.verification_status = "quarantined"
            eku.quarantine_reason = failed
            await self.quarantine(eku)
            return False
```

---

## 🧪 Phase 10: Stress & Adversarial Testing (Your Phase 9)

**Goal**: Deliberately try to BREAK the agent's own knowledge.

```python
# agent/modules/stress_tester.py
# STOLEN FROM: autoresearch (the never-stop experiment loop)

class StressTester:
    """
    The autoresearch pattern, applied to knowledge instead of model training.
    Loop: mutate → test → keep/discard → repeat.
    """

    async def stress_test(self, eku: EKU) -> StressResult:
        # 1. Break its own logic intentionally
        attacks = await self.generate_adversarial_inputs(eku)
        # "What if the decorator receives None?"
        # "What if it's applied to a generator?"
        # "What if the wrapper doesn't call the original function?"

        # 2. Generate worst-case scenarios
        worst_cases = await self.generate_worst_cases(eku)
        # Max recursion with recursive decorator
        # Decorator on decorator on decorator (10 levels deep)
        # Decorator that mutates global state

        # 3. Simulate misuse
        misuse = await self.simulate_misuse(eku)
        # "Using decorator when a simple function call would suffice"
        # "Decorating every function in a module"

        # 4. Run everything through sandbox
        for test in attacks + worst_cases + misuse:
            result = await self.sandbox.run(test)
            if result.unexpected():
                eku.add_failure(result)
                eku.confidence *= 0.9  # Each unknown failure decreases confidence
```

---

## 🧬 Phase 11: Decision Engine Training (Your Phase 10)

**Goal**: Agent learns WHEN to apply vs avoid concepts, with trade-off awareness.

This uses the accumulated data from Phases 4–10 to build a decision matrix:

```
CONCEPT: Python Decorator
├── APPLY WHEN:
│   ├── Multiple functions need the same preprocessing → confidence: 0.95
│   ├── Cross-cutting concerns (logging, auth, caching) → confidence: 0.98
│   └── Need to modify function behavior without touching source → confidence: 0.92
├── AVOID WHEN:
│   ├── One-off behavior modification → confidence: 0.88
│   ├── Heavy computation in decorator (perf impact) → confidence: 0.85
│   └── Team doesn't know decorators (readability cost) → confidence: 0.72
└── TRADE-OFFS:
    ├── readability: +1 (cleaner) vs -1 (magical behavior)
    ├── debugging:   -1 (wrapper in stack trace)
    └── testability: +1 (test decorator independently)
```

---

## 🔁 Phase 12: Iterative Reinforcement (Your Phase 11)

**Goal**: Loop until the agent cannot break its own knowledge.

```python
# agent/orchestrator.py
# STOLEN FROM: autoresearch program.md (the never-stop loop)

class LearningOrchestrator:
    async def learn(self, subject: str, topic: str):
        # Phase 0: Pre-validation
        contract = await self.pre_validator.validate(subject, topic)

        # The autoresearch-style loop
        iteration = 0
        while True:
            iteration += 1

            # Phases 1-8: Full learning pipeline
            raw = await self.collector.collect(contract)
            verified = await self.verifier.verify(raw)
            executed = await self.executor.learn_by_doing(verified)
            failures = await self.failure_analyzer.analyze_all(executed)
            divergences = await self.divergence_detector.detect(eku)
            transformations = await self.transformation_learner.learn(eku)
            eku = await self.compressor.compress(verified, executed, failures, transformations)

            # Phase 9: Stress test
            stress = await self.stress_tester.stress_test(eku)

            # Phase 10: Storage gate
            stored = await self.eku_store.maybe_store(eku)

            # CONVERGENCE CHECK
            if eku.confidence >= 0.95 and eku.test_pass_rate >= 0.98:
                break  # Knowledge is battle-tested

            if iteration > 10:
                eku.verification_status = "needs_human_review"
                break  # Prevent infinite loops
```

---

## ⚠️ Hidden Failure Guards (Built Into Every Phase)

### 1. Illusion Detection
```python
# Built into verifier.py
async def detect_illusion(self, eku: EKU) -> bool:
    """
    "I think I know this" vs "I proved this"
    If confidence is high but test_pass_rate is low → ILLUSION
    """
    if eku.confidence > 0.8 and eku.test_pass_rate < 0.5:
        eku.verification_status = "illusion_detected"
        eku.confidence = eku.test_pass_rate  # Force-correct
        return True
    return False
```

### 2. Overfitting Guard
```python
# Built into divergence_detector.py
async def detect_overfitting(self, eku: EKU) -> bool:
    """If solution works only for 2-3 cases → REJECT"""
    unique_contexts = len(set(t.context for t in eku.passed_tests))
    return unique_contexts < 4  # Must pass in at least 4 distinct contexts
```

### 3. Memory Corruption Check
```python
# Built into eku_store.py
async def check_corruption(self, new_eku: EKU) -> list[Conflict]:
    """If new learning contradicts existing EKU → resolve before storing"""
    existing = await self.find_related(new_eku)
    conflicts = []
    for old in existing:
        for new_inv in new_eku.invariants:
            for old_inv in old.invariants:
                if await self.contradicts(new_inv, old_inv):
                    conflicts.append(Conflict(new=new_inv, old=old_inv))
    return conflicts
```

### 4. Shallow Learning Detection
```python
# Built into compressor.py
async def detect_shallow(self, eku: EKU) -> bool:
    """If agent cannot explain OR apply in new context → INCOMPLETE"""
    can_explain = len(eku.definition) > 20 and len(eku.invariants) >= 2
    can_apply = len(eku.execution_templates) >= 1 and eku.test_pass_rate > 0
    can_generalize = len(eku.language_mappings) >= 1 or len(eku.transformations) >= 1
    return not (can_explain and can_apply and can_generalize)
```

---

## 🧬 Human-Like Generalization

```python
# agent/modules/generalizer.py

class Generalizer:
    """
    Once the agent understands addition (2+2), it should handle:
    - 4+8
    - 20000+4568
    - any_number + any_number

    This is PATTERN EXTRACTION, not memorization.
    """

    async def generalize(self, eku: EKU) -> EKU:
        # 1. Extract the PATTERN from specific examples
        pattern = await self.extract_pattern(eku.execution_templates)
        # From "@decorator def f(): ..." extract:
        # Pattern: "callable(callable) → callable"

        # 2. Generate SCALED variations
        variations = await self.scale_pattern(pattern)
        # Variation 1: Simple function → Simple decorated function
        # Variation 2: Class with 10 methods → All decorated
        # Variation 3: Module with 100 functions → Selective decoration

        # 3. Verify generalization holds at scale
        for v in variations:
            result = await self.sandbox.run(v.code)
            if not result.passed:
                eku.add_constraint(f"Pattern breaks at scale: {v.description}")

        return eku
```

---

## 🚀 Implementation Order (What To Build First)

| Priority | Phase | Days | Why First |
|----------|-------|------|-----------|
| **P0** | Phase 0: Skeleton + Config | 2 | Nothing works without a runnable project |
| **P0** | LLM Client (steal from LocalMind) | 1 | Every module needs LLM access |
| **P0** | Sandbox Runner | 1 | Can't verify anything without safe code execution |
| **P1** | Phase 1: Pre-Validator | 2 | Wrong scope = wasted everything |
| **P1** | Phase 2: Collector (steal from Scrapling) | 2 | No data = no learning |
| **P1** | Phase 4: Executor + Phase 5: Failure Analyzer | 3 | Execution-first learning is the core loop |
| **P2** | EKU Schema + Store | 2 | Need somewhere to put validated knowledge |
| **P2** | Phase 3: Verifier | 2 | Self-challenge before storing |
| **P2** | Phase 9: Delayed Storage | 1 | Gate that prevents garbage knowledge |
| **P3** | Phase 6: Divergence Detection | 2 | Catches context-dependent failures |
| **P3** | Phase 7: Transformation Learning | 2 | When/why/when-not logic |
| **P3** | Phase 10: Stress Testing | 2 | Agent tries to break itself |
| **P4** | Phase 11: Decision Engine | 2 | Accumulated intelligence |
| **P4** | Phase 12: Reinforcement Loop (autoresearch pattern) | 2 | Ties everything together |
| **P4** | Generalization Engine | 2 | Scale from specific to universal |

**Total: ~28 days for a working v1**

---

## 🔑 What Makes This Agent Different From Every Other Agent

| Other Agents | This Agent |
|---|---|
| Learn once, store immediately | Learn → Verify → Stress-test → THEN store |
| Store raw text | Store structured EKUs (executable, queryable) |
| No failure memory | Every failure is a permanent lesson |
| No self-challenge | Agent tries to BREAK its own knowledge |
| Context-blind | Divergence detection catches context-dependent bugs |
| Know WHAT | Know WHAT + WHEN + WHY + WHEN-NOT |
| Memorize examples | Extract patterns, generalize to any scale |
| Trust their own output | Illusion detection, overfitting guard, corruption check |
| Stop when they think they're done | Stop when they CANNOT BREAK themselves anymore |

---

## 🎯 Final Agent Capabilities (When Complete)

The agent will be able to:

- ✅ Learn any programming topic from subject + topic name
- ✅ Validate knowledge through execution, not just reading
- ✅ Apply knowledge across different contexts and scales
- ✅ Write AND debug code using its verified EKU library
- ✅ Detect and fix its own mistakes from experience memory
- ✅ Explain WHY it chose a particular approach (decision engine)
- ✅ Improve over time without knowledge corruption
- ✅ Generalize from specific examples to universal patterns
- ✅ Never store unproven knowledge (delayed storage gate)
- ✅ Break its own logic to find weaknesses (stress testing)

> **Learning is NOT complete when you understand.**
> **Learning is complete when you cannot break it anymore.**
