"""Context Fingerprinting System.

Captures and compares execution environment state to ensure knowledge applicability.
"""

import hashlib
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


def compute_fingerprint(relevant_files: list[str] = None) -> dict[str, Any]:
    """Compute a fingerprint of current execution context.
    
    Includes:
    - Runtime version (Python)
    - Timestamp
    - SHA-256 hashes of specified files
    - Versions of key dependencies
    """
    fingerprint = {
        "runtime_version": sys.version,
        "computed_at": datetime.now().isoformat(),
        "file_hashes": {},
        "dependency_versions": {}
    }
    
    # 1. Hash relevant files if provided
    if relevant_files:
        for filepath in relevant_files:
            path = Path(filepath)
            if path.exists():
                try:
                    content = path.read_bytes()
                    fingerprint["file_hashes"][filepath] = hashlib.sha256(content).hexdigest()[:12]
                except Exception:
                    pass
    
    # 2. Capture key package versions
    # We use importlib.metadata (modern stdlib) instead of pkg_resources
    try:
        from importlib.metadata import version
        for pkg in ["scrapling", "chromadb", "sentence-transformers", "tiktoken", "httpx", "numpy"]:
            try:
                fingerprint["dependency_versions"][pkg] = version(pkg)
            except Exception:
                pass
    except ImportError:
        # Fallback for very old Python < 3.8 (though project requires 3.10+)
        pass
        
    return fingerprint


def fingerprints_match(stored: dict[str, Any], current: dict[str, Any]) -> tuple[bool, list[str]]:
    """Compare fingerprints. Returns (matches, list_of_differences)."""
    differences = []
    
    # Check runtime (Python version)
    if stored.get("runtime_version") != current.get("runtime_version"):
        differences.append(
            f"Runtime changed: {stored.get('runtime_version')} -> {current.get('runtime_version')}"
        )
    
    # Check file hashes
    stored_hashes = stored.get("file_hashes", {})
    current_hashes = current.get("file_hashes", {})
    
    for filepath, stored_hash in stored_hashes.items():
        current_hash = current_hashes.get(filepath)
        if current_hash is None:
            differences.append(f"File missing in current context: {filepath}")
        elif current_hash != stored_hash:
            differences.append(f"File modified: {filepath}")
            
    # Check dependency versions
    stored_deps = stored.get("dependency_versions", {})
    current_deps = current.get("dependency_versions", {})
    
    for pkg, stored_ver in stored_deps.items():
        current_ver = current_deps.get(pkg)
        if current_ver != stored_ver:
            differences.append(f"Dependency {pkg} version changed: {stored_ver} -> {current_ver}")
            
    return len(differences) == 0, differences
