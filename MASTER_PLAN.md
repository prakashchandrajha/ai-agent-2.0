# MASTER PLAN — UNIVERSAL ENGINEER AGENT
### The single document you follow. Built from deep analysis of PROJECT_BIBLE + review_report + review_report_2.
### Every conflict resolved. Every duplication removed. Every task sequenced perfectly.
### Last Updated: 2026-03-27

---

## HOW TO READ THIS DOCUMENT

- **Follow phases in exact order. Never skip.**
- Every phase has EXIT CRITERIA. You do not move forward until ALL pass.
- Tasks marked `[CRITICAL]` — if you skip these, the project fails silently.
- Tasks marked `[NEW]` — not in PROJECT_BIBLE, added by reviewers.
- Time estimates are realistic (not best-case).
- Source key: `[B]` = PROJECT_BIBLE, `[R1]` = review_report, `[R2]` = review_report_2

---

## SYNTHESIS DECISIONS (CONFLICTS RESOLVED)

| Conflict | Decision | Reason |
|----------|----------|--------|
| Timeline: Bible=37h, R1=44h, R2=54h | **Follow R2 timeline (54-57h)** | R2 includes R1 includes Bible. All enhancements are additive. |
| Phase numbering: Bible uses Sprint 0-9, R2 adds Phase -2 and -1 | **Use Phase -2, -1, 0-9** | More phases = more safety. Foundation audit is critical. |
| R2 Discovery 1-7 (new bugs nobody caught) | **ALL implemented** | Zero theoretical — all have concrete failure modes |
| R1 vs R2 on pre-flight: R1 creates it, R2 says "execute as documented" | **R1 creates it (Sprint -1), execute before Phase 0** | Both agree. No conflict. |
| Smart chunking: R1=Sprint 0 LOW priority | **Keep in Sprint 0** | 15 minutes, meaningful quality gain |

---

## WHAT YOU HAVE RIGHT NOW (HONEST TRUTH)

**Phases 0 through 2.5 are complete.** This means:
- Config loads. Sandbox runs. EKU schema exists. ChromaDB connected.
- Scrapling fetches. Semantic chunker splits. DAG rollback exists.
- CLI accepts commands. Pre-validator does disambiguation.

**What has NEVER run even once:** a complete learning loop. No concept has been fed in,
verified by execution, failed intentionally, recovered from failure, and stored.
The intelligence layer is zero. You have the most sophisticated empty container ever built.

**Three .env values wrong right now — fix before anything else:**
```
MAX_LEARNING_ITERATIONS=1   → Change to 3
ENTROPY_THRESHOLD=0.92      → Change to 0.85
DEFAULT_MODEL=phi3:medium   → Keep this
```

---

## TOTAL TIMELINE

| Phase | Name | Duration | Depends On |
|-------|------|----------|------------|
| **Phase -2** | Foundation Audit | 2 hours | Nothing |
| **Phase -1** | Pre-Flight | 30 min | Phase -2 |
| **Phase 0** | Foundation Stabilization | 6-7 hours | Phase -1 |
| **Phase 1** | First Working Learning Loop | 8-9 hours | Phase 0 |
| **Phase 2** | Knowledge Intelligence Layer | 5 hours | Phase 1 |
| **Phase 3** | Task Execution Engine | 7 hours | Phase 2 |
| **Phase 4** | Multi-Language Support | 4 hours | Phase 1 (parallel with 2-3) |
| **Phase 5** | Adversarial Testing + Prediction | 5 hours | Phase 3 |
| **Phase 6** | Semantic Search (ChromaDB) | 4 hours | Phase 2 (parallel with 5) |
| **Phase 7** | Knowledge Lifecycle | 4 hours | Phase 5 + 6 |
| **Phase 8** | Self-Improvement Systems | 4 hours | Phase 7 |
| **Phase 9** | Production Hardening | 4 hours | All phases |
| **TOTAL** | | **54–57 hours** | |

---

---

# PHASE -2: FOUNDATION AUDIT
**Duration:** 2 hours
**Depends on:** Nothing
**Why:** Before building anything, verify what you have actually works. R2 adds this. It is not in the Bible. It is CRITICAL — you cannot build on a broken foundation.

---

## TASK -2.1: Run Every Existing Module in Isolation
**Time:** 45 minutes

Run each module below independently and document: works / fails / needs fix.

```bash
# web_search.py — Does DDG actually return results?
python -c "from agent.services.web_search import search; print(search('python list append'))"

# web_scraper.py — Does Scrapling extract content?
python -c "from agent.services.web_scraper import scrape_page; print(scrape_page('https://docs.python.org/3/tutorial/datastructures.html')[:500])"

# chunker.py — Does tiktoken produce valid chunks?
python -c "from agent.services.chunker import chunk_text; chunks = chunk_text('test ' * 1000); print(len(chunks), 'chunks')"

# embedder.py — Does sentence-transformers produce embeddings?
python -c "from agent.services.embedder import embed_text; v = embed_text('hello world'); print(len(v), 'dimensions')"

# sandbox/runner.py — Does isolation actually isolate?
python -c "from agent.sandbox.runner import SandboxRunner; r=SandboxRunner(); print(r.run('print(1+1)'))"

# llm/client.py — Does Ollama call work with phi3:medium?
python -c "from agent.llm.client import complete; print(complete('Say hello in one word')[:50])"
```

**Document results in:** `phase_minus2_audit.txt`
Record exactly which modules work and which fail.
Do NOT proceed until every module either works or has a filed bug.

---

## TASK -2.2: Dependency Conflict Check
**Time:** 30 minutes

```bash
# Generate conflict-free requirements.txt
pip check
pip list --format=freeze > requirements_current.txt

# Check for known problematic combinations:
# scrapling requires specific httpx version
# chromadb requires specific sqlite3 version
# sentence-transformers requires specific torch version

python -c "import scrapling; import chromadb; import sentence_transformers; print('No conflicts')"
```

If conflicts found: pin versions until `pip check` passes clean.
Output: `requirements.txt` with pinned versions.

---

## TASK -2.3: LLM Behavior Baseline
**Time:** 45 minutes

Run these 10 prompts through `phi3:medium` and document what it can and cannot do:

```python
# test_llm_baseline.py
tests = [
    # JSON reliability
    {"prompt": "Return JSON: {\"key\": \"value\"}", "expect": "valid JSON"},
    {"prompt": "Return JSON with nested object", "expect": "valid nested JSON"},
    
    # Code generation
    {"prompt": "Write Python: append 5 to list x=[1,2,3]. No explanation.", "expect": "code only"},
    {"prompt": "Write Python assertion for: x.append(5) where x=[1,2,3]", "expect": "assert x == [1,2,3,5]"},
    
    # Reasoning
    {"prompt": "What does list.append return in Python? One word answer.", "expect": "None"},
    {"prompt": "Step by step: what happens when you append to a full list?", "expect": "detailed steps"},
    
    # Failure modes
    {"prompt": "{{invalid json prompt", "expect": "graceful response"},
    {"prompt": "Return JSON: {this is broken", "expect": "graceful response"},
    
    # Temperature sensitivity
    {"prompt": "Pick a random number 1-10", "expect": "a number"},
    {"prompt": "Pick a random number 1-10", "expect": "same or different from above"},
]
```

**Document:** What phi3:medium does reliably, what breaks it, temperature behavior.
This prevents Sprint 1 failures from model limitations you could have known about.

---

## PHASE -2 EXIT CRITERIA

```bash
# All must be true before Phase -1:
✓ phase_minus2_audit.txt exists documenting every module
✓ Every module either works or has explicit bug filed
✓ requirements.txt has pinned versions with zero conflicts (pip check clean)
✓ LLM baseline documented — know exactly what phi3:medium can/cannot do
```

---

---

# PHASE -1: PRE-FLIGHT
**Duration:** 30 minutes
**Depends on:** Phase -2 complete
**Goal:** One script that tells you GREEN (proceed) or RED (fix this first).

---

## TASK -1.1: Create preflight_check.py [NEW from R1]
**Time:** 30 minutes
**File:** `preflight_check.py` (root directory)

```python
#!/usr/bin/env python3
"""
Pre-flight check. Run this before anything else.
Output: ALL GREEN = proceed. Any RED = fix before continuing.
"""
import sys
import subprocess
import shutil
from pathlib import Path

checks = []

def check(name: str, passed: bool, fix_command: str = ""):
    status = "✅ GREEN" if passed else "❌ RED"
    checks.append((name, passed, fix_command))
    print(f"{status}: {name}")
    if not passed and fix_command:
        print(f"       FIX: {fix_command}")

# Check 1: Python >= 3.10
import sys
check("Python >= 3.10", sys.version_info >= (3, 10),
      "Install Python 3.10+ from python.org")

# Check 2: Ollama running + phi3:medium pulled
try:
    result = subprocess.run(["ollama", "list"], capture_output=True, text=True, timeout=5)
    ollama_running = result.returncode == 0
    phi3_available = "phi3:medium" in result.stdout
except Exception:
    ollama_running = False
    phi3_available = False

check("Ollama running", ollama_running, "ollama serve &")
check("phi3:medium available", phi3_available, "ollama pull phi3:medium")

# Check 3: Node.js >= 18 (needed for Phase 4)
node_path = shutil.which("node")
if node_path:
    result = subprocess.run(["node", "--version"], capture_output=True, text=True)
    version = result.stdout.strip()  # "v18.0.0"
    major = int(version.lstrip("v").split(".")[0])
    check("Node.js >= 18", major >= 18, "Install Node.js 18+ from nodejs.org")
else:
    check("Node.js >= 18", False, "Install Node.js 18+ from nodejs.org")

# Check 4: Required directories exist
required_dirs = ["data/", "data/logs/", "data/ekus/", "data/chromadb/", "data/tmp/", "data/llm_cache/"]
for d in required_dirs:
    Path(d).mkdir(parents=True, exist_ok=True)
check("Required directories", True, "")  # Created above

# Check 5: .env file with required keys
required_env_keys = [
    "MAX_LEARNING_ITERATIONS", "ENTROPY_THRESHOLD", "DEFAULT_MODEL",
    "CHROMADB_PATH", "SANDBOX_TIMEOUT",
]
if Path(".env").exists():
    env_content = Path(".env").read_text()
    missing = [k for k in required_env_keys if k not in env_content]
    check(f".env has all required keys", len(missing) == 0,
          f"Add missing keys to .env: {missing}")
else:
    check(".env file exists", False, "cp .env.example .env && edit values")

# Check 6: Network connectivity
import urllib.request
try:
    urllib.request.urlopen("https://docs.python.org", timeout=5)
    check("Network connectivity to docs.python.org", True)
except Exception:
    check("Network connectivity to docs.python.org", False, "Check internet connection")

# Check 7: Disk space >= 500MB
import shutil as sh
free_bytes = sh.disk_usage(".").free
check(f"Disk space >= 500MB (have {free_bytes // (1024**2)}MB)",
      free_bytes > 500 * 1024 * 1024,
      "Free up disk space")

# Check 8: Key packages importable
packages = [
    ("scrapling", "pip install scrapling"),
    ("chromadb", "pip install chromadb"),
    ("sentence_transformers", "pip install sentence-transformers"),
    ("tiktoken", "pip install tiktoken"),
    ("rich", "pip install rich"),
]
for pkg, fix in packages:
    try:
        __import__(pkg)
        check(f"Package: {pkg}", True)
    except ImportError:
        check(f"Package: {pkg}", False, fix)

# Final report
print("\n" + "="*50)
all_passed = all(p for _, p, _ in checks)
if all_passed:
    print("✅ ALL GREEN — Proceed to Phase 0")
else:
    failed = [n for n, p, _ in checks if not p]
    print(f"❌ {len(failed)} checks failed. Fix RED items before proceeding.")
    sys.exit(1)
```

**Run it:**
```bash
python preflight_check.py
# Must show: ALL GREEN — Proceed to Phase 0
```

---

## PHASE -1 EXIT CRITERIA

```bash
python preflight_check.py
# Output: ALL GREEN — Proceed to Phase 0
```

---

---

# PHASE 0: FOUNDATION STABILIZATION
**Duration:** 6-7 hours
**Depends on:** Phase -1 ALL GREEN
**Goal:** Fix all bugs. Extend schema. Add safety systems. Make infrastructure trustworthy.

**IMPORTANT:** Do phases 0A → 0B → 0C → 0D → 0E → 0F in order.

---

## PHASE 0A — CRITICAL INFRASTRUCTURE (2.5 hours)

### TASK 0.0: Extend EKU Schema [B]
**File:** `agent/knowledge/eku_schema.py`
**Time:** 30 minutes

Add these 15 fields to `ExecutableKnowledgeUnit` dataclass:

```python
# Confidence detail
confidence_breakdown: dict = field(default_factory=dict)
# {"execution": 0.8, "documentation": 0.9, "edge_cases": 0.7, "transfer": 0.6, "prediction": 0.5}

# Constraint system
hard_constraints: list = field(default_factory=list)     # MUST be true
soft_constraints: list = field(default_factory=list)     # SHOULD be true
violated_constraints_log: list = field(default_factory=list)  # every violation ever

# Execution traces
canonical_traces: list = field(default_factory=list)     # representative traces
trace_patterns: list = field(default_factory=list)       # abstracted behavior patterns

# Prediction tracking
prediction_accuracy: float = 0.0
prediction_history: list = field(default_factory=list)
confusion_gaps: list = field(default_factory=list)       # wrong predictions — most valuable

# Transfer
micro_skills: list = field(default_factory=list)         # language-agnostic patterns

# Lifecycle
last_used_timestamp: str = ""
usage_count: int = 0
decay_score: float = 0.0                                 # 0=fresh, 1=fully decayed

# Safety
state_sensitive: bool = False
context_dependencies: list = field(default_factory=list)

# Quality metrics
avg_robustness_score: float = 1.0
fragility_flags: list = field(default_factory=list)      # NEAR_TIMEOUT, WARNINGS_PRESENT

# Source tracking
source_urls: list = field(default_factory=list)
avg_source_authority: float = 0.0

# Contract tracking
mastery_criteria_met: list = field(default_factory=list)
mastery_criteria_unmet: list = field(default_factory=list)
gate_diagnostics: list = field(default_factory=list)

# NEW from R2 — version awareness
version_bounds: dict = field(default_factory=dict)
# {"min_version": "3.8", "max_version": None, "deprecated_in": None, "removed_in": None}

# NEW from R2 — context fingerprint
context_fingerprint: dict = field(default_factory=dict)
# {"file_hashes": {}, "dependency_versions": {}, "runtime_version": "", "computed_at": ""}
```

Add 3 new dataclasses:

```python
@dataclass
class ExecutionTrace:
    code: str
    actual_output: str
    elapsed_ms: float
    test_category: str       # "normal", "edge", "extreme"
    passed: bool
    robustness_score: float

@dataclass
class Constraint:
    rule: str
    is_hard: bool            # True=hard, False=soft
    source: str              # "failure_inversion", "test_implication", "documentation"
    confidence: float
    violation_count: int = 0

@dataclass
class GateDiagnostic:
    gate_name: str
    failure_reason: str
    actual_value: float
    required_value: float
    suggested_fix: str
    is_retryable: bool
```

Update `to_dict()` and `from_dict()` for ALL new fields.

**Validation test:**
```python
def test_eku_roundtrip_all_new_fields():
    eku = ExecutableKnowledgeUnit()
    eku.hard_constraints = ["returns None"]
    eku.decay_score = 0.3
    eku.avg_source_authority = 0.9
    eku.version_bounds = {"min_version": "3.8"}
    eku.context_fingerprint = {"runtime_version": "3.11"}
    data = eku.to_dict()
    restored = ExecutableKnowledgeUnit.from_dict(data)
    assert restored.hard_constraints == ["returns None"]
    assert restored.decay_score == 0.3
    assert restored.version_bounds["min_version"] == "3.8"
```

---

### TASK 0.NEW-A: Create migrations.py [NEW from R1]
**File:** `agent/knowledge/migrations.py`
**Time:** 45 minutes

```python
SCHEMA_VERSION = "2.0.0"

MIGRATIONS = {
    "1.0.0 → 2.0.0": {
        "add_fields": [
            ("confidence_breakdown", {}),
            ("hard_constraints", []),
            ("soft_constraints", []),
            ("violated_constraints_log", []),
            ("canonical_traces", []),
            ("trace_patterns", []),
            ("prediction_accuracy", 0.0),
            ("prediction_history", []),
            ("confusion_gaps", []),
            ("micro_skills", []),
            ("last_used_timestamp", ""),
            ("usage_count", 0),
            ("decay_score", 0.0),
            ("state_sensitive", False),
            ("context_dependencies", []),
            ("avg_robustness_score", 1.0),
            ("fragility_flags", []),
            ("source_urls", []),
            ("avg_source_authority", 0.0),
            ("mastery_criteria_met", []),
            ("mastery_criteria_unmet", []),
            ("gate_diagnostics", []),
            ("version_bounds", {}),
            ("context_fingerprint", {}),
            ("_schema_version", "2.0.0"),
        ],
    }
}

def migrate_eku(data: dict) -> dict:
    """Migrate old EKU JSON to current schema. Wire this as first line of from_dict()."""
    stored_version = data.get("_schema_version", "1.0.0")
    if stored_version == SCHEMA_VERSION:
        return data
    
    migration_key = f"{stored_version} → {SCHEMA_VERSION}"
    if migration_key not in MIGRATIONS:
        raise ValueError(f"No migration path from {stored_version} to {SCHEMA_VERSION}")
    
    migration = MIGRATIONS[migration_key]
    for field_name, default in migration["add_fields"]:
        if field_name not in data:
            data[field_name] = default
    
    return data
```

Wire into `eku_schema.py` `from_dict()`: `data = migrate_eku(data)` as FIRST LINE before parsing.

**Validation test:**
```python
def test_migration_upgrades_old_eku():
    old_eku = {"id": "123", "concept": "list.append", "confidence": 0.8}
    # Missing all new fields
    migrated = migrate_eku(old_eku)
    assert migrated["hard_constraints"] == []
    assert migrated["decay_score"] == 0.0
    assert migrated["version_bounds"] == {}
    assert migrated["_schema_version"] == "2.0.0"

def test_migration_handles_extra_field():
    old_eku = {"unknown_field": "value", "concept": "test"}
    migrated = migrate_eku(old_eku)
    assert "unknown_field" in migrated  # Extra field preserved, not deleted
```

---

### TASK 0.NEW-B: File Locking for JSON Stores [NEW from R1]
**File:** `agent/utils/file_lock.py`
**Time:** 30 minutes

```python
import fcntl
import json
from pathlib import Path
from contextlib import contextmanager

@contextmanager
def locked_file(path: Path, mode: str):
    """Cross-platform file locking for concurrent JSON access."""
    path = Path(path)
    f = open(path, mode)
    try:
        fcntl.flock(f.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        yield f
    except BlockingIOError:
        f.close()
        raise TimeoutError(f"Could not acquire lock on {path} within timeout")
    finally:
        try:
            fcntl.flock(f.fileno(), fcntl.LOCK_UN)
        except Exception:
            pass
        try:
            f.close()
        except Exception:
            pass

def atomic_json_write(path: Path, data: dict) -> None:
    """Write JSON atomically — reads and writes in single locked operation."""
    with locked_file(path, 'r+') as f:
        f.seek(0)
        json.dump(data, f, indent=2)
        f.truncate()
```

Wire into `eku_store.py` `_save_eku()`: replace direct writes with `atomic_json_write()`.

**Validation test:**
```python
def test_file_lock_prevents_concurrent_write():
    # Verify concurrent writes don't corrupt
    import threading
    path = Path("data/test_lock.json")
    path.write_text('{"count": 0}')
    
    def increment():
        for _ in range(10):
            with locked_file(path, 'r+') as f:
                data = json.load(f)
                data["count"] += 1
                f.seek(0); json.dump(data, f); f.truncate()
    
    threads = [threading.Thread(target=increment) for _ in range(5)]
    for t in threads: t.start()
    for t in threads: t.join()
    
    assert json.loads(path.read_text())["count"] == 50  # No lost writes
```

---

### TASK 0.NEW-C: Feature Flags System [NEW from R1]
**File:** `agent/config.py` (additions)
**Time:** 20 minutes

```python
import os

FEATURE_FLAGS = {
    "chromadb_enabled": False,      # Phase 6 enables
    "async_pipeline": False,        # Phase 3 enables
    "adversarial_tests": False,     # Phase 5 enables
    "decay_system": False,          # Phase 7 enables
    "experience_log": False,        # Phase 8 enables
    "multi_language": False,        # Phase 4 enables
    "sandbox_pool": False,          # Phase 1 enables
    "speculative_prefetch": False,  # Phase 3 enables
}

def feature_enabled(flag: str) -> bool:
    """Check feature flag. Env var overrides config (for testing)."""
    env_key = f"FEATURE_{flag.upper()}"
    if env_key in os.environ:
        return os.environ[env_key].lower() in ("true", "1", "yes")
    return FEATURE_FLAGS.get(flag, False)

def enable_feature(flag: str) -> None:
    """Enable a feature flag (call this at start of each phase)."""
    if flag not in FEATURE_FLAGS:
        raise ValueError(f"Unknown feature flag: {flag}")
    FEATURE_FLAGS[flag] = True
```

Graceful degradation rule: Every new feature wraps its execution with `if feature_enabled("name"):`.
When disabled, falls back to simpler working behavior. Never crashes when feature is off.

---

### TASK 0.1: Fix Sandbox Environment Isolation [B]
**File:** `agent/sandbox/runner.py`
**Time:** 15 minutes

Current code does `os.environ.copy()` — leaks API keys, PYTHONPATH conflicts, proxy settings.

Replace `_sandbox_env()` entirely:
```python
def _sandbox_env(self) -> dict[str, str]:
    """Minimal environment built from scratch. Nothing from parent process."""
    return {
        "PATH": "/usr/local/bin:/usr/bin:/bin",
        "HOME": str(Path.home()),
        "PYTHONPATH": str(self._sandbox_dir),
        "PYTHONDONTWRITEBYTECODE": "1",
        "PYTHONUNBUFFERED": "1",
        "LANG": "en_US.UTF-8",
    }
```

**Validation test:**
```python
def test_sandbox_env_has_exactly_6_keys():
    runner = SandboxRunner()
    env = runner._sandbox_env()
    assert len(env) == 6
    assert "OPENAI_API_KEY" not in env
    assert "ANTHROPIC_API_KEY" not in env
    assert "PYTHONPATH" in env
```

---

## PHASE 0B — BUG FIXES (1.5 hours)

### TASK 0.2: Fix Rollback Direction [B]
**File:** `agent/knowledge/eku_store.py`
**Time:** 25 minutes

Current bug: `rollback_eku()` walks UP to parents (wrong). Must walk DOWN to dependents.

```python
def rollback_eku(self, eku_id: str, dry_run: bool = False) -> list[str]:
    """
    ALWAYS call with dry_run=True first to see impact.
    dry_run=True: returns list of what WOULD be deleted, deletes nothing.
    dry_run=False: deletes everything in the impact list.
    """
    impact = self._find_all_downstream(eku_id)
    if not dry_run:
        for delete_id in impact:
            self._delete_single_eku(delete_id)
    return impact

def _find_all_downstream(self, eku_id: str) -> list[str]:
    """Find all EKUs whose .dependencies includes eku_id, recursively."""
    result = [eku_id]
    for stored_id in self._index:
        eku = self.load_eku(stored_id)
        if eku and eku_id in getattr(eku, 'dependencies', []):
            result.extend(self._find_all_downstream(stored_id))
    return list(set(result))
```

**Validation test:**
```python
def test_rollback_cascades_downstream_not_upstream():
    # A → B → C chain (C depends on B depends on A)
    impact = store.rollback_eku(A.id, dry_run=True)
    assert B.id in impact   # B depends on A → deleted
    assert C.id in impact   # C depends on B → deleted
    assert "root" not in impact  # Root NOT in impact (upstream)
    # Verify dry_run didn't actually delete
    assert store.load_eku(A.id) is not None
```

---

### TASK 0.3: Fix Contradiction Gate [B]
**File:** `agent/knowledge/eku_store.py`
**Time:** 15 minutes

Current bug: `_gate_no_contradictions()` always returns `True`. Fix:

```python
async def _gate_no_contradictions(self, eku: ExecutableKnowledgeUnit) -> bool:
    existing = self.find_by_topic(eku.domain, eku.topic)
    if not existing:
        return True
    
    best_existing = max(existing, key=lambda e: e.confidence)
    
    if best_existing.confidence > eku.confidence + 0.15:
        eku.gate_diagnostics.append(GateDiagnostic(
            gate_name="no_contradictions",
            failure_reason=f"Existing EKU is significantly better ({best_existing.confidence:.2f} vs {eku.confidence:.2f})",
            actual_value=eku.confidence,
            required_value=best_existing.confidence,
            suggested_fix="Run more iterations to improve confidence before replacing: MAX_LEARNING_ITERATIONS=5",
            is_retryable=True
        ))
        return False
    
    # New EKU is equal or better — allow replacement, bump version
    eku.version = best_existing.version + 1
    return True
```

---

### TASK 0.4: Create Pre-Execution Code Validator [B] [CRITICAL]
**New file:** `agent/modules/code_validator.py`
**Time:** 20 minutes

This is the wall between LLM-generated code and your sandbox. Nothing enters the sandbox without passing this.

```python
import re
from dataclasses import dataclass

@dataclass
class ValidationResult:
    is_safe: bool
    violations: list[str]
    suggestion: str

DANGEROUS_PATTERNS = [
    (r'\bimport\s+os\b',          "os module — filesystem access"),
    (r'\bimport\s+subprocess\b',  "subprocess — shell execution"),
    (r'\bimport\s+sys\b',         "sys — interpreter access"),
    (r'\b__import__\b',           "dynamic import bypass"),
    (r'\bopen\s*\(',              "file I/O"),
    (r'\bexec\s*\(',              "exec() — arbitrary code"),
    (r'\beval\s*\(',              "eval() — arbitrary expression"),
    (r'\bglobals\s*\(',           "globals() — scope escape"),
    (r'\bsocket\b',               "network socket"),
    (r'\burllib\b|\brequests\b',  "HTTP client"),
    (r'\bshutil\b',               "file operations"),
    (r'\bpickle\b',               "deserialization attack vector"),
    (r'\b__builtins__\b',         "builtins access"),
    (r'compile\s*\(',             "compile() — code generation"),
]

def validate_code(code: str) -> ValidationResult:
    violations = []
    for pattern, description in DANGEROUS_PATTERNS:
        if re.search(pattern, code):
            violations.append(description)
    
    is_safe = len(violations) == 0
    suggestion = "Remove dangerous patterns. Only use pure Python data structures and algorithms." if violations else ""
    
    return ValidationResult(is_safe=is_safe, violations=violations, suggestion=suggestion)
```

Wire into `executor.py`: **Before EVERY sandbox call**, run `validate_code(code)`.
If not safe: log violation, skip test, mark as `code_quality_failure` in test result.

---

### TASK 0.5: Fix JSON Extraction + Think Tags [B]
**File:** `agent/llm/helpers.py`
**Time:** 15 minutes

Current code breaks on `<think>...</think>` tags from deepseek-r1 and on JSON not starting at position 0.

```python
import re

def extract_json(content: str) -> dict | list | None:
    # Step 1: Strip reasoning model think tags (deepseek-r1, qwq, etc.)
    content = re.sub(r'<think>.*?</think>', '', content, flags=re.DOTALL)
    
    # Step 2: Strip markdown code fences
    content = re.sub(r'```(?:json)?\s*', '', content)
    content = content.replace('```', '')
    
    # Step 3: Find first JSON structure (object or array)
    first_brace = content.find('{')
    first_bracket = content.find('[')
    
    if first_brace == -1 and first_bracket == -1:
        return None
    
    # Take whichever comes first
    if first_brace == -1:
        start = first_bracket
    elif first_bracket == -1:
        start = first_brace
    else:
        start = min(first_brace, first_bracket)
    
    content = content[start:]
    
    # Step 4: Parse
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        # Try to find and extract just the first complete JSON object
        try:
            decoder = json.JSONDecoder()
            obj, _ = decoder.raw_decode(content)
            return obj
        except Exception:
            return None
```

**Validation tests:**
```python
def test_json_extractor_strips_think_tags():
    content = "<think>I need to think about this</think>\n{\"result\": \"done\"}"
    assert extract_json(content) == {"result": "done"}

def test_json_extractor_handles_nested_think_tags():
    content = "<think><think>nested</think>more text</think>{\"key\": 1}"
    assert extract_json(content) == {"key": 1}

def test_json_extractor_strips_markdown_fences():
    content = "```json\n{\"key\": \"value\"}\n```"
    assert extract_json(content) == {"key": "value"}

def test_json_extractor_strips_preamble():
    content = "Here is the JSON you requested:\n\n{\"result\": true}"
    assert extract_json(content) == {"result": True}
```

---

### TASK 0.NEW-D: Lazy Import Pattern (Circular Dependency Prevention) [NEW from R1]
**Files:** Multiple
**Time:** 15 minutes

Replace any top-level imports that create cycles with lazy imports:

```python
# WRONG — creates circular import:
from agent.knowledge.eku_store import EKUStore

# CORRECT — lazy import inside function:
def get_eku_store():
    from agent.knowledge.eku_store import EKUStore
    return EKUStore()

# CORRECT — type-only import that doesn't execute:
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from agent.knowledge.eku_store import EKUStore

def process(store: "EKUStore") -> None:  # Forward reference
    ...
```

Scan all files. Fix any circular imports found.

---

## PHASE 0C — PERFORMANCE INFRASTRUCTURE (1.5 hours)

### TASK 0.6: Create Session Logger [B]
**New file:** `agent/utils/session_logger.py`
**Time:** 20 minutes

```python
import json
import uuid
from pathlib import Path
from datetime import datetime

class SessionLogger:
    def __init__(self, concept: str):
        self._session_id = str(uuid.uuid4())[:8]
        self._concept = concept
        self._events = []
        self._path = Path(f"data/logs/session_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{self._session_id}.json")
    
    def log(self, phase: str, event: str, data: dict = None):
        self._events.append({
            "timestamp": datetime.now().isoformat(),
            "phase": phase,
            "event": event,
            "data": data or {}
        })
        # Write immediately — don't buffer (so crash doesn't lose logs)
        self._flush()
    
    def log_scrape_failure(self, url: str, reason: str = ""):
        self.log("collection", "scrape_failure", {"url": url, "reason": reason})
    
    def log_gate_failure(self, gate: str, diagnostic: dict):
        self.log("storage", "gate_failure", {"gate": gate, "diagnostic": diagnostic})
    
    def _flush(self):
        self._path.write_text(json.dumps({
            "session_id": self._session_id,
            "concept": self._concept,
            "events": self._events
        }, indent=2))
```

Wire into `orchestrator.py`: Create one `SessionLogger` per `learn()` call. Pass it down to all modules.

---

### TASK 0.NEW-E: LLM Response Cache [NEW from R1]
**New file:** `agent/llm/cache.py`
**Time:** 25 minutes

Same prompt + same model at temperature 0 = same response. Don't call LLM twice.

```python
import hashlib
import json
from pathlib import Path
from datetime import datetime

class LLMCache:
    def __init__(self):
        self._cache_dir = Path("data/llm_cache")
        self._cache_dir.mkdir(exist_ok=True)
    
    def _key(self, prompt: str, model: str, temperature: float) -> str:
        content = f"{model}:{temperature}:{prompt}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]
    
    def get(self, prompt: str, model: str, temperature: float) -> str | None:
        if temperature > 0:
            return None  # Non-deterministic — never cache
        key = self._key(prompt, model, temperature)
        path = self._cache_dir / f"{key}.json"
        if path.exists():
            return json.loads(path.read_text())["response"]
        return None
    
    def set(self, prompt: str, model: str, temperature: float, response: str) -> None:
        if temperature > 0:
            return
        key = self._key(prompt, model, temperature)
        path = self._cache_dir / f"{key}.json"
        path.write_text(json.dumps({
            "response": response,
            "model": model,
            "created": datetime.now().isoformat()
        }))

_cache = LLMCache()

def cached_complete(prompt: str, model: str, temperature: float, llm_client) -> str:
    cached = _cache.get(prompt, model, temperature)
    if cached:
        return cached
    response = llm_client.complete(prompt, model=model, temperature=temperature)
    _cache.set(prompt, model, temperature, response)
    return response
```

Wire into `agent/llm/client.py`: Check cache before API call, set after successful call.

---

### TASK 0.NEW-F: Batch Embedding Computation [NEW from R1]
**File:** `agent/services/embedder.py`
**Time:** 15 minutes

Add `embed_batch()` that computes all embeddings in one call, returns numpy matrix:

```python
import numpy as np

def embed_batch(texts: list[str]) -> np.ndarray:
    """Embed all texts at once. Returns shape (n_texts, embedding_dim)."""
    return model.encode(texts, convert_to_numpy=True, show_progress_bar=False)

def cosine_similarity_matrix(embeddings: np.ndarray) -> np.ndarray:
    """Compute full cosine similarity matrix in one operation."""
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    normalized = embeddings / (norms + 1e-10)
    return np.dot(normalized, normalized.T)
```

Wire into `collector.py` semantic dedup: Replace per-pair embedding with batch.

---

### TASK 0.NEW-G: Parallel URL Scraping [NEW from R1]
**File:** `agent/modules/collector.py`
**Time:** 20 minutes

```python
import asyncio

async def collect_from_urls_parallel(urls: list[str]) -> list[str]:
    """Scrape all URLs concurrently. 5x faster than sequential."""
    tasks = [asyncio.to_thread(scrape_page, url) for url in urls]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    successful = []
    for url, result in zip(urls, results):
        if isinstance(result, Exception):
            session_logger.log_scrape_failure(url, str(result))
        elif result and len(result.strip()) > 100:
            successful.append(result)
        else:
            session_logger.log_scrape_failure(url, "empty response")
    
    return successful
```

Replace sequential scraping loop in `collect()` with `await collect_from_urls_parallel(urls)`.

---

### TASK 0.NEW-H: Gate Short-Circuit Evaluation [NEW from R1]
**File:** `agent/knowledge/eku_store.py`
**Time:** 15 minutes

Stop running gates after first failure. Gate 6 (mastery contract) is an LLM call — don't waste it.

```python
async def _validate_all_gates(self, eku: ExecutableKnowledgeUnit) -> bool:
    # ORDERED: cheapest first, most expensive last
    gates = [
        self._gate_not_trivial,           # Simple check, fast
        self._gate_entropy,               # Embedding comparison, fast
        self._gate_tests_pass,            # Already computed, fast
        self._gate_not_overfitted,        # Array check, fast
        self._gate_no_contradictions,     # Store lookup, medium
        self._gate_mastery_contract,      # LLM call — MOST EXPENSIVE, run last
    ]
    
    for gate in gates:
        if not await gate(eku):
            return False  # SHORT CIRCUIT — don't run remaining gates
    
    return True
```

---

## PHASE 0D — SAFETY SYSTEMS (NEW from R2, 1.5 hours)

These four tasks are from review_report_2. They are not in the Bible or R1. They prevent silent failures that would corrupt all future knowledge.

### TASK 0.NEW-I: Context Fingerprinting System [NEW from R2]
**New file:** `agent/knowledge/context_fingerprint.py`
**Time:** 35 minutes

**Why this exists:** Without this, the agent learns `list.append` from Python 3 docs but then uses it on Python 2.7 code. Or learns from a codebase before it was modified, then uses knowledge that no longer applies.

```python
import hashlib
import sys
from pathlib import Path
from datetime import datetime

def compute_fingerprint(relevant_files: list[str] = None) -> dict:
    """Compute a fingerprint of current execution context."""
    fingerprint = {
        "runtime_version": sys.version,
        "computed_at": datetime.now().isoformat(),
        "file_hashes": {},
        "dependency_versions": {}
    }
    
    # Hash relevant files if provided
    if relevant_files:
        for filepath in relevant_files:
            path = Path(filepath)
            if path.exists():
                content = path.read_bytes()
                fingerprint["file_hashes"][filepath] = hashlib.sha256(content).hexdigest()[:12]
    
    # Capture key package versions
    try:
        import pkg_resources
        for pkg in ["scrapling", "chromadb", "sentence-transformers", "tiktoken"]:
            try:
                fingerprint["dependency_versions"][pkg] = pkg_resources.get_distribution(pkg).version
            except Exception:
                pass
    except Exception:
        pass
    
    return fingerprint

def fingerprints_match(stored: dict, current: dict) -> tuple[bool, list[str]]:
    """Compare fingerprints. Returns (matches, list_of_differences)."""
    differences = []
    
    if stored.get("runtime_version") != current.get("runtime_version"):
        differences.append(f"Runtime changed: {stored.get('runtime_version')} → {current.get('runtime_version')}")
    
    for filepath, stored_hash in stored.get("file_hashes", {}).items():
        current_hash = current.get("file_hashes", {}).get(filepath)
        if current_hash and current_hash != stored_hash:
            differences.append(f"File modified: {filepath}")
    
    return len(differences) == 0, differences
```

Wire into EKU store: Save fingerprint when EKU is stored.
Wire into task executor: Before using an EKU, check fingerprint. Warn if mismatch.

---

### TASK 0.NEW-J: Version-Aware Knowledge Scoping [NEW from R2]
**File:** `agent/knowledge/eku_schema.py` (additions)
**Time:** 25 minutes

The `version_bounds` field was added in TASK 0.0. Now add the check logic:

```python
def is_compatible_with_version(eku: ExecutableKnowledgeUnit, runtime_version: str) -> tuple[bool, str]:
    """Check if EKU knowledge applies to the current runtime version."""
    bounds = eku.version_bounds
    if not bounds:
        return True, ""  # No bounds specified — assume compatible
    
    from packaging.version import Version
    try:
        current = Version(runtime_version.lstrip("v").split(" ")[0][:5])  # "3.11.2" → Version("3.11.2")
        
        if bounds.get("min_version"):
            if current < Version(bounds["min_version"]):
                return False, f"Requires >= {bounds['min_version']}, you have {runtime_version}"
        
        if bounds.get("max_version"):
            if current > Version(bounds["max_version"]):
                return False, f"Only valid up to {bounds['max_version']}, you have {runtime_version}"
        
        if bounds.get("deprecated_in"):
            dep_version = Version(bounds["deprecated_in"])
            if current >= dep_version:
                return True, f"WARNING: Deprecated in {bounds['deprecated_in']} — verify still works"
        
        if bounds.get("removed_in"):
            rem_version = Version(bounds["removed_in"])
            if current >= rem_version:
                return False, f"Removed in {bounds['removed_in']}, you have {runtime_version}"
    
    except Exception:
        return True, ""  # If version parsing fails, don't block
    
    return True, ""
```

During collection in `collector.py`: Parse version info from documentation if present.
During task solving: Check compatibility before injecting EKU into prompt.

---

### TASK 0.NEW-K: Composition Hazard Registry [NEW from R2]
**New file:** `agent/knowledge/hazard_registry.py`
**Time:** 30 minutes

When two or more EKUs are used together, their interaction may violate invariants neither captures alone.

```python
from dataclasses import dataclass

@dataclass
class CompositionHazard:
    concepts: list[str]      # Concepts that trigger this hazard when combined
    hazard: str              # What goes wrong
    mitigation: str          # How to avoid it
    severity: str            # "error" | "warning" | "note"

PYTHON_HAZARDS = [
    CompositionHazard(
        concepts=["dict iteration", "dict modification"],
        hazard="RuntimeError: dictionary changed size during iteration",
        mitigation="Use dict.copy() or list(dict.keys()) before iteration",
        severity="error"
    ),
    CompositionHazard(
        concepts=["list iteration", "list modification"],
        hazard="Skipped elements or IndexError during iteration",
        mitigation="Iterate over a copy: for item in list.copy()",
        severity="error"
    ),
    CompositionHazard(
        concepts=["file open", "exception handling"],
        hazard="Resource leak if exception raised before file.close()",
        mitigation="Always use context manager: with open(...) as f:",
        severity="warning"
    ),
    CompositionHazard(
        concepts=["mutable default argument", "function definition"],
        hazard="Mutable default shared across all calls",
        mitigation="Use None as default, create mutable inside function",
        severity="error"
    ),
    CompositionHazard(
        concepts=["float arithmetic", "equality comparison"],
        hazard="Float precision errors make == unreliable",
        mitigation="Use math.isclose() or round() for float comparison",
        severity="warning"
    ),
]

JAVASCRIPT_HAZARDS = [
    CompositionHazard(
        concepts=["array iteration", "async operation"],
        hazard="forEach doesn't await async callbacks",
        mitigation="Use for...of loop or Promise.all with .map()",
        severity="error"
    ),
    CompositionHazard(
        concepts=["object comparison", "equality check"],
        hazard="=== doesn't deep compare objects, always returns false for distinct references",
        mitigation="Use JSON.stringify() or deep equality library",
        severity="warning"
    ),
]

ALL_HAZARDS = PYTHON_HAZARDS + JAVASCRIPT_HAZARDS

def check_composition_hazards(required_concepts: list[str]) -> list[CompositionHazard]:
    """Find all hazards triggered by this combination of concepts."""
    found = []
    concepts_lower = [c.lower() for c in required_concepts]
    for hazard in ALL_HAZARDS:
        if all(any(h_concept in c for c in concepts_lower) for h_concept in hazard.concepts):
            found.append(hazard)
    return found
```

Wire into task executor (Phase 3): Before generating any solution, call `check_composition_hazards()`.
If hazards found: inject mitigations as hard constraints into solution generation prompt.

---

### TASK 0.NEW-L: Transitive Confidence Calculator [NEW from R2]
**File:** `agent/knowledge/eku_store.py` (additions)
**Time:** 20 minutes

When EKU B depends on EKU A, using B at its stated confidence is wrong. True confidence decays through the chain.

```python
def calculate_effective_confidence(eku_id: str) -> tuple[float, str]:
    """
    Calculate the real effective confidence considering dependency chain.
    Returns (effective_confidence, chain_description).
    
    Example: A(0.95) → B(0.90) → C(0.85)
    Using C: effective = 0.95 × 0.90 × 0.85 = 0.73 (NOT 0.85)
    """
    eku = self.load_eku(eku_id)
    if not eku:
        return 0.0, f"EKU {eku_id} not found"
    
    if not getattr(eku, 'dependencies', []):
        return eku.confidence, f"{eku.concept}({eku.confidence:.2f})"
    
    chain_parts = [f"{eku.concept}({eku.confidence:.2f})"]
    effective = eku.confidence
    
    for dep_id in eku.dependencies:
        dep_eku = self.load_eku(dep_id)
        if dep_eku:
            effective *= dep_eku.confidence
            chain_parts.append(f"{dep_eku.concept}({dep_eku.confidence:.2f})")
    
    chain_desc = " × ".join(chain_parts) + f" = {effective:.2f}"
    return effective, chain_desc
```

Wire into `agent inspect` command: Show both `raw_confidence` and `effective_confidence`.
Wire into task executor: Use `effective_confidence` for decision-making, not `raw_confidence`.

---

## PHASE 0E — CONFIGURATION & STUBS (45 minutes)

### TASK 0.7: Fix .env Values [B]
**File:** `.env`
**Time:** 5 minutes

```
MAX_LEARNING_ITERATIONS=3      # Was 1 — loop now actually iterates
ENTROPY_THRESHOLD=0.85         # Was 0.92 — stops killing legitimate knowledge
DEFAULT_MODEL=phi3:medium      # Keep this
CI=false                       # Set to true in CI environments
```

---

### TASK 0.8: Per-Type Dedup Thresholds [B]
**File:** `agent/config.py`
**Time:** 20 minutes

Different knowledge types need different similarity thresholds:

```python
DEDUP_THRESHOLDS = {
    "invariant":    0.95,  # Invariants are precise — only true duplicates removed
    "definition":   0.90,  # Definitions can tolerate some overlap
    "edge_case":    0.85,  # Edge cases — medium tolerance
    "example":      0.80,  # Examples — more tolerance, varied examples valuable
    "constraint":   0.92,  # Constraints are precise
    "_default":     0.90,  # Fallback
}

def get_dedup_threshold(knowledge_type: str) -> float:
    return DEDUP_THRESHOLDS.get(knowledge_type, DEDUP_THRESHOLDS["_default"])
```

Wire into `collector.py` `_semantic_dedup()`: Pass knowledge type to get correct threshold.

---

### TASK 0.9: VectorStore Stub [B]
**New file:** `agent/knowledge/vector_store.py`
**Time:** 15 minutes

Creates the interface now. ChromaDB wired in Phase 6.

```python
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from agent.knowledge.eku_schema import ExecutableKnowledgeUnit

class VectorStore:
    """Stub. Phase 6 replaces with real ChromaDB implementation."""
    
    async def search(self, query: str, top_k: int = 5) -> list:
        """Returns [] not None — prevents TypeError on iteration."""
        if feature_enabled("chromadb_enabled"):
            return await self._chromadb_search(query, top_k)
        return []
    
    async def add(self, eku) -> None:
        if feature_enabled("chromadb_enabled"):
            await self._chromadb_add(eku)
    
    async def _chromadb_search(self, query: str, top_k: int) -> list:
        raise NotImplementedError("Phase 6")
    
    async def _chromadb_add(self, eku) -> None:
        raise NotImplementedError("Phase 6")
```

**Critical:** Stub must return `[]` not `None`. Every caller iterates the result.

---

### TASK 0.NEW-M: Smart Chunking by Content Type [NEW from R1]
**File:** `agent/services/chunker.py`
**Time:** 20 minutes

API docs need small chunks preserving function boundaries. Tutorials need large chunks preserving narrative.

```python
def smart_chunk(content: str, source_url: str) -> list[str]:
    url_lower = source_url.lower()
    
    if any(x in url_lower for x in ["api", "reference", "library"]):
        # API docs: small chunks, preserve function boundaries
        return chunk_by_function_boundary(content, max_tokens=200)
    elif any(x in url_lower for x in ["tutorial", "guide", "howto"]):
        # Tutorials: larger chunks, preserve narrative
        return chunk_by_section(content, max_tokens=600)
    else:
        # Default: overlapping chunks
        return chunk_overlapping(content, max_tokens=400, overlap=100)

def chunk_by_function_boundary(content: str, max_tokens: int) -> list[str]:
    # Split at def/class boundaries
    import re
    sections = re.split(r'\n(?=def |class )', content)
    return [s for s in sections if s.strip() and len(s.split()) <= max_tokens]

def chunk_by_section(content: str, max_tokens: int) -> list[str]:
    # Split at heading boundaries
    sections = re.split(r'\n(?=#{1,3} )', content)
    # Merge small sections, split large ones
    result = []
    for section in sections:
        words = section.split()
        if len(words) <= max_tokens:
            result.append(section)
        else:
            result.extend(chunk_overlapping(section, max_tokens, overlap=50))
    return result
```

---

## PHASE 0F — ROBUSTNESS (30 minutes)

### TASK 0.10: Fix Scraper Failure Tracking [B]
**File:** `agent/modules/collector.py`
**Time:** 15 minutes

Current behavior: failed scrapes return empty string silently. Pipeline continues with zero knowledge.

```python
failures = 0
successes = 0

for url in dedupe_urls_by_domain(urls):  # NEW: deduplicate by domain first
    content = scrape_page(url)
    if not content or len(content.strip()) < 100:
        failures += 1
        session_logger.log_scrape_failure(url, "empty or too short")
        
        # Abort if majority failing and nothing collected yet
        failure_rate = failures / max(failures + successes, 1)
        if failure_rate > 0.5 and successes == 0:
            raise ScrapingThresholdError(
                f"Critical scraping failure: {failures}/{failures+successes} URLs failed. "
                f"Check network connection or try different search terms."
            )
        continue
    
    successes += 1
    # ... process content
```

---

### TASK 0.NEW-N: Atomic Learning Sessions [NEW from R1]
**New file:** `agent/utils/atomic_session.py`
**Time:** 25 minutes

Crash mid-learning leaves no corrupted state:

```python
import shutil
import uuid
from pathlib import Path

class AtomicLearningSession:
    """All-or-nothing. If commit() not called, cleanup removes all temp files."""
    
    def __init__(self, concept: str):
        self._temp_dir = Path(f"data/tmp/{uuid.uuid4().hex[:8]}")
        self._temp_dir.mkdir(parents=True, exist_ok=True)
        self._concept = concept
        self._committed = False
    
    def save_intermediate(self, filename: str, data: dict) -> None:
        """Save to temp location only."""
        import json
        (self._temp_dir / filename).write_text(json.dumps(data, indent=2))
    
    def commit(self, final_dest: Path) -> None:
        """Atomic move from temp to permanent. Raises if fails."""
        temp_path = self._temp_dir / "eku.json"
        if not temp_path.exists():
            raise RuntimeError("Nothing to commit — save_intermediate not called")
        temp_path.rename(final_dest)
        self._committed = True
    
    def __del__(self):
        """Cleanup temp files on crash or abort."""
        if not self._committed and self._temp_dir.exists():
            shutil.rmtree(self._temp_dir, ignore_errors=True)
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            # Exception occurred — cleanup temp files
            if self._temp_dir.exists():
                shutil.rmtree(self._temp_dir, ignore_errors=True)
        return False  # Don't suppress exception
```

---

### TASK 0.NEW-O: Source URL Deduplication [NEW from R1]
**File:** `agent/modules/collector.py`
**Time:** 10 minutes

DDG often returns multiple URLs from same domain. Max 2 per domain, official docs first:

```python
def dedupe_urls_by_domain(urls: list[str], max_per_domain: int = 2) -> list[str]:
    from collections import defaultdict
    from urllib.parse import urlparse
    from agent.utils.source_authority import get_authority
    
    # Sort by authority first (official docs get priority)
    urls_sorted = sorted(urls, key=lambda u: -get_authority(u))
    
    domain_counts = defaultdict(int)
    result = []
    
    for url in urls_sorted:
        domain = urlparse(url).netloc.replace("www.", "")
        if domain_counts[domain] < max_per_domain:
            result.append(url)
            domain_counts[domain] += 1
    
    return result
```

---

## PHASE 0 EXIT CRITERIA

**ALL of these must pass before Phase 1. No exceptions.**

```bash
# Fix .env first
grep "MAX_LEARNING_ITERATIONS=3" .env    # Must exist
grep "ENTROPY_THRESHOLD=0.85" .env       # Must exist

# Run ALL sprint 0 tests
python -m pytest tests/test_sprint0.py tests/test_sprint0_enhanced.py -v

# Every single one of these must show PASSED:
✓ test_eku_roundtrip_all_new_fields
✓ test_eku_roundtrip_version_bounds
✓ test_eku_roundtrip_context_fingerprint
✓ test_migration_upgrades_old_eku
✓ test_migration_handles_missing_field
✓ test_migration_handles_extra_field
✓ test_file_lock_prevents_concurrent_write
✓ test_file_lock_timeout
✓ test_feature_flag_disables_chromadb
✓ test_sandbox_env_has_exactly_6_keys
✓ test_sandbox_env_no_api_keys
✓ test_rollback_cascades_downstream_not_upstream
✓ test_rollback_dry_run_does_not_delete
✓ test_contradiction_gate_rejects_lower_confidence
✓ test_code_validator_blocks_os_import
✓ test_code_validator_blocks_eval
✓ test_code_validator_allows_safe_code
✓ test_json_extractor_strips_think_tags
✓ test_json_extractor_handles_nested_think_tags
✓ test_json_extractor_strips_markdown_fences
✓ test_json_extractor_strips_preamble
✓ test_session_logger_creates_structured_file
✓ test_llm_cache_hit_skips_api_call
✓ test_llm_cache_miss_on_model_change
✓ test_parallel_scraping_handles_mixed_success
✓ test_gate_short_circuit_on_first_failure
✓ test_context_fingerprint_detects_file_change
✓ test_version_bounds_reject_incompatible_runtime
✓ test_composition_hazard_detected
✓ test_transitive_confidence_calculated
✓ test_vector_store_stub_returns_empty_not_none
✓ test_scraper_abort_on_high_failure_rate
✓ test_atomic_session_cleanup_on_crash
✓ test_atomic_session_cleanup_on_sigkill
✓ test_per_type_dedup_thresholds_exist_in_config
✓ test_env_max_iterations_is_3
✓ test_env_entropy_threshold_is_0_85

# Health check must be all green
python -m agent health
# All checks: ✅
```

---

---

# PHASE 1: FIRST WORKING LEARNING LOOP
**Duration:** 8-9 hours
**Depends on:** Phase 0 ALL exit criteria green
**Goal:** `python -m agent learn python list.append` completes successfully with a stored, verified EKU.

**IMPORTANT:** Do phases 1A → 1B → 1C → 1D → 1E → 1F → 1G in order.

---

## PHASE 1A — CORE EPISTEMIC FIXES (2 hours)

### TASK 1.1: Fix Circular Verification [B] [CRITICAL — THE MOST IMPORTANT FIX IN THE ENTIRE PROJECT]
**Files:** `agent/modules/executor.py` + `agent/llm/prompts.py`
**Time:** 45 minutes

**Why this is the silent killer:** LLM currently writes BOTH the test code AND the expected answer in the same call. A confidently-wrong LLM generates wrong code that produces wrong output, then generates an expected value matching that wrong output. Both pass. Wrong knowledge gets stored at high confidence.

**The fix — Two separate calls, real sandbox output as ground truth:**

```
OLD FLOW (CIRCULAR — WRONG):
LLM: "Generate test for list.append"
→ Returns: code="x.append(1)" AND expected="[1]"
→ Compare LLM prediction to LLM prediction → always passes

NEW FLOW (CORRECT):
Call 1 (CODE ONLY): "Write Python code demonstrating list.append. NO assertions. NO expected output."
→ Returns only: code="x = []; x.append(1); x.append(2); print(x)"

SANDBOX EXECUTION: Runs code, gets REAL output: "[1, 2]"

Call 2 (ASSERTIONS FROM REAL OUTPUT): 
"Code: {code}
 ACTUAL output from running it: [1, 2]
 Write Python assert statements that verify this behavior.
 ONLY use values you see in the actual output above."
→ Returns: "assert x == [1, 2]\nassert len(x) == 2"
```

Add to `prompts.py`:
```python
CODE_GENERATOR_PROMPT = """
You are generating Python code to demonstrate a specific concept.
Concept: {concept}
Domain: {domain}

Write ONLY executable Python code. 
DO NOT include:
- assert statements
- expected output comments  
- print statements about what should happen
- any predictions about output

Just write the code that demonstrates the concept.
"""

ASSERTION_GENERATOR_PROMPT = """
You are writing test assertions for code that has already been executed.

Code that was run:
{code}

ACTUAL output from running this code (this is ground truth):
{actual_output}

Write Python assert statements that verify this exact behavior.
Only assert things you can see in the actual output above.
Do not assert things you believe should be true — only what IS true per the output.
"""
```

---

### TASK 1.NEW-A: Assertion Independence Verification [NEW from R1]
**File:** `agent/modules/executor.py`
**Time:** 25 minutes

Even with two-call fix, assertion generator can still contradict real output. Verify assertions match:

```python
import re

def verify_assertion_uses_actual_output(
    assertions: str,
    actual_output: str
) -> tuple[bool, str]:
    """
    Verify assertions don't contradict the actual sandbox output.
    Returns (is_valid, error_message).
    """
    # Extract all == comparisons from assertions
    comparisons = re.findall(r'assert\s+\w+\s*==\s*([^\n]+)', assertions)
    
    for comparison in comparisons:
        comparison_clean = comparison.strip()
        # Check if comparison value appears in actual output (loose check)
        # This catches obvious contradictions like asserting [3,4] when output was [1,2]
        if len(comparison_clean) > 3:  # Skip trivial comparisons
            if not any(part in actual_output for part in comparison_clean.replace("'", "").replace('"', "").split()):
                return False, f"Assertion claims {comparison_clean} but actual output was: {actual_output}"
    
    return True, ""
```

Call this after assertion generation. If invalid: log warning, regenerate assertions.

---

### TASK 1.2: Create Source Authority Module [B]
**New file:** `agent/utils/source_authority.py`
**Time:** 20 minutes

```python
AUTHORITY_SCORES = {
    # Official documentation — maximum authority
    "docs.python.org": 1.0,
    "developer.mozilla.org": 1.0,
    "docs.oracle.com": 1.0,
    "docs.microsoft.com": 0.95,
    "nodejs.org": 1.0,
    "reactjs.org": 1.0,
    "react.dev": 1.0,
    "docs.djangoproject.com": 1.0,
    "docs.rust-lang.org": 1.0,
    "golang.org": 1.0,
    "pkg.go.dev": 0.95,
    "kotlinlang.org": 1.0,
    "swift.org": 1.0,
    "developer.apple.com": 1.0,
    "en.cppreference.com": 1.0,
    "isocpp.org": 0.95,
    "docs.rs": 0.90,
    
    # High-quality community
    "github.com": 0.75,
    "stackoverflow.com": 0.65,
    "realpython.com": 0.75,
    "mozilla.org": 0.90,
    
    # Medium quality
    "medium.com": 0.45,
    "dev.to": 0.40,
    "hashnode.com": 0.40,
    "towardsdatascience.com": 0.50,
    
    # Default for unknown
    "_default": 0.50,
}

def get_authority(url: str) -> float:
    from urllib.parse import urlparse
    domain = urlparse(url).netloc.replace("www.", "")
    return AUTHORITY_SCORES.get(domain, AUTHORITY_SCORES["_default"])
```

Wire into `collector.py`: Each scraped URL tagged with its authority score.
Wire into EKU: `eku.source_urls` populated. `eku.avg_source_authority` = mean of all source authorities.

---

## PHASE 1B — EXECUTION QUALITY (1.5 hours)

### TASK 1.3: Near-Failure Detection [B]
**File:** `agent/sandbox/runner.py`
**Time:** 30 minutes

A test that barely passed under 80% time limit is not as healthy as one that passed instantly.

```python
# Add to SandboxResult dataclass:
robustness_score: float = 1.0
fragility_flags: list = field(default_factory=list)

# In _run_python() after execution, calculate:
robustness = 1.0
flags = []

if elapsed_ms > (timeout * 1000 * 0.80):
    robustness -= 0.50
    flags.append("NEAR_TIMEOUT")

if stderr.strip() and proc.returncode == 0:
    robustness -= 0.20
    flags.append("WARNINGS_PRESENT")

if elapsed_ms < 5 and len(code) > 100:
    robustness -= 0.10
    flags.append("SUSPICIOUSLY_FAST")

result.robustness_score = max(0.0, robustness)
result.fragility_flags = flags
```

Wire: When building EKU confidence, weight tests by their robustness_score.
A NEAR_TIMEOUT test contributes 0.5 to confidence, not 1.0.

---

### TASK 1.NEW-B: Sandbox Warm Pool [NEW from R1]
**New file:** `agent/sandbox/pool.py`
**Time:** 30 minutes

Subprocess spawn costs 50-100ms. With 9 tests = 900ms wasted. Fix with warm pool.

```python
import asyncio
from agent.sandbox.runner import SandboxRunner

class SandboxPool:
    def __init__(self, size: int = 3):
        self._size = size
        self._pool: list[SandboxRunner] = []
    
    async def initialize(self):
        """Pre-warm the pool."""
        self._pool = [SandboxRunner() for _ in range(self._size)]
    
    async def execute(self, code: str, timeout: int = 10) -> dict:
        if not self._pool:
            # Pool empty or not initialized — create fresh
            runner = SandboxRunner()
            return runner.run(code, timeout=timeout)
        
        runner = self._pool.pop()
        try:
            result = runner.run(code, timeout=timeout)
            # Replace consumed runner with fresh one
            self._pool.append(SandboxRunner())
            return result
        except Exception as e:
            # Runner crashed — replace with fresh, re-raise
            self._pool.append(SandboxRunner())
            raise
    
    def handle_all_crashed(self):
        """Recovery if all 3 pooled sandboxes crash simultaneously."""
        self._pool = [SandboxRunner() for _ in range(self._size)]

_pool = SandboxPool()
```

Enable via feature flag. Wire into executor.py: `if feature_enabled("sandbox_pool"): use pool else use direct runner`.

---

### TASK 1.NEW-C: Test Category Balancing [NEW from R1]
**File:** `agent/modules/executor.py`
**Time:** 20 minutes

```python
TEST_REQUIREMENTS = {
    "normal":  {"min": 3, "max": 4},   # Happy path tests
    "edge":    {"min": 3, "max": 4},   # Edge cases (None, empty, boundary)
    "extreme": {"min": 2, "max": 3}    # Adversarial (wrong types, huge input)
}

CATEGORY_TEMPERATURES = {
    "normal":  0.0,   # Deterministic — happy path always same
    "edge":    0.3,   # Some variation — discover different edges each run
    "extreme": 0.5,   # High variation — adversarial needs creativity
}

def generate_balanced_tests(concept: str, already_tested: list[str] = None) -> list[TestCase]:
    tests = []
    for category, reqs in TEST_REQUIREMENTS.items():
        category_tests = generate_tests_for_category(
            concept=concept,
            category=category,
            count=reqs["max"],
            temperature=CATEGORY_TEMPERATURES[category],
            avoid_similar_to=already_tested or []
        )
        tests.extend(category_tests[:reqs["max"]])
        
        if len(category_tests) < reqs["min"]:
            # Log warning but don't crash — some concepts have few edge cases
            session_logger.log("execution", "insufficient_test_coverage",
                               {"category": category, "generated": len(category_tests), "needed": reqs["min"]})
    
    return tests
```

---

## PHASE 1C — GATE SYSTEM (1.5 hours)

### TASK 1.4: Mastery Contract Gate [B]
**Files:** `agent/knowledge/eku_store.py` + `agent/modules/pre_validator.py`
**Time:** 30 minutes

The pre_validator generates a `LearningContract` with mastery criteria. This gate checks if they're met.

```python
def _gate_mastery_contract_met(
    self, eku: ExecutableKnowledgeUnit, contract: LearningContract
) -> bool:
    unmet = []
    for criterion in contract.mastery_criteria:
        if not self._check_criterion(eku, criterion):
            unmet.append(criterion)
    
    eku.mastery_criteria_met = [c for c in contract.mastery_criteria if c not in unmet]
    eku.mastery_criteria_unmet = unmet
    
    if unmet:
        eku.gate_diagnostics.append(GateDiagnostic(
            gate_name="mastery_contract",
            failure_reason=f"Unmet criteria: {unmet}",
            actual_value=len(eku.mastery_criteria_met),
            required_value=len(contract.mastery_criteria),
            suggested_fix="Increase MAX_LEARNING_ITERATIONS=5 or add more authoritative sources",
            is_retryable=True
        ))
        return False
    
    return True
```

---

### TASK 1.5: Rich Gate Diagnostics [B]
**File:** `agent/knowledge/eku_store.py`
**Time:** 25 minutes

Replace bare string gate names with rich diagnostic objects. Every gate failure must explain:
- What failed
- What the actual value was
- What the required value is
- How to fix it
- Whether it can be retried

Example output from `agent inspect list.append` when quarantined:
```json
{
    "gate_diagnostics": [
        {
            "gate_name": "tests_pass",
            "failure_reason": "Only 3/9 tests passed (33%). Required: >= 70%",
            "actual_value": 0.33,
            "required_value": 0.70,
            "suggested_fix": "Increase MAX_LEARNING_ITERATIONS=5",
            "is_retryable": true
        }
    ]
}
```

---

### TASK 1.NEW-D: Graduated Gate Thresholds [NEW from R1]
**File:** `agent/knowledge/eku_store.py`
**Time:** 15 minutes

First learning attempt gets slightly more lenient gates. Re-learning is stricter (replacing existing knowledge requires proving it's better):

```python
def get_gate_threshold(gate_name: str, iteration: int, is_relearn: bool) -> float:
    base_thresholds = {
        "tests_pass":    0.70,
        "entropy":       0.85,
        "not_trivial":   0.30,
        "not_overfitted": 2,    # Minimum distinct test categories
    }
    
    base = base_thresholds[gate_name]
    
    if isinstance(base, float):
        if is_relearn:
            return min(base + 0.10, 0.99)   # Stricter for re-learning
        elif iteration == 1:
            return max(base - 0.10, 0.0)    # Lenient for first attempt
        else:
            return base
    return base  # int thresholds don't scale
```

---

### TASK 1.NEW-E: Quarantine with Re-Learning Hints [NEW from R1]
**File:** `agent/knowledge/eku_store.py`
**Time:** 20 minutes

When quarantined, tell the user exactly how to fix it:

```python
GATE_FIX_HINTS = {
    "tests_pass": [
        "Try: MAX_LEARNING_ITERATIONS=5 python -m agent learn {concept}",
        "Try: python -m agent learn {concept} --sources official",
        "Check prerequisites: python -m agent deps {concept}"
    ],
    "not_overfitted": [
        "Knowledge too narrow — learn broader topic first",
        "Try: python -m agent suggest-prereqs {concept}"
    ],
    "entropy": [
        "Too similar to existing knowledge: python -m agent similar {concept}",
        "Consider if this is genuinely new or just an alias"
    ],
    "mastery_contract": [
        "Re-learn with more iterations: MAX_LEARNING_ITERATIONS=5",
        "Add specific documentation URL: python -m agent learn {concept} --url {url}"
    ]
}
```

---

## PHASE 1D — KNOWLEDGE QUALITY (1.5 hours)

### TASK 1.6: Quality-Weighted Dedup Winner [B]
**File:** `agent/modules/collector.py`
**Time:** 25 minutes

Current dedup winner is the longest string. Wrong. Winner should be most precise.

```python
def _quality_score(text: str) -> float:
    """Higher score = more precise, more useful knowledge."""
    words = text.split()
    if not words:
        return 0.0
    
    # Count precision markers — specific values, types, behaviors
    precision_count = len(re.findall(
        r'O\(|returns |raises |None|True|False|\d+|TypeError|ValueError|IndexError', 
        text
    ))
    density = precision_count / len(words)
    
    # Penalize verbosity — precision density per character matters
    verbosity_penalty = min(1.0, 80 / len(text)) if len(text) > 80 else 1.0
    
    return density * verbosity_penalty

# In dedup: winner = max(item_i, item_j, key=_quality_score)
# "append modifies list in-place, returns None" beats verbose blog explanation
```

---

### TASK 1.7: Lossless Compressor [B]
**File:** `agent/modules/compressor.py`
**Time:** 30 minutes

Current: LLM summarizes everything → structured data destroyed.
New: Two-pass. Structured data merged directly (no LLM). LLM only synthesizes prose.

```python
def compress_phases(phases: list) -> ExecutableKnowledgeUnit:
    
    # PASS 1: Direct merge — no LLM, zero data loss
    structured = {
        "test_results":         [],
        "failure_memory":       [],
        "edge_cases":           [],
        "execution_templates":  [],
        "source_urls":          [],
        "hard_constraints":     [],
        "canonical_traces":     [],
    }
    for phase in phases:
        structured["test_results"].extend(getattr(phase, "test_results", []))
        structured["failure_memory"].extend(getattr(phase, "failure_memory", []))
        structured["edge_cases"].extend(getattr(phase, "edge_cases", []))
        structured["execution_templates"].extend(getattr(phase, "execution_templates", []))
        structured["source_urls"].extend(getattr(phase, "source_urls", []))
        structured["hard_constraints"].extend(getattr(phase, "hard_constraints", []))
    
    # PASS 2: LLM synthesizes ONLY prose fields
    prose = llm_synthesize_prose(
        definitions=[p.definition for p in phases if p.definition],
        invariants=[inv for p in phases for inv in getattr(p, "invariants", [])]
    )
    
    # Combine: structured data (lossless) + synthesized prose
    eku = ExecutableKnowledgeUnit()
    eku.definition = prose["definition"]
    eku.invariants = prose["invariants"]
    eku.test_results = structured["test_results"]
    eku.failure_memory = structured["failure_memory"]
    eku.edge_cases = structured["edge_cases"]
    eku.source_urls = list(set(structured["source_urls"]))
    eku.hard_constraints = list(set(structured["hard_constraints"]))
    
    return eku
```

---

### TASK 1.NEW-F: Confidence Ceiling by Evidence Count [NEW from R1]
**File:** `agent/modules/compressor.py`
**Time:** 15 minutes

Single-source knowledge cannot be highly confident. Evidence breadth caps confidence:

```python
EVIDENCE_CEILING = {
    1: 0.60,  # Single source → max 60%
    2: 0.75,  # Two sources → max 75%
    3: 0.85,  # Three sources → max 85%
}

def calculate_confidence(
    test_pass_rate: float,
    source_authority: float,
    source_count: int,
    robustness_score: float
) -> float:
    raw = (
        test_pass_rate * 0.40 +
        source_authority * 0.25 +
        robustness_score * 0.35
    )
    ceiling = EVIDENCE_CEILING.get(source_count, 0.95)
    return min(raw, ceiling)
```

---

## PHASE 1E — TEST GENERATION (1 hour)

### TASK 1.8: Temperature Stratification [B]
**File:** `agent/modules/executor.py`
**Time:** 20 minutes

Already implemented in TASK 1.NEW-C (CATEGORY_TEMPERATURES dict). Additionally:

After first run, inject "do NOT generate tests similar to: {already_tested}" into subsequent generation prompts. This forces exploration of untested territory in iterations 2 and 3.

```python
def build_test_gen_prompt(concept: str, category: str, already_tested: list[str]) -> str:
    avoid_section = ""
    if already_tested:
        avoid_section = f"\nDo NOT generate tests similar to:\n" + "\n".join(f"- {t}" for t in already_tested)
    
    return f"""Generate {category} tests for {concept}.{avoid_section}"""
```

---

### TASK 1.9: Constraint Extractor [B]
**New file:** `agent/modules/constraint_extractor.py`
**Time:** 40 minutes

Three sources of hard constraints:

```python
import re

class ConstraintExtractor:
    
    def extract_from_failure(self, failure: TestResult) -> list[str]:
        """Failure inversion: every failure implies a constraint."""
        constraints = []
        
        if "TypeError" in failure.error_message:
            # "TypeError when URL is None" → "URL must never be None"
            prompt = f"This failure: '{failure.error_message}' implies what constraint? Reply with one 'X must Y' rule."
            constraint = llm_complete(prompt).strip()
            if constraint:
                constraints.append(constraint)
        
        if "IndexError" in failure.error_message:
            constraints.append("Must check list is non-empty before indexing")
        
        return constraints
    
    def extract_from_passing_test(self, code: str, actual_output: str) -> list[str]:
        """Passing test confirms expected behavior."""
        prompt = f"""
        Code: {code}
        Output: {actual_output}
        
        What behavior rule does this passing test confirm?
        Reply with one constraint in the form 'X always Y' or 'X returns Y'.
        """
        constraint = llm_complete(prompt).strip()
        return [constraint] if constraint else []
    
    def extract_from_documentation(self, doc_text: str) -> list[str]:
        """Parse explicit rules from documentation."""
        patterns = [
            r'must\s+\w+[^.]+\.',
            r'always\s+\w+[^.]+\.',
            r'never\s+\w+[^.]+\.',
            r'raises\s+\w+Error[^.]+\.',
            r'returns\s+None[^.]*\.',
        ]
        constraints = []
        for pattern in patterns:
            matches = re.findall(pattern, doc_text, re.IGNORECASE)
            constraints.extend(matches)
        return constraints[:10]  # Max 10 per doc to prevent noise
```

Call this during Phase collection. Wire results into `eku.hard_constraints`.

---

### TASK 1.NEW-G: Smart Retry with Differentiated Prompts [NEW from R1]
**File:** `agent/llm/client.py`
**Time:** 20 minutes

Current retry sends the same prompt. Same prompt at temp=0 = same failure. Fix:

```python
def generate_with_smart_retry(prompt: str, max_retries: int = 3) -> dict | None:
    last_error = None
    
    for attempt in range(max_retries):
        if attempt > 0:
            # DIFFERENTIATE on retry — same prompt guarantees same failure
            prompt = f"""{prompt}

[RETRY ATTEMPT {attempt + 1}]
Your previous response failed validation.
Error from previous attempt: {last_error}

Please try a different approach:
- Be more explicit with JSON formatting
- Ensure all required fields are present
- Double-check your response is valid JSON only
"""
        
        response = llm_complete(prompt)
        result = extract_json(response)
        
        if result:
            error = validate_result(result)
            if not error:
                return result
            last_error = error
        else:
            last_error = "Response was not valid JSON"
    
    return None
```

---

### TASK 1.NEW-H: Failure Pattern Clustering [NEW from R1]
**File:** `agent/modules/failure_analyzer.py`
**Time:** 25 minutes

```python
import re
from collections import defaultdict

FAILURE_PATTERNS = {
    "type_error":        r"TypeError:.*(NoneType|'int'|'str'|'list'|'dict')",
    "attribute_error":   r"AttributeError:.*has no attribute",
    "import_error":      r"ModuleNotFoundError|ImportError",
    "timeout":           r"TimeoutError|timed out",
    "assertion":         r"AssertionError",
    "index_error":       r"IndexError",
    "key_error":         r"KeyError",
    "runtime_error":     r"RuntimeError",
}

def cluster_failures(failures: list) -> dict[str, list]:
    """Group failures by root cause pattern."""
    clusters = defaultdict(list)
    
    for failure in failures:
        matched = False
        for pattern_name, regex in FAILURE_PATTERNS.items():
            if re.search(regex, failure.get("error_message", ""), re.IGNORECASE):
                clusters[pattern_name].append(failure)
                matched = True
                break
        if not matched:
            clusters["unknown"].append(failure)
    
    return dict(clusters)

def get_root_cause_summary(clusters: dict) -> str:
    """Human-readable summary of what's failing and why."""
    if not clusters:
        return "No failures recorded."
    
    dominant = max(clusters.items(), key=lambda x: len(x[1]))
    return f"Primary failure pattern: {dominant[0]} ({len(dominant[1])} occurrences)"
```

---

## PHASE 1F — UX (30 minutes)

### TASK 1.NEW-I: Progress Reporting with Rich [NEW from R1]
**File:** `agent/cli.py` + `agent/orchestrator.py`
**Time:** 30 minutes

```python
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.console import Console

console = Console()

LEARNING_PHASES = [
    "Pre-validation",
    "Web collection",
    "Knowledge extraction", 
    "Verification",
    "Sandbox execution",
    "Failure analysis",
    "Compression",
    "Gate validation",
    "Storage"
]

async def learn_with_progress(concept: str, domain: str):
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}"),
        BarColumn(),
        TextColumn("{task.completed}/{task.total}"),
        console=console
    ) as progress:
        task = progress.add_task(f"Learning {concept}", total=len(LEARNING_PHASES))
        
        for phase_name in LEARNING_PHASES:
            progress.update(task, description=f"[{LEARNING_PHASES.index(phase_name)+1}/{len(LEARNING_PHASES)}] {phase_name}...")
            # Check LLM cache — show cache hit in description
            await execute_phase(phase_name, concept, domain, progress_callback=lambda: progress.advance(task))
```

---

## PHASE 1G — INTEGRATION (30 minutes)

### TASK 1.10: Run The First Complete Learning Loop [B]
**Time:** 20 minutes running + debugging

```bash
python -m agent learn python list.append
```

You will likely hit 2-4 issues on the first complete run. Fix them. Run again. Repeat until clean.

**Expected path through the code:**
1. `cli.py` → `orchestrator.py` → `pre_validator.py`
2. `pre_validator.py` generates `LearningContract` with mastery criteria
3. `orchestrator.py` → `collector.py` → `web_search.py` (DDG) + `web_scraper.py`
4. `collector.py` deduplicates → `verifier.py` runs counter-questions
5. `orchestrator.py` → `executor.py` runs two-call test generation
6. `executor.py` → `code_validator.py` (safety check) → `sandbox/runner.py`
7. `failure_analyzer.py` processes any failures → `constraint_extractor.py`
8. `compressor.py` merges phases losslessly
9. `eku_store.py` runs all 6 gates → stores or quarantines

---

### TASK 1.11: Transfer Validation Gate [NEW from R2]
**Time:** 40 minutes

When a cross-language invariant link is created (Phase 4), validate it before trusting it:

```python
@dataclass  
class InvariantLink:
    source_eku_id: str
    target_eku_id: str
    shared_invariant: str
    similarity_score: float
    transfer_status: str = "uncertain"    # "confirmed" | "uncertain" | "rejected"
    validation_tests: list = field(default_factory=list)
    created_at: str = ""

async def validate_transfer_link(link: InvariantLink, target_eku) -> InvariantLink:
    """Generate 3 language-specific tests to verify the transfer is real."""
    adversarial_tests = await generate_language_specific_tests(
        concept=target_eku.concept,
        domain=target_eku.domain,
        shared_invariant=link.shared_invariant,
        count=3
    )
    
    results = []
    for test in adversarial_tests:
        result = sandbox.run(test.code)
        results.append(result)
    
    link.validation_tests = results
    failures = [r for r in results if not r.passed]
    
    if len(failures) == 0:
        link.transfer_status = "confirmed"
    elif len(failures) <= 1:
        link.transfer_status = "uncertain"
    else:
        link.transfer_status = "rejected"
    
    return link
```

---

### TASK 1.12: Delayed Outcome Verification [NEW from R2]
**Time:** 30 minutes

Don't mark experience as "success" until verified. Prevents reinforcing subtly-wrong patterns:

```python
@dataclass
class ExperienceRecord:
    task: str
    solution_code: str
    concepts_used: list[str]
    outcome_status: str = "provisional"   # "provisional" | "confirmed" | "invalidated"
    confirmation_due: str = ""            # ISO timestamp 7 days out
    invalidation_reason: str | None = None

def mark_provisional(experience: ExperienceRecord) -> ExperienceRecord:
    from datetime import datetime, timedelta
    experience.outcome_status = "provisional"
    experience.confirmation_due = (datetime.now() + timedelta(days=7)).isoformat()
    return experience

# Background job (run daily):
def confirm_or_invalidate_experiences():
    from datetime import datetime
    for exp in load_all_provisional_experiences():
        if datetime.fromisoformat(exp.confirmation_due) < datetime.now():
            # Run adversarial tests against stored solution
            test_results = run_adversarial_tests(exp.solution_code, exp.concepts_used)
            if all(r.passed for r in test_results):
                exp.outcome_status = "confirmed"
            else:
                exp.outcome_status = "invalidated"
                exp.invalidation_reason = f"Failed adversarial tests: {[r.error_message for r in test_results if not r.passed]}"
```

---

### TASK 1.13: Usage-Weighted Context Injection [NEW from R2]
**File:** `agent/modules/task_executor.py` (Phase 3, but design now)
**Time:** 25 minutes — design the interface now, implement in Phase 3

```python
def build_context_for_task(ekus: list, max_tokens: int = 2000) -> str:
    """
    High-usage EKUs get full context. Low-usage get minimal reference.
    Engineering follows power law: 20% of knowledge solves 80% of tasks.
    """
    ekus_sorted = sorted(ekus, key=lambda e: e.usage_count, reverse=True)
    
    context_parts = []
    tokens_used = 0
    
    for i, eku in enumerate(ekus_sorted):
        if i < 2 or eku.usage_count > 10:
            content = format_full_context(eku)      # All constraints, traces, edge cases
        elif eku.usage_count > 3:
            content = format_summary_context(eku)   # Key facts only
        else:
            content = format_minimal_context(eku)   # Name + definition only
        
        estimated_tokens = len(content.split()) * 1.3  # Rough token estimate
        if tokens_used + estimated_tokens > max_tokens:
            break
        
        context_parts.append(content)
        tokens_used += estimated_tokens
    
    return "\n\n---\n\n".join(context_parts)
```

---

## PHASE 1 EXIT CRITERIA

**ALL must pass before Phase 2:**

```bash
# Core test
python -m agent learn python list.append

python -m agent inspect list.append
# Must show ALL of:
# status: "proven"  
# confidence: BETWEEN 0.60 and 0.90 (not too high, not too low)
# hard_constraints: >= 3 entries
# avg_source_authority: > 0.70
# avg_robustness_score: > 0.80
# mastery_criteria_unmet: []
# gate_diagnostics: []  (or gate_diagnostics shows all gates passed)
# source_urls: contains "docs.python.org"
# effective_confidence shown (not just raw_confidence)

# Deduplication test
python -m agent learn python list.append
python -m agent learn python list.append
python -m agent list
# count of list.append EKUs must be exactly 1

# Learn 3 more concepts (all must reach "proven")
python -m agent learn python list.extend
python -m agent learn python list.insert
python -m agent learn python dict.update

python -m agent list
# Shows 4 concepts, all status: "proven"

# Run all tests
python -m pytest tests/test_sprint0.py tests/test_sprint0_enhanced.py tests/test_sprint1.py tests/test_sprint1_enhanced.py -v

# Additional exit criteria from R1:
✓ Second learn of same concept shows "cache hit" in logs
✓ agent inspect shows confidence <= 0.75 if only 2 sources (ceiling applied)
✓ Test execution shows 3 test categories (normal/edge/extreme)
✓ gate_diagnostics show specific values when any gate fails

# Validation checkpoints from R2:
python -m agent ask "What does list.append return?"
# Expected: "None. list.append modifies in-place and returns None. [Source: docs.python.org, confidence: 0.XX]"
# If it cannot cite source or claims confidence without learning: Phase 1 incomplete.
```

---

---

# PHASE 2: KNOWLEDGE INTELLIGENCE LAYER
**Duration:** 5 hours
**Depends on:** Phase 1 ALL exit criteria green
**Goal:** Make concepts aware of each other. Build the intelligence that connects knowledge.

---

### TASK 2.1: Invariant Inheritance Graph [B]
**New file:** `agent/knowledge/invariant_graph.py`
**Time:** 45 minutes

After Phase 1 you have 4 EKUs: list.append, list.extend, list.insert, dict.update.
All share: "modifies object in-place, returns None." But stored as isolated strings.

When `list.append`'s invariant is corrected, `list.extend` should be flagged for re-verification.
When `set.add` is learned later, it should inherit edge cases from all 3 in-place mutation methods.

**Implementation:** See Phase 2 code in PROJECT_BIBLE SECTION 5 TASK 2.1 — implement exactly as documented.

Key methods:
- `add_eku(eku)` — finds links with all existing EKUs
- `propagate_correction(eku_id, corrected_invariant)` — flags linked EKUs for re-verification
- `inherit_edge_cases(new_eku)` — if 3+ links, inherit edge cases from linked EKUs

---

### TASK 2.2: Declarative Knowledge Tier (DKU) [B]
**New files:** `agent/knowledge/dku_schema.py` + `agent/knowledge/dku_store.py`
**Time:** 40 minutes

Performance rules, deprecation notices, architecture patterns cannot be "proven" by sandbox execution. They still need to be stored.

`DeclarativeKnowledgeUnit` gates:
- `cross_reference_count >= 2` — must appear in at least 2 independent sources
- `avg(authority_scores) >= 0.60`
- `formal_check` present — even if not auto-runnable

DKUs feed task executor as additional constraints.

---

### TASK 2.3: Prerequisite Dependency Check [B]
**File:** `agent/modules/pre_validator.py`
**Time:** 35 minutes

Before learning `asyncio`, check if `coroutines` and `event_loop` are in the EKU store.
If critical prerequisites missing: warn user, suggest learning order.

```
⚠️ PREREQUISITE WARNING: Learning 'asyncio' requires:
   ❌ coroutines — not yet learned (REQUIRED)
   ❌ event_loop — not yet learned (REQUIRED)  
   ⚠️ generators — not yet learned (helpful but not required)

Suggested order: python -m agent learn python coroutines
```

---

### TASK 2.4: Gap Detector [B]
**New file:** `agent/modules/gap_detector.py`
**Time:** 35 minutes

When task requires concepts not in EKU store: identify exactly what's missing, never attempt silently.

```python
def detect_gaps(task_description: str, available_ekus: list) -> GapReport:
    # Extract required concepts from task
    required_concepts = extract_required_concepts(task_description)
    
    # Check each against store
    known = [c for c in required_concepts if any(e.concept == c for e in available_ekus)]
    missing = [c for c in required_concepts if c not in known]
    
    return GapReport(
        required=required_concepts,
        known=known,
        missing=missing,
        can_proceed=len(missing) == 0,
        suggestion=f"Learn these first: {missing}" if missing else ""
    )
```

---

### TASK 2.5: Knowledge Graph Connector [B]
**New file:** `agent/modules/connector.py`
**Time:** 30 minutes

Builds explicit edges in the knowledge graph:
- `requires` — concept B requires concept A as prerequisite
- `extends` — concept B is a specialization of concept A
- `contradicts` — concept B contradicts concept A (triggers re-verification)
- `similar_to` — concept B is similar but distinct from concept A

---

### TASK 2.NEW-A: Inference Chain Tracker [NEW from R2]
**Time:** 35 minutes

When EKU B depends on EKU A which depends on EKU C: using B means trusting A and C.
Confidence must multiply through the chain.

```python
@dataclass
class InferenceChain:
    terminal_eku_id: str
    chain: list[str]                  # [A_id, B_id, C_id]
    chain_confidence: float           # A.conf × B.conf × C.conf
    weakest_link: str                 # EKU ID with lowest confidence

def build_inference_chain(eku_id: str) -> InferenceChain:
    # Already implemented in TASK 0.NEW-L (transitive confidence)
    # Now wrap it with the chain structure
    pass

# Before using ANY EKU in task solving:
# Build its inference chain
# If chain_confidence < 0.5: warn "Knowledge relies on uncertain foundation: {weakest_link}"
```

---

### TASK 2.NEW-B: Context Scope Manager [NEW from R2]
**Time:** 30 minutes

EKUs learned from a web app codebase may not apply to a CLI tool.

```python
@dataclass
class ContextScope:
    project_type: str | None     # "web", "cli", "library", "data-pipeline"
    framework: str | None        # "django", "react", "none"
    environment: str | None      # "production", "development", "testing"

# During task solving: detect current project context from codebase
# Filter EKUs by matching context scope
# EKUs with mismatched scope get warning annotation in prompt
```

---

## PHASE 2 EXIT CRITERIA

```bash
# After learning list.append, list.extend, list.insert, dict.update:
python -m agent learn python set.add

# Must show in inspect output:
# inherited_edge_cases: > 0 (inherited from in-place mutation siblings)
# invariant_links: >= 3 (linked to list.append, list.extend, list.insert)

# Prerequisites working:
python -m agent learn python asyncio
# Must show prerequisite warning before attempting

# Gap detection working:
python -m agent solve "write async code using asyncio"
# If asyncio not learned: shows gap report, not silent failure

# Run all tests:
python -m pytest tests/test_sprint2.py -v

# Inference chain checkpoint (from R2):
python -m agent inspect set.add
# Shows both raw_confidence and effective_confidence (with chain breakdown)
```

---

---

# PHASE 3: TASK EXECUTION ENGINE
**Duration:** 7 hours
**Depends on:** Phase 2 complete
**Goal:** Agent solves real tasks using its verified knowledge.

---

### TASK 3.1-3.5: Core Task Executor [B]
**New file:** `agent/modules/task_executor.py`
**Time:** 4 hours total

Implement full task solving loop as documented in PROJECT_BIBLE Section 6.
Key components:
- Task interpretation (extract required concepts)
- Knowledge retrieval (gap detection, context injection)
- Solution generation (constraints injected from EKUs)
- Solution verification (check against hard_constraints before sandbox)
- Result packaging (cite sources, explain constraints respected)

---

### TASK 3.6: Adaptive Planner [NEW from R2] [CRITICAL]
**Time:** 60 minutes

Current architecture: `Plan → Execute → (failure) → retry same plan` = same failure.
Required: `Plan → Execute → (failure) → classify why → revise plan → try different approach`

```python
class AdaptivePlanner:
    revision_budget: int = 3
    
    async def solve(self, task: str) -> TaskResult:
        plan = self.create_plan(task)
        revisions = 0
        
        while revisions < self.revision_budget:
            for step in plan.steps:
                result = await self.execute_step(step)
                
                if result.failed:
                    failure_type = self.classify_failure(result)
                    
                    if failure_type == "knowledge_gap":
                        return TaskResult(refused=True, reason="Missing knowledge", gaps=result.gaps)
                    
                    if failure_type == "impossible":
                        return TaskResult(refused=True, reason=result.why)
                    
                    if failure_type == "wrong_approach":
                        plan = self.revise_plan(plan, failure_type)
                        revisions += 1
                        break  # Restart with revised plan
                    
                    if failure_type == "environment":
                        await asyncio.sleep(2 ** revisions)  # Exponential backoff
                        continue  # Retry same step
            else:
                return TaskResult(success=True, code=plan.final_code)
        
        return TaskResult(refused=True, reason=f"Exhausted {self.revision_budget} plan revisions. Needs human review.")
    
    def classify_failure(self, result: StepResult) -> str:
        """
        Four types of failure — each requires different response:
        - knowledge_gap: agent doesn't know enough → refuse, explain gaps
        - wrong_approach: tried wrong strategy → revise plan
        - environment: network/sandbox issue → retry with backoff
        - impossible: task cannot be done → refuse gracefully
        """
        if result.missing_concepts:
            return "knowledge_gap"
        if result.error_type in ("TimeoutError", "NetworkError"):
            return "environment"
        if "impossible" in result.error_message.lower():
            return "impossible"
        return "wrong_approach"
```

---

### TASK 3.7: Composition Hazard Check in Task Executor [NEW from R2]
**Time:** 30 minutes

Wire the hazard registry (TASK 0.NEW-K) into task execution:

```python
# Before generating any solution:
required_concepts = extract_required_concepts(task_description)
hazards = check_composition_hazards(required_concepts)

if hazards:
    # Inject mitigations as HARD CONSTRAINTS into solution prompt
    mitigation_context = "\n".join([
        f"⚠️ HAZARD: {h.hazard}\nMITIGATION REQUIRED: {h.mitigation}"
        for h in hazards
    ])
    
    solution_prompt += f"\n\nMANDATORY CONSTRAINTS:\n{mitigation_context}"
    
    # After generation: verify solution includes mitigation
    for hazard in hazards:
        if hazard.mitigation_keyword not in generated_code:
            session_logger.log("execution", "hazard_mitigation_missing", 
                             {"hazard": hazard.hazard, "mitigation": hazard.mitigation})
```

---

### TASK 3.8: Fingerprint Verification Before Execution [NEW from R2]
**Time:** 20 minutes

Before executing any task that uses stored EKUs:

```python
current_fp = compute_fingerprint()
for eku in ekus_being_used:
    stored_fp = eku.context_fingerprint
    if stored_fp:
        matches, differences = fingerprints_match(stored_fp, current_fp)
        if not matches:
            console.print(f"⚠️ WARNING: Knowledge for '{eku.concept}' was learned in a different context:")
            for diff in differences:
                console.print(f"   - {diff}")
            console.print("   Solution may not apply to current codebase. Verify before using.")
```

---

### TASK 3.NEW: Speculative Pre-Fetching [NEW from R1]
**Time:** 30 minutes

While learning `list.append`, start pre-fetching web content for `list.extend` (likely next):

```python
async def learn_with_prefetch(concept: str, domain: str):
    learn_task = asyncio.create_task(learn_concept(concept, domain))
    
    # Predict next 2 concepts from patterns + invariant graph
    likely_next = predict_next_concepts(concept, domain)
    
    # Start background prefetch (don't await — fire and forget)
    prefetch_tasks = [
        asyncio.create_task(prefetch_web_content(c, domain))
        for c in likely_next[:2]
    ]
    
    result = await learn_task
    # Prefetched content now cached for next `learn` command
    return result

def predict_next_concepts(concept: str, domain: str) -> list[str]:
    """Based on what people commonly learn together."""
    siblings = {
        "list.append": ["list.extend", "list.insert", "list.pop"],
        "dict.update": ["dict.get", "dict.items", "dict.setdefault"],
    }
    return siblings.get(f"{domain}.{concept}", [])
```

Enable via feature flag `speculative_prefetch`.

---

## PHASE 3 EXIT CRITERIA

```bash
# Solve a real task:
python -m agent solve "Write a function that adds items to a list without duplicates"
# Must: cite which EKUs it used, show constraints it respected, produce working code

# Composition hazard test (from R2 checkpoint):
python -m agent solve "Write a function that appends to a list while iterating over it"
# Must: show composition hazard warning about concurrent modification, NOT just generate code

# Adaptive planner test:
python -m agent solve "Learn quantum computing then write a quantum circuit"
# Must: refuse gracefully citing knowledge gap, NOT attempt with no knowledge

# Run tests:
python -m pytest tests/test_sprint3.py -v

✓ test_adaptive_planner_revises_on_wrong_approach
✓ test_adaptive_planner_refuses_after_budget_exhausted
✓ test_composition_hazard_injected_into_prompt
✓ test_fingerprint_mismatch_warns_user
✓ test_task_cites_source_ekus
✓ test_gap_detection_refuses_gracefully
```

---

---

# PHASE 4: MULTI-LANGUAGE SUPPORT
**Duration:** 4 hours
**Depends on:** Phase 1 (can run parallel with Phases 2-3)
**Goal:** JavaScript support. Cross-language transfer with validated limitations.

---

### TASK 4.1-4.5: Language Adapters [B]
**New files:** `agent/adapters/base.py`, `agent/adapters/python_adapter.py`, `agent/adapters/javascript_adapter.py`
**Time:** 2.5 hours total

Implement as documented in PROJECT_BIBLE Sprint 4.
Enable via feature flag `multi_language`.

---

### TASK 4.6: Language-Specific Hazard Registry [NEW from R2]
**Time:** 30 minutes

Already created JavaScript hazards in TASK 0.NEW-K. Wire them into the JavaScript adapter.
Hazards are language-scoped — Python hazards don't fire for JavaScript tasks.

---

### TASK 4.7: Cross-Language Transfer Limitations [NEW from R2]
**Time:** 30 minutes

Explicit registry of what does NOT transfer cleanly between languages:

```python
TRANSFER_LIMITATIONS = {
    ("python.list.append", "javascript.array.push"): [
        "JavaScript push() returns new array length; Python append() returns None",
        "JavaScript sparse arrays behave differently from Python lists",
        "JavaScript push() on frozen array throws TypeError; Python has no direct equivalent"
    ],
    ("python.dict.update", "javascript.object.assign"): [
        "Object.assign mutates first argument; dict.update mutates self — same semantics",
        "Object.assign doesn't deep merge nested objects; Python dict.update doesn't either — compatible"
    ]
}

def get_transfer_limitations(source: str, target: str) -> list[str]:
    return TRANSFER_LIMITATIONS.get((source, target), [])

# When creating invariant link between Python and JavaScript EKUs:
# Check for limitations, mark link with them
# When using linked knowledge: include limitations as constraints in prompt
```

---

## PHASE 4 EXIT CRITERIA

```bash
enable_feature("multi_language")

python -m agent learn javascript array.push
python -m agent inspect array.push
# Must show: transfer_link to python.list.append
# Must show: transfer_limitations (3 entries about differences)
# Must show: transfer_status: "confirmed" or "uncertain" (not blank)

python -m pytest tests/test_sprint4.py -v
✓ test_javascript_hazard_detected
✓ test_transfer_limitations_included_in_constraints
✓ test_transfer_validation_runs_on_new_link
```

---

---

# PHASE 5: ADVERSARIAL TESTING + PREDICTION
**Duration:** 5 hours
**Depends on:** Phase 3 complete

---

### TASK 5.1-5.3: Core Adversarial System [B]
**New file:** `agent/modules/adversarial.py`
**Time:** 2.5 hours

Agent generates tests designed to break its own knowledge:
- Boundary values
- Type violations  
- State mutations
- Composition attacks (combine two EKUs in dangerous ways)

---

### TASK 5.4: Mutation Testing Integration [NEW from R2]
**Time:** 45 minutes

Beyond adversarial tests: verify test suite actually catches bugs.

```python
@dataclass
class MutationResult:
    total_mutants: int
    killed_mutants: int
    survived_mutants: int
    mutation_score: float         # killed / total. Should be > 0.7
    surviving_mutations: list     # These reveal test gaps

def run_mutation_testing(canonical_code: str, test_suite: list[str]) -> MutationResult:
    """
    Mutate the code, check if tests catch mutations.
    If mutation_score < 0.7: tests are weak, EKU flagged for strengthening.
    """
    mutants = generate_mutants(canonical_code)
    killed = 0
    survived_mutations = []
    
    for mutant in mutants:
        all_tests_pass = all(
            run_test(mutant, test) for test in test_suite
        )
        if all_tests_pass:
            survived_mutations.append(mutant)  # Tests didn't catch this bug
        else:
            killed += 1
    
    score = killed / len(mutants) if mutants else 1.0
    return MutationResult(
        total_mutants=len(mutants),
        killed_mutants=killed,
        survived_mutants=len(survived_mutations),
        mutation_score=score,
        surviving_mutations=survived_mutations
    )
```

EKUs with `mutation_score < 0.7` get flagged: `needs_test_strengthening = True`.

---

### TASK 5.5: Prediction Confidence Calibration [NEW from R2]
**Time:** 30 minutes

Track whether claimed confidence matches actual accuracy:

```python
@dataclass
class CalibrationBucket:
    confidence_range: tuple[float, float]   # (0.8, 0.9)
    total_predictions: int
    correct_predictions: int
    
    @property
    def actual_accuracy(self) -> float:
        return self.correct_predictions / max(self.total_predictions, 1)
    
    @property  
    def calibration_error(self) -> float:
        midpoint = (self.confidence_range[0] + self.confidence_range[1]) / 2
        return abs(midpoint - self.actual_accuracy)

def adjust_confidence(raw_confidence: float, historical_accuracy: float) -> float:
    """
    If agent claims 90% but is right 60%: adjust reported confidence down.
    adjusted = raw × (historical_accuracy / raw)
    """
    if historical_accuracy == 0:
        return raw_confidence
    return raw_confidence * (historical_accuracy / raw_confidence)
```

---

## PHASE 5 EXIT CRITERIA

```bash
python -m agent audit
# Shows calibration report:
# claimed_confidence vs actual_accuracy per bucket
# calibration_error per bucket

python -m pytest tests/test_sprint5.py -v
✓ test_mutation_testing_finds_weak_tests
✓ test_surviving_mutations_flagged
✓ test_calibration_buckets_tracked
✓ test_adjusted_confidence_more_accurate
```

---

---

# PHASE 6: CHROMADB SEMANTIC SEARCH
**Duration:** 4 hours
**Depends on:** Phase 2 complete (can run parallel with Phase 5)

---

### TASK 6.1-6.2: Wire ChromaDB [B]
**File:** `agent/knowledge/vector_store.py`
**Time:** 2 hours

Enable feature flag `chromadb_enabled`. Replace stub with real ChromaDB calls.
Pre-compute embeddings on EKU save (don't compute at search time).

---

### TASK 6.3: Hybrid Search with BM25 [NEW from R2]
**Time:** 45 minutes

Pure embedding search misses exact keyword matches. Combine semantic + keyword:

```python
def hybrid_search(query: str, top_k: int = 10) -> list:
    # Semantic search via ChromaDB
    semantic_results = chromadb_search(query, top_k * 2)
    
    # Keyword search via BM25
    keyword_results = bm25_search(query, top_k * 2)
    
    # Reciprocal Rank Fusion (RRF) — standard technique
    scores = defaultdict(float)
    for rank, eku in enumerate(semantic_results):
        scores[eku.id] += 1 / (60 + rank)
    for rank, eku in enumerate(keyword_results):
        scores[eku.id] += 1 / (60 + rank)
    
    sorted_ids = sorted(scores.keys(), key=lambda x: scores[x], reverse=True)
    return [load_eku(id) for id in sorted_ids[:top_k]]
```

---

### TASK 6.4: Search Result Explanation [NEW from R2]
**Time:** 30 minutes

Why was this EKU returned? Show the reasoning:

```python
@dataclass
class SearchResultExplanation:
    eku_id: str
    relevance_score: float
    match_reasons: list[str]  # ["semantic: 'add to list' ↔ 'append element'", "keyword: 'append' exact match"]
    authority_boost: float
    usage_boost: float

# Display with --verbose flag in CLI
```

---

### TASK 6.NEW: Semantic Search Fallback Chain [NEW from R1]
**Time:** 20 minutes

Already stubbed in TASK 0.9. Now complete the fallback chain:

```
ChromaDB → JSON + Embeddings → BM25 keyword → Linear scan (last resort)
```

Each fallback logs clearly: `"ChromaDB unavailable, using JSON embedding fallback"`.
Never silently degrades without logging.

---

## PHASE 6 EXIT CRITERIA

```bash
enable_feature("chromadb_enabled")

python -m agent search "how to add element to collection"
# Must return list.append, set.add (semantic match even without keyword 'append')
# Must show match_reasons with --verbose

python -m pytest tests/test_sprint6.py -v
✓ test_hybrid_search_finds_keyword_match_without_semantic_similarity
✓ test_semantic_search_finds_conceptual_match
✓ test_search_explanation_generated
✓ test_chromadb_fallback_chain_works
```

---

---

# PHASE 7: KNOWLEDGE LIFECYCLE
**Duration:** 4 hours
**Depends on:** Phase 5 + Phase 6 complete

---

### TASK 7.1-7.4: Core Lifecycle [B]
**New files:** `agent/modules/decay_manager.py`, `agent/modules/tension.py`
**Time:** 2.5 hours

- Decay calculation: `decay_score` increases with time since last verification
- Intelligent refusal: warn before using decayed knowledge
- Background strengthening: re-verify knowledge that's been used 10+ times
- `agent strengthen <concept>` command

---

### TASK 7.5: Proactive Decay Warning [NEW from R2]
**Time:** 30 minutes

Don't wait for task to fail — warn proactively at startup:

```bash
python -m agent status
# Shows:
⚠️ KNOWLEDGE DECAY WARNINGS (run before important work):
  - list.append: decay=0.62, used 23 times, last verified 34 days ago
  - dict.update: decay=0.58, used 15 times, last verified 29 days ago

Run: agent strengthen list.append  to refresh
```

Daily background job: find EKUs where `decay_score > 0.5 AND usage_count > 5`. Add to warnings.

---

### TASK 7.6: Automatic Prerequisite Chain Refresh [NEW from R2]
**Time:** 30 minutes

When strengthening an EKU, automatically check and strengthen decayed prerequisites too:

```python
def strengthen_with_chain(eku_id: str):
    eku = load_eku(eku_id)
    prereqs = find_prerequisites(eku)
    decayed_prereqs = [p for p in prereqs if p.decay_score > 0.5]
    
    if decayed_prereqs:
        console.print(f"Prerequisites also need strengthening:")
        for prereq in decayed_prereqs:
            console.print(f"  - {prereq.concept} (decay: {prereq.decay_score:.2f})")
        
        for prereq in decayed_prereqs:
            strengthen(prereq.id)
    
    strengthen(eku_id)
```

---

## PHASE 7 EXIT CRITERIA

```bash
python -m agent strengthen list.append
# Must: check prerequisite chain, strengthen any decayed prereqs

python -m agent status
# Must show: decay warnings for EKUs not used/verified recently

python -m pytest tests/test_sprint7.py -v
✓ test_proactive_decay_warning_generated
✓ test_prerequisite_chain_refreshed
✓ test_intelligent_refusal_on_high_decay
```

---

---

# PHASE 8: SELF-IMPROVEMENT SYSTEMS
**Duration:** 4 hours
**Depends on:** Phase 7 complete

---

### TASK 8.1-8.4: Core Self-Improvement [B]
**New files:** `agent/knowledge/experience_log.py`, `agent/modules/self_audit.py`
**Time:** 2.5 hours

- Experience log: record every solved task
- Confidence calibration: compare claimed vs actual
- Confusion gap analysis: what keeps going wrong
- Self-audit command: `agent audit`

---

### TASK 8.5: Failure Pattern Mining [NEW from R2]
**Time:** 45 minutes

Weekly job: cluster failed experiences, surface recurring patterns:

```python
@dataclass
class FailurePattern:
    pattern_id: str
    description: str
    example_failures: list
    frequency: int
    concepts_involved: list[str]
    suggested_action: str

# Mining logic:
# Group experiences by error_type + concepts_used
# If same combination appears >= 3 times: create FailurePattern
# Add pattern to "avoid this" context when those concepts are used again
```

---

### TASK 8.6: Success Pattern Extraction [NEW from R2]
**Time:** 30 minutes

Mirror of failure mining, for successes:

```python
@dataclass
class SuccessPattern:
    approach: str
    example_successes: list
    frequency: int
    concepts_used: list[str]
    reuse_template: str       # Abstracted code template for similar future tasks

# When new task matches concepts from SuccessPattern:
# Surface pattern to LLM as "preferred approach"
# Include reuse_template as starting point in generation prompt
```

---

## PHASE 8 EXIT CRITERIA

```bash
python -m agent audit
# Shows: calibration report, confusion gaps, success patterns, failure patterns

python -m pytest tests/test_sprint8.py -v
✓ test_failure_pattern_mined_from_experience
✓ test_success_pattern_surfaced_for_similar_task
✓ test_confusion_gap_triggers_learning_goal
✓ test_calibration_error_calculated
```

---

---

# PHASE 9: PRODUCTION HARDENING
**Duration:** 4 hours
**Depends on:** ALL phases complete

---

### TASK 9.1-9.5: Core Hardening [B]
**Time:** 2 hours

- CLI polish: all 12+ commands working cleanly
- Error messages: all user-facing errors are helpful
- Logging: session logs complete and searchable
- Tests: full integration stress test (20+ concepts, 10+ tasks)
- Documentation: README with quick-start

---

### TASK 9.6: Graceful Degradation Matrix [NEW from R2]
**Time:** 30 minutes

Document and implement every fallback path:

| Component | Primary | Fallback 1 | Fallback 2 | Final Fallback |
|-----------|---------|------------|------------|----------------|
| Vector Search | ChromaDB | JSON + Embeddings | BM25 keyword | Linear scan |
| Embeddings | sentence-transformers | Ollama embed | TF-IDF | Jaccard |
| LLM | Ollama phi3:medium | OpenAI API | Manual queue | Refuse gracefully |
| Web Scraping | Scrapling | requests+BeautifulSoup | Cache only | Refuse |
| Sandbox | Subprocess | Docker | Refuse | — |

Every fallback: logs degradation clearly. Never silent failure.

---

### TASK 9.7: Deep Health Check [NEW from R2]
**Time:** 30 minutes

```bash
python -m agent health --deep
```

Runs:
- End-to-end learning test (learn trivial concept, verify stored)
- End-to-end solve test (solve trivial task, verify correct)
- All fallback paths (verify each works in isolation)
- Performance baseline (compare to benchmarks)

---

### TASK 9.8: Progressive Command Disclosure [NEW from R1]
**Time:** 30 minutes

Don't overwhelm new users with all 12 commands:

```
0 EKUs learned:
  Commands: learn, status, health

1+ EKUs learned:
  Commands: learn, inspect, list, status, health

5+ EKUs learned:
  Commands: learn, solve, ask, inspect, list, strengthen, status, health

20+ concepts + 10+ tasks solved:
  Full command set unlocked
```

---

## PHASE 9 EXIT CRITERIA

```bash
# Full stress test
python -m pytest tests/test_integration.py -v
# 20+ concepts learned, 10+ tasks solved, 0 crashes

python -m agent health --deep
# All checks: ✅
# All fallbacks verified: ✅
# Performance within benchmarks: ✅

# Validation checkpoints from R2:
python -m agent audit
# calibration_error < 0.15 (claimed confidence close to actual)

# Progressive disclosure working:
python -m agent help  # Shows appropriate commands for current EKU count
```

---

---

# THINGS NOBODY DOCUMENTED (FOUND BY DEEP ANALYSIS)

These are issues found by analyzing all three documents together. They are not in any single document. They are real and they will bite you.

---

## UNDOCUMENTED ISSUE 1: The Embedding Dimension Mismatch Timebomb

**What it is:** If you switch from `all-MiniLM-L6-v2` (384 dimensions) to a different embedding model later, all stored embeddings become incompatible. ChromaDB will either crash or return nonsense similarities silently.

**Where it hits:** Phase 6, when you enable ChromaDB. Also whenever you try to upgrade embedding models.

**Fix — Add to EKU schema now (TASK 0.0):**
```python
embedding_model: str = "all-MiniLM-L6-v2"    # Which model created this embedding
embedding_dim: int = 384                        # Dimension for compatibility check
```

**Add to vector_store.py:**
```python
def add(self, eku) -> None:
    current_model = config.EMBEDDING_MODEL
    if eku.embedding_model != current_model:
        # Recompute embedding with current model before storing
        eku._embedding = embedder.embed_text(f"{eku.concept} {eku.definition}")
        eku.embedding_model = current_model
```

**Why nobody caught this:** Phase 6 feels far away during Phase 0. But the data schema is set in Phase 0. Fix it now.

---

## UNDOCUMENTED ISSUE 2: The Concurrent Learning Race Condition

**What it is:** The file locking in TASK 0.NEW-B uses `fcntl` which is Unix-only. Windows will fail silently (fcntl doesn't exist). Also: locking the entire JSON index file blocks ALL reads while ONE write happens.

**Where it hits:** Immediately on Windows. On Unix: becomes a bottleneck at 100+ EKUs.

**Fix:**
```python
# In file_lock.py: Platform-aware locking
import sys

if sys.platform == "win32":
    import msvcrt
    @contextmanager
    def locked_file(path: Path, mode: str):
        f = open(path, mode)
        try:
            msvcrt.locking(f.fileno(), msvcrt.LK_NBLCK, 1)
            yield f
        finally:
            msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
            f.close()
else:
    # fcntl version (original)
    pass
```

For the bottleneck: move to per-EKU files (one file per EKU) instead of one giant index JSON. Index file only stores IDs + metadata. EKU data in individual files.

---

## UNDOCUMENTED ISSUE 3: The Ollama Context Window Silent Truncation

**What it is:** `phi3:medium` has a context window of ~4096 tokens. When your collection phase scrapes 5 URLs and feeds all content to the LLM for extraction, you may silently overflow. Ollama doesn't error — it silently truncates the input. The LLM then hallucinates from partial context.

**Where it hits:** Phase 1, Task 1.7 (compressor) and any extraction call with large scraped content.

**Fix — Add to client.py:**
```python
MAX_PROMPT_TOKENS = 3000  # Leave 1000 for response

def complete_with_truncation_guard(prompt: str, model: str = "phi3:medium") -> str:
    # Estimate tokens (rough: 1 token ≈ 0.75 words)
    estimated_tokens = len(prompt.split()) / 0.75
    
    if estimated_tokens > MAX_PROMPT_TOKENS:
        # Truncate from the MIDDLE (keep start + end, remove middle)
        words = prompt.split()
        keep_start = int(MAX_PROMPT_TOKENS * 0.75 * 0.6)  # Keep 60% from start
        keep_end = int(MAX_PROMPT_TOKENS * 0.75 * 0.3)    # Keep 30% from end
        
        truncated = words[:keep_start] + ["[...TRUNCATED...]"] + words[-keep_end:]
        prompt = " ".join(truncated)
        session_logger.log("llm", "prompt_truncated", {
            "original_tokens": estimated_tokens,
            "max_tokens": MAX_PROMPT_TOKENS
        })
    
    return complete(prompt, model=model)
```

Why truncate from the middle: the task definition (start) and the "return JSON" instruction (end) must be preserved. The middle content chunk is the most disposable.

---

## UNDOCUMENTED ISSUE 4: The ChromaDB SQLite Version Lock

**What it is:** ChromaDB requires SQLite >= 3.35.0. Many Linux systems (especially Ubuntu 20.04 LTS) ship with SQLite 3.31. ChromaDB will fail to initialize with a cryptic error about WAL mode.

**Where it hits:** Phase 6, immediately on ChromaDB initialization.

**Fix — Add to preflight_check.py:**
```python
# Check SQLite version (ChromaDB requirement)
import sqlite3
sqlite_version = tuple(int(x) for x in sqlite3.sqlite_version.split("."))
check(
    f"SQLite >= 3.35.0 (have {sqlite3.sqlite_version})",
    sqlite_version >= (3, 35, 0),
    "Run: pip install pysqlite3-binary && add 'import pysqlite3; sys.modules[\"sqlite3\"] = pysqlite3' to top of vector_store.py"
)
```

Also add to vector_store.py top:
```python
# SQLite version fix for ChromaDB on older systems
try:
    import pysqlite3
    import sys
    sys.modules["sqlite3"] = pysqlite3
except ImportError:
    pass  # If not installed, use system SQLite and hope it's >= 3.35.0
```

---

## UNDOCUMENTED ISSUE 5: The phi3:medium JSON Reliability Problem

**What it is:** From your Phase -2.3 LLM baseline, you'll likely find that phi3:medium at temperature=0 produces valid JSON roughly 75-80% of the time but fails on complex nested structures. The smart retry (TASK 1.NEW-G) helps. But there's a better fix that nobody mentioned.

**The insight:** phi3:medium is most reliable at JSON when the JSON structure is given to it explicitly.

**Fix — Structured prompt template for every JSON call:**
```python
def structured_json_prompt(task: str, schema: dict) -> str:
    schema_example = json.dumps(schema, indent=2)
    return f"""{task}

You MUST respond with ONLY valid JSON matching this exact structure:
{schema_example}

Start your response with {{ and end with }}.
Do not include any text before or after the JSON."""
```

The key: show the schema with the expected keys, not just describe it. phi3 is much better at filling a template than inventing structure.

---

## UNDOCUMENTED ISSUE 6: The DDG Rate Limiting Silent Failure

**What it is:** DuckDuckGo's scraping-based search gets rate-limited if you run multiple `learn` commands quickly. Scrapling will return empty results without raising an exception. Your scraper failure tracking (TASK 0.10) will catch SOME of this, but the failure message will be "empty response" not "rate limited."

**Fix — Add to web_search.py:**
```python
import time
_last_search_time = 0
DDG_MIN_INTERVAL = 2.0  # Minimum seconds between searches

def search(query: str, max_results: int = 5) -> list[str]:
    global _last_search_time
    
    # Rate limit protection
    elapsed = time.time() - _last_search_time
    if elapsed < DDG_MIN_INTERVAL:
        time.sleep(DDG_MIN_INTERVAL - elapsed)
    
    _last_search_time = time.time()
    
    # ... existing search code ...
    
    # Verify we actually got results
    if not results:
        session_logger.log("search", "empty_results", {
            "query": query,
            "possible_cause": "rate_limiting or no_results"
        })
    
    return results
```

---

## UNDOCUMENTED ISSUE 7: The Test Isolation Contamination

**What it is:** When the sandbox runs 9 tests for `list.append` sequentially, each test reuses the same subprocess (or in the pool case, a warm subprocess). If test 3 modifies global state and test 4 depends on a clean environment, test 4 may pass or fail based on test 3's side effects — not based on the concept being tested.

**Fix — Add to runner.py:**
```python
def run_isolated_tests(test_codes: list[str]) -> list[SandboxResult]:
    """Each test runs in a completely fresh subprocess. Zero shared state."""
    results = []
    for code in test_codes:
        # Fresh runner for EVERY test — no state contamination between tests
        runner = SandboxRunner()
        result = runner.run(code)
        results.append(result)
        del runner  # Explicit cleanup
    return results
```

The sandbox pool (TASK 1.NEW-B) must REPLACE the runner after each test, not reuse it. The pool implementation already does this (`self._pool.append(self._spawn_sandbox())` after each use). But verify it — the warmup savings only matter if the test results are still correct.

---

---

# VALIDATION CHECKPOINTS

Run these after each phase. They verify the agent is building real intelligence, not just structured storage.

**After Phase 0:**
```
Ask: "What is your confidence in list.append?"
Expected: "I have not learned this concept."
If it answers ANYTHING else: Phase 0 is incomplete.
```

**After Phase 1:**
```
After learning: python -m agent learn python list.append
Ask: "What does list.append return?"
Expected: "None. list.append modifies the list in-place and returns None. [Source: docs.python.org, confidence: 0.XX, effective_confidence: 0.XX]"
If it cannot cite source: Phase 1 incomplete.
If confidence > 0.95: confidence ceiling not working.
```

**After Phase 3:**
```
Give task: "Write a function that appends to a list while iterating over it"
Expected: WARNING about composition hazard (concurrent modification)
If it just generates code without warning: Phase 3 incomplete.
```

**After Phase 5:**
```
Run: python -m agent audit
Expected: Shows calibration_error per confidence bucket
If calibration_error is not calculated: Phase 5 incomplete.
```

**After Phase 9:**
```
Run: python -m agent health --deep
Expected: All checks pass, all fallbacks verified
If any check fails: Phase 9 incomplete.
```

---

---

# THE SINGLE MOST IMPORTANT RULE

**Do not move to Phase N+1 until Phase N's exit criteria ALL pass.**

Every phase has testable exit criteria.
They are not suggestions.
They are proof that the phase worked.
Without proof, you are guessing.
This entire project is built on the principle that guessing is the enemy.
Apply that principle to building it.

The one thing that will make this work:
Every new component serves one goal — the agent must be more confident about its uncertainty than about its knowledge.

The one thing that will break this:
Skipping Phase 0's new tasks (fingerprinting, hazards, transitive confidence) to get to Phase 1 faster.
You'll have a system that learns wrong things confidently. That is worse than no system.

---

*MASTER_PLAN.md — 2026-03-27*
*Synthesized from: PROJECT_BIBLE.md + review_report.md + review_report_2.md*
*All conflicts resolved. All duplications removed. All discoveries integrated.*
*Total: 54-57 hours of disciplined execution to production-grade learning agent.*
