Phase: 1
Task ID: 1.NEW-B
Task Name: Sandbox Warm Pool
From MASTER_PLAN.md: Phase 1, TASK 1.NEW-B
Exact Action: Create agent/sandbox/pool.py with SandboxPool class. Pre-warm 3 sandbox runners. execute() takes warm runner, replaces it with fresh after use. Enable via feature flag sandbox_pool.
Files to touch: agent/sandbox/pool.py only (create new file)
Done when:
- SandboxPool initializes with 3 runners
- execute() returns result and replaces used runner
- handle_all_crashed() recreates all 3 runners
- Works with feature_enabled('sandbox_pool') flag