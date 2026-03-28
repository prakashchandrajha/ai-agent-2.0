# NEXT_TASK.md
# CURRENT TASK — UPDATE THIS AFTER EVERY COMPLETED TASK
# This is the ONLY thing the agent is allowed to work on right now.

---

## CURRENT TASK

Phase: 0
Task ID: 0.9
Task Name: VectorStore Stub
From MASTER_PLAN.md: Phase 0, TASK 0.9

---

## EXACT ACTION

Create `agent/services/vector_store.py` with `VectorStore` class. Methods: `add_eku(eku)`, `query_similar(query, n_results=5)`. For now, `query_similar` always returns `[]` and `add_eku` is a `pass`. This decouples the system from the actual vector database implementation.

---

## FILES TO TOUCH

- agent/services/vector_store.py only (create new file)

---

## DONE WHEN

- [ ] `VectorStore` class exists with `add_eku` and `query_similar` methods
- [ ] `query_similar` returns an empty list
- [ ] PROGRESS.md updated

---

## HOW TO UPDATE THIS FILE WHEN TASK IS COMPLETE

Replace the contents with the next task from MASTER_PLAN.md.
Next task after this one: Phase 0, TASK 0.10 (Grounded Extraction Bridge)
