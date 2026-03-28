# NEXT_TASK.md
Phase: 1
Task ID: 1.1
Task Name: Fix Circular Verification
From MASTER_PLAN.md: Phase 1, TASK 1.1 [CRITICAL]
Exact Action: Split executor.py test generation into TWO separate LLM calls. Call 1 generates code only. Sandbox runs it and gets REAL output. Call 2 generates assertions FROM the real output. Add CODE_GENERATOR_PROMPT and ASSERTION_GENERATOR_PROMPT to prompts.py.
Files to touch: agent/modules/executor.py and agent/llm/prompts.py
Done when: LLM cannot confirm imagined output — assertions only use real sandbox output