Phase: 0
Task ID: 0.NEW-M
Task Name: Smart Chunking by Content Type
From MASTER_PLAN.md: Phase 0, TASK 0.NEW-M
Exact Action: Add smart_chunk() function to agent/services/chunker.py. Detects content type from source URL and applies different chunking strategy: API/reference URLs get small chunks (max 200 tokens), tutorial URLs get large chunks (max 600 tokens), default gets overlapping chunks (max 400 tokens, overlap 100).
Files to touch: agent/services/chunker.py only
Done when:
- smart_chunk(content, 'https://docs.python.org/3/library/functions.html') uses small chunks
- smart_chunk(content, 'https://realpython.com/python-tutorial/') uses large chunks
- smart_chunk(content, 'https://random-blog.com') uses default chunks
