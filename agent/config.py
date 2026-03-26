"""Configuration management — adapted from LocalMind config.py.

Uses pure stdlib to avoid dependency issues during early development.
Reads from environment variables and .env file.
"""

import os
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path


def _load_dotenv(path: str = ".env") -> None:
    """Minimal .env loader — no external deps."""
    env_path = Path(path)
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:  # Don't override existing env vars
            os.environ[key] = value


def _env(key: str, default: str = "") -> str:
    return os.environ.get(key, default)


def _env_int(key: str, default: int = 0) -> int:
    try:
        return int(os.environ.get(key, str(default)))
    except (ValueError, TypeError):
        return default


def _env_float(key: str, default: float = 0.0) -> float:
    try:
        return float(os.environ.get(key, str(default)))
    except (ValueError, TypeError):
        return default


class Settings:
    """Agent settings loaded from environment variables or .env file."""

    def __init__(self):
        _load_dotenv()

        # ── LLM Backend ─────────────────────────────────────────
        self.llm_backend: str = _env("LLM_BACKEND", "ollama")
        self.ollama_base_url: str = _env("OLLAMA_BASE_URL", "http://localhost:11434")
        self.lmstudio_base_url: str = _env("LMSTUDIO_BASE_URL", "http://localhost:1234/v1")
        self.openai_api_key: str = _env("OPENAI_API_KEY", "")
        self.default_model: str = _env("DEFAULT_MODEL", "qwen2.5:3b")

        # ── Embedding ───────────────────────────────────────────
        self.embedding_backend: str = _env("EMBEDDING_BACKEND", "local")
        self.embedding_model: str = _env("EMBEDDING_MODEL", "nomic-embed-text")
        self.local_embedding_model: str = _env("LOCAL_EMBEDDING_MODEL", "all-MiniLM-L6-v2")

        # ── Data Paths ──────────────────────────────────────────
        self.data_dir: str = _env("DATA_DIR", "./data")
        self.chroma_path: str = _env("CHROMA_PATH", "./data/chromadb")
        self.eku_store_path: str = _env("EKU_STORE_PATH", "./data/eku_store")
        self.sandbox_path: str = _env("SANDBOX_PATH", "/tmp/agent_sandbox")
        self.logs_path: str = _env("LOGS_PATH", "./data/logs")

        # ── Learning Parameters ─────────────────────────────────
        self.chunk_size: int = _env_int("CHUNK_SIZE", 500)
        self.chunk_overlap: int = _env_int("CHUNK_OVERLAP", 50)
        self.max_sources: int = _env_int("MAX_SOURCES", 5)
        self.entropy_threshold: float = _env_float("ENTROPY_THRESHOLD", 0.92)
        self.min_confidence_to_store: float = _env_float("MIN_CONFIDENCE_TO_STORE", 0.80)
        self.min_contexts_to_pass: int = _env_int("MIN_CONTEXTS_TO_PASS", 4)
        self.sandbox_timeout: int = _env_int("SANDBOX_TIMEOUT", 30)
        self.max_learning_iterations: int = _env_int("MAX_LEARNING_ITERATIONS", 10)

        # ── Stress Testing ──────────────────────────────────────
        self.adversarial_tests_per_eku: int = _env_int("ADVERSARIAL_TESTS_PER_EKU", 5)
        self.worst_case_scenarios: int = _env_int("WORST_CASE_SCENARIOS", 3)

    @property
    def chroma_path_resolved(self) -> Path:
        return Path(self.chroma_path).resolve()

    @property
    def eku_store_path_resolved(self) -> Path:
        return Path(self.eku_store_path).resolve()

    @property
    def sandbox_path_resolved(self) -> Path:
        return Path(self.sandbox_path).resolve()

    @property
    def logs_path_resolved(self) -> Path:
        return Path(self.logs_path).resolve()

    def ensure_directories(self) -> None:
        """Ensure all data directories exist."""
        self.chroma_path_resolved.mkdir(parents=True, exist_ok=True)
        self.eku_store_path_resolved.mkdir(parents=True, exist_ok=True)
        self.sandbox_path_resolved.mkdir(parents=True, exist_ok=True)
        self.logs_path_resolved.mkdir(parents=True, exist_ok=True)


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    settings = Settings()
    settings.ensure_directories()
    return settings
