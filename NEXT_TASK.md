# NEXT_TASK.md
# CURRENT TASK — UPDATE THIS AFTER EVERY COMPLETED TASK
# This is the ONLY thing the agent is allowed to work on right now.

---

## CURRENT TASK

Phase: 0
Task ID: 0.2
Task Name: Fix Scraper HTML Stripping
From MASTER_PLAN.md: Phase 0, TASK 0.2

---

## EXACT ACTION

Update `agent/scraper/html_utils.py` to use BeautifulSoup for aggressive HTML stripping. Ensure all tags (except <code> and <pre>) are removed, and only meaningful text and code blocks are preserved. Implement `strip_html(html: str) -> str`.

---

## FILES TO TOUCH

- agent/scraper/html_utils.py

---

## DONE WHEN

- [ ] `agent/scraper/html_utils.py` uses BeautifulSoup for stripping
- [ ] python -c "from agent.scraper.html_utils import strip_html; h='<div><p>Hello</p><script>alert(1)</script><code>print(1)</code></div>'; print(strip_html(h))" prints "Hello\nprint(1)" (or similar clean text)
- [ ] PROGRESS.md updated

---

## HOW TO UPDATE THIS FILE WHEN TASK IS COMPLETE

Replace the contents with the next task from MASTER_PLAN.md.
Next task after this one: Phase 0, TASK 0.3 (Mandatory EKU Semantic Dimensions)
