# INTENT.md
# PROJECT PURPOSE — FROZEN — NEVER MODIFY THIS FILE
# One sentence. Always true. Read this when lost.

---

## THE INTENT (15 words)

Build a universal learning agent that verifies knowledge through execution before storing it.

---

## WHAT THIS MEANS (read when confused about a decision)

The agent learns concepts by:
1. Collecting knowledge from authoritative sources
2. Verifying that knowledge by actually running code
3. Storing only what has been proven to work
4. Using that verified knowledge to solve real tasks

The agent never stores what it has not proven.
The agent never claims confidence it has not earned.
The agent knows exactly what it knows and what it does not know.

---

## WHAT THIS PROJECT IS NOT

This is NOT a general-purpose chatbot.
This is NOT a code generator that guesses.
This is NOT a wrapper around an LLM.
This is NOT a web scraper.
This is NOT a search engine.

It is a verified knowledge store with an execution-backed learning loop.

---

## THE ONE QUESTION FOR EVERY DECISION

When you are unsure whether to do something, ask:

> "Does this make the agent more certain about what it knows,
>  or does it make the agent faster at guessing?"

If the answer is "faster at guessing": do not do it.
If the answer is "more certain about what it knows": it belongs in this project.

---

## THE NORTH STAR CAPABILITY

When complete, the agent will be able to say:

"I know that list.append modifies in-place and returns None.
 I know this because I ran 9 tests proving it.
 My confidence is 0.82 based on 3 authoritative sources.
 Source: docs.python.org.
 I do not know asyncio. Learn it first if you need it."

That is the goal. Every line of code serves that goal.

---

## CURRENT PROJECT STATE (update only this section when phases complete)

Phase -2: Foundation Audit — COMPLETE ✅
Phase -1: Pre-Flight — COMPLETE ✅
Phase 0:  Foundation Stabilization — NOT STARTED
Phase 1:  First Working Learning Loop — NOT STARTED
Phase 2:  Knowledge Intelligence Layer — NOT STARTED
Phase 3:  Task Execution Engine — NOT STARTED
Phase 4:  Multi-Language Support — NOT STARTED
Phase 5:  Adversarial Testing — NOT STARTED
Phase 6:  ChromaDB Semantic Search — NOT STARTED
Phase 7:  Knowledge Lifecycle — NOT STARTED
Phase 8:  Self-Improvement Systems — NOT STARTED
Phase 9:  Production Hardening — NOT STARTED
