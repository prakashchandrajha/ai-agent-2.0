Phase: 1
Task ID: 1.3
Task Name: Near-Failure Detection
From MASTER_PLAN.md: Phase 1, TASK 1.3
Exact Action: Extend SandboxResult in agent/sandbox/runner.py with robustness_score and fragility_flags fields. After execution calculate: NEAR_TIMEOUT if elapsed > 80% of timeout, WARNINGS_PRESENT if stderr non-empty but passed, SUSPICIOUSLY_FAST if elapsed < 5ms and code > 100 chars.
Files to touch: agent/sandbox/runner.py only
Done when:
- SandboxResult has robustness_score float field
- SandboxResult has fragility_flags list field
- Code that runs near timeout gets NEAR_TIMEOUT flag and robustness_score < 1.0