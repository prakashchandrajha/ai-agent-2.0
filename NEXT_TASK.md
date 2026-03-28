# NEXT_TASK.md
# CURRENT TASK — UPDATE THIS AFTER EVERY COMPLETED TASK
# This is the ONLY thing the agent is allowed to work on right now.

---

## CURRENT TASK

Phase: 0
Task ID: 0.NEW-K
Task Name: Composition Hazard Registry
From MASTER_PLAN.md: Phase 0, TASK 0.NEW-K

---

## EXACT ACTION

Create `agent/knowledge/hazard_registry.py` with `CompositionHazard` dataclass (fields: `concepts`, `hazard`, `mitigation`, `severity`). Implement `check_composition_hazards(required_concepts)` function. Populate `ALL_HAZARDS` with at least 3 common hazards (e.g., dict modification during iteration, async callbacks in forEach).

---

## FILES TO TOUCH

- agent/knowledge/hazard_registry.py only (create new file)

---

## DONE WHEN

- [ ] `CompositionHazard` dataclass is defined
- [ ] `check_composition_hazards(['dict iteration', 'dict modification'])` returns the relevant hazard
- [ ] `check_composition_hazards(['safe concept'])` returns an empty list
- [ ] PROGRESS.md updated

---

## HOW TO UPDATE THIS FILE WHEN TASK IS COMPLETE

Replace the contents with the next task from MASTER_PLAN.md.
Next task after this one: Phase 0, TASK 0.NEW-L (Transitive Confidence Calculator)
