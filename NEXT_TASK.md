Phase: 0
Task ID: 0.NEW-N
Task Name: Atomic Learning Sessions
From MASTER_PLAN.md: Phase 0, TASK 0.NEW-N
Exact Action: Create agent/utils/atomic_session.py with AtomicLearningSession class. If commit() is never called, cleanup removes all temp files automatically. Must work as context manager.
Files to touch: agent/utils/atomic_session.py only (create new file)
Done when:
- Session saves to temp location
- commit() moves to final location atomically
- If exception occurs before commit, temp files are cleaned up automatically
- Works as context manager with: with AtomicLearningSession('concept') as session:
