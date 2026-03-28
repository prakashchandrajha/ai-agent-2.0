# PROGRESS.md
# READ THIS FIRST. UPDATE THIS LAST. EVERY SESSION.
# Last Updated: [agent updates this]

---

## ONE-LINE STATUS

Phase 0, Task 0.0, NOT STARTED

---

## WHAT IS COMPLETE AND VERIFIED

Phase -1 (Pre-Flight) — all 8 checks passed and verified ALL GREEN.
Phase -2 (Foundation Audit) — all 3 tasks done and verified.
- Task -2.1: Module isolation tests complete (found working with correct internal APIs).
- Task -2.2: Dependency check complete (no conflicts, requirements.txt generated).
- Task -2.3: LLM baseline complete (identified forced JSON mode behavior).

---

## WHAT IS IN PROGRESS

Nothing yet.

---

## EXACT NEXT ACTION

Extend EKU Schema in agent/knowledge/eku_schema.py.
Add 15 new fields and 3 new dataclasses.
Verify roundtrip with to_dict() and from_dict().

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
| 0  | IN PROGRESS | 0/37 tests |
| 1  | NOT STARTED | 0/10 tests |
| 2+ | NOT STARTED | — |

---

## AGENT HANDOFF NOTES

Next agent: start with Phase 0 Task 0.0.
Read GUARDRAILS.md before touching anything.
Extend EKU Schema in agent/knowledge/eku_schema.py.
