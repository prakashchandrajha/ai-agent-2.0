# PROGRESS.md
# READ THIS FIRST. UPDATE THIS LAST. EVERY SESSION.
# Last Updated: 2026-03-28 (15:16:00)

---

## ONE-LINE STATUS

Phase 0, Task 0.7, NOT STARTED

---

## WHAT IS COMPLETE AND VERIFIED

Phase 0 (Foundation Stabilization) — IN PROGRESS
- Task 0.NEW-L: Implemented Transitive Confidence Calculator (Product of chain) — DONE and VERIFIED.
- Task 0.NEW-K: Implemented Composition Hazard Registry (5 Python, 2 JS hazards) — DONE and VERIFIED.
- Task 0.NEW-J: Implemented Version-Aware Knowledge Scoping (min/max/dep/rem checks) — DONE and VERIFIED.
- Task 0.NEW-I: Implemented Context Fingerprinting System (runtime, hashes, deps) — DONE and VERIFIED.
- Task 0.NEW-H: Implemented Gate Short-Circuiting in EKUStore (6 gates in order) — DONE and VERIFIED.
- Task 0.NEW-G: Implemented Parallel URL Scraping (asyncio.gather) — DONE and VERIFIED.
- Task 0.NEW-F: Implemented Batch Embedding Computation and Similarity Matrix — DONE and VERIFIED.
- Task 0.6: Created Session Logger (non-buffered JSON) — DONE and VERIFIED.
- Task 0.NEW-E: Implemented LLM Response Cache — DONE and VERIFIED.
- Task 0.NEW-D: Fixed Circular Imports and side-effects in __main__.py — DONE and VERIFIED.
- Task 0.5: Fixed JSON Extraction and Think Tags (handles nested tags and returns None on failure) — DONE and VERIFIED.
- Task 0.4: Created Pre-Execution Code Validator (regex-based static analysis) — DONE and VERIFIED.
- Task 0.4: Created Pre-Execution Code Validator (regex-based static analysis) — DONE and VERIFIED.
- Task 0.3: Fixed Contradiction Gate (confidence-based) — DONE and VERIFIED.
- Task 0.2: Fixed Rollback Direction (cascades downstream with dry_run) — DONE and VERIFIED.
- Task 0.1: Fixed Sandbox Environment Isolation (whitelist-only env) — DONE and VERIFIED.
- Task 0.NEW-C: Implemented Feature Flags system in config.py — DONE and VERIFIED.
- Task 0.NEW-B: Implemented cross-platform file locking and atomic writes in eku_store.py — DONE and VERIFIED.
- Task 0.NEW-A: Created migrations.py and wired into eku_schema.py for v1->v2 upgrades — DONE and VERIFIED.
- Task 0.0: Extended EKU schema with 15 new fields and 3 new dataclasses — DONE and VERIFIED.
Phase -1 (Pre-Flight) — all 8 checks passed and verified ALL GREEN.
Phase -2 (Foundation Audit) — all 3 tasks done and verified.
- Task -2.1: Module isolation tests complete (found working with correct internal APIs).
- Task -2.2: Dependency check complete (no conflicts, requirements.txt generated).
- Task -2.3: LLM baseline complete (identified forced JSON mode behavior).

---

Nothing yet.
---

## EXACT NEXT ACTION

Create agent/knowledge/semantic_correction.py with SemanticCorrector class.
Methods: correct_typo(term, known_terms) returns best match or original.
Implement fuzzy string matching (Levenshtein distance) using stdlib or minimal dependency.
Verify that 'pythn' corrects to 'python' when in the domain.

---

## DO NOT TOUCH THESE (already done — do not rewrite)

Nothing frozen yet.

---

## KNOWN ISSUES (pasted errors that are NOT the current task)

- LLMClient forces json format on all calls — needs json_mode=False parameter — fix in Phase 0 Task 0.5
None yet.

---

## DECISIONS MADE (do not re-debate)

- Embedding model locked to: all-MiniLM-L6-v2
- Primary LLM: phi3:medium via Ollama
- File locking: fcntl on Unix, msvcrt on Windows
- Schema version: 2.0.0
- Max learning iterations: 3
- Entropy threshold: 0.85

---

## LAST TEST RUN

No tests run yet.

---

## PHASE EXIT CRITERIA STATUS

| Phase | Status | Tests Passing |
|-------|--------|---------------|
| -2 | COMPLETE ✅ | 4/4 criteria |
| -1 | COMPLETE ✅ | 1/1 criteria |
| 0  | IN PROGRESS | 24/37 tests |
| 1  | NOT STARTED | 0/10 tests |
| 2+ | NOT STARTED | — |

---

## AGENT HANDOFF NOTES

Next agent: start with Phase 0 Task 0.7.
Read GUARDRAILS.md before touching anything.
Semantic Correction Engine.
