Phase: 1
Task ID: 1.NEW-A
Task Name: Assertion Independence Verification
From MASTER_PLAN.md: Phase 1, TASK 1.NEW-A
Exact Action: Add verify_assertion_uses_actual_output() function to agent/modules/executor.py. After assertion generation, verify assertions reference the real output not a contradicting value. If invalid: log warning and regenerate.
Files to touch: agent/modules/executor.py only
Done when:
- verify_assertion_uses_actual_output(assertions, actual_output) returns True when assertions match output
- returns False when assertions contradict actual output