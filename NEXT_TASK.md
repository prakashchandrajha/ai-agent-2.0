# NEXT_TASK.md
# CURRENT TASK — UPDATE THIS AFTER EVERY COMPLETED TASK
# This is the ONLY thing the agent is allowed to work on right now.

---

## CURRENT TASK

Phase: 0
Task ID: 0.3
Task Name: Mandatory EKU Semantic Dimensions
From MASTER_PLAN.md: Phase 0, TASK 0.3

---

## EXACT ACTION

Update `ExecutableKnowledgeUnit` in `agent/knowledge/eku_schema.py` to make semantic dimensions (`how`, `why`, `when`, `what`) mandatory fields (not empty). Update `maybe_store` in `agent/knowledge/eku_store.py` to add a gate that enforces this.

---

## FILES TO TOUCH

- agent/knowledge/eku_schema.py
- agent/knowledge/eku_store.py

---

## DONE WHEN

- [ ] `ExecutableKnowledgeUnit` validation requires all four dimensions
- [ ] `maybe_store` rejects EKUs with any empty dimension
- [ ] python -c "from agent.knowledge.eku_schema import ExecutableKnowledgeUnit; e=ExecutableKnowledgeUnit(concept='test'); e.how=''; assert e.is_valid() == False; print('OK')" (or similar)
- [ ] PROGRESS.md updated

---

## HOW TO UPDATE THIS FILE WHEN TASK IS COMPLETE

Replace the contents with the next task from MASTER_PLAN.md.
Next task after this one: Phase 0, TASK 0.4 (Semantic Correction Engine)
