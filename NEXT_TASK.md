# NEXT_TASK.md
# CURRENT TASK — UPDATE THIS AFTER EVERY COMPLETED TASK
# This is the ONLY thing the agent is allowed to work on right now.

---

## CURRENT TASK

Phase: 0
Task ID: 0.NEW-L
Task Name: Transitive Confidence Calculator
From MASTER_PLAN.md: Phase 0, TASK 0.NEW-L

---

## EXACT ACTION

Add `calculate_effective_confidence(eku_id)` method to `EKUStore` in `agent/knowledge/eku_store.py`. This method must recursively (or iteratively) calculate the real confidence by multiplying the EKU's raw confidence by the confidences of all its dependencies. Returns tuple `(float, str)` where the string is the chain description (e.g., `"A(0.90) * B(0.80) = 0.72"`).

---

## FILES TO TOUCH

- agent/knowledge/eku_store.py

---

## DONE WHEN

- [ ] `calculate_effective_confidence` exists in `EKUStore`
- [ ] Returns `(conf, chain)` where `conf` is correctly multiplied
- [ ] Returns `(raw_conf, concept)` if no dependencies
- [ ] PROGRESS.md updated

---

## HOW TO UPDATE THIS FILE WHEN TASK IS COMPLETE

Replace the contents with the next task from MASTER_PLAN.md.
Next task after this one: Phase 0, TASK 0.7 (Semantic Correction Engine)
