# NEXT_TASK.md
# CURRENT TASK — UPDATE THIS AFTER EVERY COMPLETED TASK
# This is the ONLY thing the agent is allowed to work on right now.

---

## CURRENT TASK

Phase: 0
Task ID: 0.NEW-B
Task Name: File Locking for JSON Stores
From MASTER_PLAN.md: Phase 0, TASK 0.NEW-B

---

## EXACT ACTION

Implement cross-platform file locking (fcntl for linux, msvcrt for windows) in agent/knowledge/json_store.py. Ensure all read/write operations use context managers for locking. Prevent data corruption during concurrent process access.

---

## FILES TO TOUCH

- agent/knowledge/json_store.py

---

## DONE WHEN

- [ ] agent/knowledge/json_store.py uses file locking
- [ ] Stress test with 10 concurrent processes writing to the same store passes without data loss
- [ ] PROGRESS.md updated

---

## HOW TO UPDATE THIS FILE WHEN TASK IS COMPLETE

Replace the contents with the next task from MASTER_PLAN.md.
Next task after this one: Phase 0, TASK 0.5 (LLMClient non-JSON mode)
