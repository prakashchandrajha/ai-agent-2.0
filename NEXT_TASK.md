# NEXT_TASK.md
# CURRENT TASK — UPDATE THIS AFTER EVERY COMPLETED TASK
# This is the ONLY thing the agent is allowed to work on right now.

---

## CURRENT TASK

Phase: 0
Task ID: 0.7
Task Name: Semantic Correction Engine
From MASTER_PLAN.md: Phase 0, TASK 0.7

---

## EXACT ACTION

Create `agent/knowledge/semantic_correction.py` with `SemanticCorrector` class. Methods: `correct_typo(term, known_terms)` returns the best match from `known_terms` if similarity is high enough, else original. Implement fuzzy string matching (Levenshtein distance) using stdlib or a minimal dependency.

---

## FILES TO TOUCH

- agent/knowledge/semantic_correction.py only (create new file)

---

## DONE WHEN

- [ ] `correct_typo('pythn', ['python', 'javascript'])` returns `'python'`
- [ ] `correct_typo('xyz', ['python', 'javascript'])` returns `'xyz'` (no match)
- [ ] PROGRESS.md updated

---

## HOW TO UPDATE THIS FILE WHEN TASK IS COMPLETE

Replace the contents with the next task from MASTER_PLAN.md.
Next task after this one: Phase 0, TASK 0.8 (Adversarial Prompt Guard)
