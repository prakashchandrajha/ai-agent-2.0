# NEXT_TASK.md
# CURRENT TASK — UPDATE THIS AFTER EVERY COMPLETED TASK
# This is the ONLY thing the agent is allowed to work on right now.

---

## CURRENT TASK

Phase: 0
Task ID: 0.NEW-J
Task Name: Version-Aware Knowledge Scoping
From MASTER_PLAN.md: Phase 0, TASK 0.NEW-J

---

## EXACT ACTION

Add `is_compatible_with_version(eku, runtime_version)` to `agent/knowledge/eku_schema.py`. It must check `eku.version_bounds` for `min_version`, `max_version`, `deprecated_in`, and `removed_in`. Use the `packaging.version.Version` (or a similar stable logic) to compare. Returns `(bool, warning_message)`.

---

## FILES TO TOUCH

- agent/knowledge/eku_schema.py only

---

## DONE WHEN

- [ ] `is_compatible_with_version` exists and handles all 4 bounds correctly
- [ ] Returns `(False, msg)` if below `min_version` or above `removed_in`
- [ ] Returns `(True, msg)` if deprecated but not yet removed
- [ ] PROGRESS.md updated

---

## HOW TO UPDATE THIS FILE WHEN TASK IS COMPLETE

Replace the contents with the next task from MASTER_PLAN.md.
Next task after this one: Phase 0, TASK 0.NEW-K (Composition Hazard Registry)
