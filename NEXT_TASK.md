# NEXT_TASK.md
# CURRENT TASK — UPDATE THIS AFTER EVERY COMPLETED TASK
# This is the ONLY thing the agent is allowed to work on right now.

---

## CURRENT TASK

Phase: 0
Task ID: 0.10
Task Name: Grounded Extraction Bridge
From MASTER_PLAN.md: Phase 0, TASK 0.10

---

## EXACT ACTION

Create `agent/modules/grounded_bridge.py` with `GroundedExtractionBridge` class. Methods: `bridge_extraction(raw_results, context_fingerprint)` converts raw LLM results into `ExecutableKnowledgeUnit` objects. It must attach the `context_fingerprint` to each EKU and set initial `verification_status="candidate"`.

---

## FILES TO TOUCH

- agent/modules/grounded_bridge.py only (create new file)

---

## DONE WHEN

- [ ] `bridge_extraction(['result1', 'result2'], fingerprint)` returns 2 EKU objects
- [ ] Each EKU has the correct fingerprint attached
- [ ] Each EKU status is `"candidate"`
- [ ] PROGRESS.md updated

---

## HOW TO UPDATE THIS FILE WHEN TASK IS COMPLETE

Replace the contents with the next task from MASTER_PLAN.md.
Next task after this one: Phase 0, TASK 0.11 (Recursive Topic Explorer)
