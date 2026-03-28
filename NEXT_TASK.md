Phase: 1
Task ID: 1.2
Task Name: Create Source Authority Module
From MASTER_PLAN.md: Phase 1, TASK 1.2
Exact Action: Create agent/utils/source_authority.py with AUTHORITY_SCORES dict and get_authority(url) function. Official docs get 1.0, community sites get 0.65-0.75, unknown gets 0.50 default.
Files to touch: agent/utils/source_authority.py only (create new file)
Done when:
- get_authority('https://docs.python.org/3/library/list.html') returns 1.0
- get_authority('https://stackoverflow.com/questions/1') returns 0.65
- get_authority('https://some-random-blog.com') returns 0.50