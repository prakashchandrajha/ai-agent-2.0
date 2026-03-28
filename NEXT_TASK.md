# NEXT_TASK.md
# CURRENT TASK — UPDATE THIS AFTER EVERY COMPLETED TASK
# This is the ONLY thing the agent is allowed to work on right now.

---

## CURRENT TASK

Phase: 0
Task ID: 0.8
Task Name: Per-Type Dedup Thresholds
From MASTER_PLAN.md: Phase 0, TASK 0.8

---

## EXACT ACTION

Add `DEDUP_THRESHOLDS` dictionary and `get_dedup_threshold(knowledge_type)` function to `agent/config.py`.
Thresholds: `invariant=0.95`, `definition=0.90`, `edge_case=0.85`, `example=0.80`, `constraint=0.92`, `_default=0.90`.

---

## FILES TO TOUCH

- agent/config.py

---

## DONE WHEN

- [ ] `DEDUP_THRESHOLDS` and `get_dedup_threshold` are implemented in `agent/config.py`
- [ ] `get_dedup_threshold('invariant')` returns `0.95`
- [ ] `get_dedup_threshold('example')` returns `0.80`
- [ ] `get_dedup_threshold('unknown')` returns `0.90` (default)
- [ ] PROGRESS.md updated

---

## HOW TO UPDATE THIS FILE WHEN TASK IS COMPLETE

Replace the contents with the next task from MASTER_PLAN.md.
Next task after this one: Phase 0, TASK 0.9 (VectorStore Stub)
