# NEXT_TASK.md
# CURRENT TASK — UPDATE THIS AFTER EVERY COMPLETED TASK
# This is the ONLY thing the agent is allowed to work on right now.

---

## CURRENT TASK

Phase: 0
Task ID: 0.NEW-A
Task Name: Create migrations.py
From MASTER_PLAN.md: Phase 0, TASK 0.NEW-A

---

## EXACT ACTION

Create migrations.py in agent/knowledge/migrations.py to handle schema version 1.0.0 to 2.0.0 migration. Wire migrate_eku() into from_dict() as the first line in eku_schema.py.

---

## FILES TO TOUCH

- agent/knowledge/migrations.py (NEW)
- agent/knowledge/eku_schema.py (to wire migration)

---

## DONE WHEN

- [ ] agent/knowledge/migrations.py exists
- [ ] Roundtrip test with old EKU data (missing new fields) successfully migrates and doesn't crash
- [ ] PROGRESS.md updated

---

## HOW TO UPDATE THIS FILE WHEN TASK IS COMPLETE

Replace the contents with the next task from MASTER_PLAN.md.
Next task after this one: Phase 0, TASK 0.NEW-B (File Locking for JSON Stores)
