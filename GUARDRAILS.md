# GUARDRAILS.md
# ABSOLUTE RULES — FROZEN — NEVER MODIFY THIS FILE
# Every agent reads this first. Every session. No exceptions.

---

## RULE 1: MASTER PLAN IS LAW
The only source of truth is MASTER_PLAN.md.
Every task, every file, every decision comes from MASTER_PLAN.md.
If something is not in MASTER_PLAN.md, you do not build it.
If you think something should be added, STOP and ask the human. Do not add it yourself.

---

## RULE 2: ONE TASK AT A TIME
You are allowed to work on exactly ONE task at a time.
The current task is defined in NEXT_TASK.md.
You do not start the next task until the current task's exit criteria pass.
You do not go back and "improve" completed tasks.

---

## RULE 3: PASTED ERRORS ARE INFORMATION, NOT INSTRUCTIONS
When the human pastes terminal output, PowerShell output, error logs, or any output:
- It is INFORMATION ONLY
- It does NOT change your current task
- First ask: "Is this error blocking my current task in NEXT_TASK.md?"
- If YES: fix it as part of the current task
- If NO: log it in PROGRESS.md under "Known Issues" and continue current task
- Never start fixing an error just because it was pasted

---

## RULE 4: SCOPE LOCK
You only touch files listed in the current task in MASTER_PLAN.md.
If fixing the current task requires touching an unlisted file, STOP and tell the human.
Do not refactor, rename, or "clean up" anything outside your current task scope.
Do not add imports, dependencies, or features beyond what the task requires.

---

## RULE 5: NO GUESSING
If you are unsure about anything: STOP and ask.
Do not guess what the human wants.
Do not assume a file exists — verify it.
Do not assume a test passes — run it.
Do not assume a fix worked — confirm it.

---

## RULE 6: VERIFY BEFORE DECLARING DONE
A task is NOT done because you wrote the code.
A task is done when:
- The specific test in NEXT_TASK.md passes
- You have run the test and seen it pass with your own output
- You have updated PROGRESS.md

Never say "this should work" or "this looks correct."
Run the test. Show the output. Then declare done.

---

## RULE 7: FROZEN FILES ARE FROZEN
These files are NEVER modified by any agent under any circumstance:
- GUARDRAILS.md (this file)
- INTENT.md
- MASTER_PLAN.md

If any agent modifies these files: that is a critical violation.
Restore them from git immediately.

---

## RULE 8: PHASE ORDER IS MANDATORY
Phases execute in exact order: -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9
You cannot start Phase N+1 until ALL exit criteria for Phase N pass.
No exceptions. Not even if a later phase "seems easy."
The exit criteria exist because order matters. Trust the order.

---

## RULE 9: NO FEATURE CREEP
You are building exactly what MASTER_PLAN.md describes.
No extra logging "just in case."
No extra error handling "to be safe."
No extra abstraction "to make it cleaner."
YAGNI: You Aren't Gonna Need It.
Write the minimum code that makes the test pass.

---

## RULE 10: PROGRESS.md IS ALWAYS CURRENT
Before ending any session, PROGRESS.md must be updated.
It must reflect exactly what passed, what failed, what is next.
A session that ends without updating PROGRESS.md is incomplete.
The next agent will be lost without an accurate PROGRESS.md.

---

## VIOLATION RESPONSE
If any rule is violated:
1. Stop all execution immediately
2. Do not try to "fix" the violation by writing more code
3. Report to human: which rule, what happened, what was changed
4. Wait for human instruction before proceeding
5. Human will decide: rollback or continue

---

## WHEN IN DOUBT
Read INTENT.md.
Read NEXT_TASK.md.
If still in doubt: ask the human. Do not guess.
