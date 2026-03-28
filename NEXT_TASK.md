# NEXT_TASK.md
# CURRENT TASK — UPDATE THIS AFTER EVERY COMPLETED TASK
# This is the ONLY thing the agent is allowed to work on right now.

---

## CURRENT TASK

Phase: 0
Task ID: 0.5
Task Name: LLMClient non-JSON mode
From MASTER_PLAN.md: Phase 0, TASK 0.5

---

## EXACT ACTION

Add `json_mode=True` parameter to `LLMClient.generate()`. When `False`, the client must NOT force JSON format in the Ollama API call. Ensure `agent/llm/client.py` and any relevant adapters are updated.

---

## FILES TO TOUCH

- agent/llm/client.py

---

## DONE WHEN

- [ ] `LLMClient.generate(prompt, json_mode=False)` returns raw text/code
- [ ] `LLMClient.generate(prompt, json_mode=True)` (default) returns JSON as before
- [ ] PROGRESS.md updated

---

## HOW TO UPDATE THIS FILE WHEN TASK IS COMPLETE

Replace the contents with the next task from MASTER_PLAN.md.
Next task after this one: Phase 0, TASK 0.6 (Verify ChromaDB Connectivity)
