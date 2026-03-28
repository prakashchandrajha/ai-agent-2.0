# ADVICE.md — Issues to Fix Before End-to-End Run
# Created: 2026-03-28 from full codebase audit
# Fix these when relevant. Do NOT fix out of sequence.

---

## 🔴 MUST FIX (Blocks learning pipeline)

### 1. executor.py — ExecutionResults class broken
- Missing `@dataclass` decorator → `field(default_factory=list)` won't work
- `pass_rate` and `all_results` properties orphaned inside `verify_assertion_uses_actual_output()` (dead code after `return True`)
- `compressor.py` calls both → **will crash at runtime**
- **Fix:** Add `@dataclass`, move properties back into class body

### 2. client.py — json_mode=False silently ignored
- `_generate_ollama()` hardcodes `"format": "json"` (line 99)
- `generate()` has no `json_mode` parameter
- `executor.py:212` passes `json_mode=False` → kwarg ignored silently
- Assertion generation gets JSON when it needs raw code
- **Fix:** Add `json_mode` param to `generate()`, conditionally include `"format": "json"`

### 3. validate_code() not wired into executor
- `code_validator.py` exists but never called before sandbox runs
- MASTER_PLAN: "Before EVERY sandbox call, run validate_code(code)"
- **Fix:** Import and call `validate_code()` in executor before `self.sandbox.run()`

---

## 🟡 SHOULD FIX (Quality improvements)

### 4. config.py — feature_enabled() missing env override
- MASTER_PLAN says check `FEATURE_<FLAG>` env var for testing
- Current: only checks dict
- **Fix:** Add `os.environ.get(f"FEATURE_{flag.upper()}")` check

### 5. collector.py — duplicate authority scoring
- Has inline `get_authority_score()` duplicating `source_authority.get_authority()`
- **Fix:** Replace inline function with import from `agent.utils.source_authority`

### 6. eku_store.py — contradiction gate too strict
- MASTER_PLAN: reject if existing > new + 0.15
- Current: rejects if ANY existing is higher at all
- Missing `GateDiagnostic` append and version bumping
- **Fix:** Add 0.15 margin, append diagnostic, bump version on replacement

### 7. cache.py — wrong timestamp
- Line 70: `os.path.getmtime(os.getcwd())` should be `time.time()`

### 8. runner.py — has_error vs passed mismatch
- `has_error` returns True if stderr non-empty
- `passed` only checks return_code == 0
- A test can be passed=True AND has_error=True simultaneously

---

## ℹ️ KNOWN ISSUES (from PROGRESS.md, fix when relevant)

- DDG rate limiting: web_search.py has no rate limit protection
- SQLite version: not checked in preflight
- Pre-commit hook uses /usr/bin/python but pytest is in .venv

---

## WIRING GAPS (wire during relevant Phase tasks)

| Module | Wire Point | When |
|--------|-----------|------|
| `validate_code()` | Before sandbox.run() in executor | Phase 1 |
| `source_authority.get_authority()` | Replace collector inline scoring | Phase 1 |
| `context_fingerprint` | Save when EKU stored, check before use | Phase 1-3 |
| `version_bounds` check | In collector during scraping | Phase 1-3 |
| `hazard_registry` | In task executor prompt injection | Phase 3 |
| `effective_confidence` | In task executor decisions | Phase 3 |
