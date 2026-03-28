# NEXT_TASK.md
# CURRENT TASK — UPDATE THIS AFTER EVERY COMPLETED TASK
# This is the ONLY thing the agent is allowed to work on right now.

---

## CURRENT TASK

Phase: 0
Task ID: 0.5
Task Name: Fix JSON Extraction + Think Tags
From MASTER_PLAN.md: Phase 0, TASK 0.5

---

## EXACT ACTION

Update `extract_json()` in `agent/llm/helpers.py` to:
1. Strip `<think>...</think>` tags using `re.DOTALL`.
2. Find the first `{` or `[` and extract the substring.
3. Handle markdown code fences (```json ... ```).

---

## FILES TO TOUCH

- agent/llm/helpers.py

---

## DONE WHEN

- [ ] `extract_json("<think>reasoning</think>{\"key\": \"val\"}")` returns `{"key": "val"}`
- [ ] `extract_json("Here is the JSON: \n\n ```json\n[1,2,3]\n```")` returns `[1,2,3]`
- [ ] PROGRESS.md updated

---

## HOW TO UPDATE THIS FILE WHEN TASK IS COMPLETE

Replace the contents with the next task from MASTER_PLAN.md.
Next task after this one: Phase 0, TASK 0.6 (Mandatory Semantic Dimensions)
