# NEXT_TASK.md
# CURRENT TASK — UPDATE THIS AFTER EVERY COMPLETED TASK
# This is the ONLY thing the agent is allowed to work on right now.

---

## CURRENT TASK

Phase: 0
Task ID: 0.0
Task Name: Extend EKU Schema
From MASTER_PLAN.md: Phase 0, TASK 0.0

---

## EXACT ACTION

Add 15 new fields to ExecutableKnowledgeUnit dataclass in agent/knowledge/eku_schema.py. Add 3 new dataclasses: ExecutionTrace, Constraint, GateDiagnostic. Update to_dict() and from_dict() for all new fields.

---

## FILES TO TOUCH

- agent/knowledge/eku_schema.py only

---

## DONE WHEN

- [ ] python -c "from agent.knowledge.eku_schema import ExecutableKnowledgeUnit, ExecutionTrace, Constraint, GateDiagnostic; print('OK')" runs without error
- [ ] Roundtrip test passes (from_dict(to_dict()))
- [ ] PROGRESS.md updated

---

## HOW TO UPDATE THIS FILE WHEN TASK IS COMPLETE

Replace the contents with the next task from MASTER_PLAN.md.
Next task after this one: Phase 0, TASK 0.NEW-A (Create migrations.py)
