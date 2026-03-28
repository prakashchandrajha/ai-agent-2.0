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
