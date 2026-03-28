Phase: 0
Task ID: 0.NEW-O
Task Name: Source URL Deduplication
From MASTER_PLAN.md: Phase 0, TASK 0.NEW-O
Exact Action: Add dedupe_urls_by_domain() function to agent/modules/collector.py. Already exists from Task 0.10 — verify it is exported and works correctly. Max 2 URLs per domain, sorted by authority score first.
Files to touch: agent/modules/collector.py only
Done when:
- 3 URLs from same domain → only 2 returned
- Official docs domain kept over random blog when both present
- Function is importable from agent.modules.collector
