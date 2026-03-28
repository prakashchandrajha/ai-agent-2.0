Phase: 0
Task ID: 0.10
Task Name: Fix Scraper Failure Tracking
From MASTER_PLAN.md: Phase 0, TASK 0.10
Exact Action: Fix collect() in agent/modules/collector.py to abort when scraping failure rate exceeds 50% and zero successes. Must raise ScrapingThresholdError with clear message. Also deduplicate URLs by domain before scraping using dedupe_urls_by_domain().
Files to touch: agent/modules/collector.py only
Done when:
- If 3 out of 3 URLs fail, ScrapingThresholdError is raised
- If 1 out of 3 URLs succeed, no error raised
- dedupe_urls_by_domain() exists and limits to max 2 per domain
