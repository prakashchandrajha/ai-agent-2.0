import hashlib
import json
import logging
import os
from pathlib import Path
from typing import Any

from agent.config import get_settings

logger = logging.getLogger(__name__)

class LLMCache:
    """Persistent disk cache for LLM responses.
    
    Only caches deterministic calls (temperature = 0).
    Saves to data/llm_cache/ using a hash of (prompt, model).
    """
    
    def __init__(self, cache_dir: str | None = None):
        settings = get_settings()
        if cache_dir:
            self.cache_dir = Path(cache_dir)
        else:
            # Derived from settings but without modifying config.py
            self.cache_dir = Path(settings.data_dir) / "llm_cache"
            
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"LLM Cache initialized at {self.cache_dir}")

    def _get_hash(self, prompt: str, model: str) -> str:
        """Create a unique hash for the request."""
        key = f"{model}:{prompt}"
        return hashlib.sha256(key.encode("utf-8")).hexdigest()

    def get(self, prompt: str, model: str, temperature: float) -> str | dict | list | None:
        """Retrieve a cached response if available and temperature is 0."""
        if temperature > 0:
            return None
            
        cache_key = self._get_hash(prompt, model)
        cache_file = self.cache_dir / f"{cache_key}.json"
        
        if not cache_file.exists():
            return None
            
        try:
            with open(cache_file, "r") as f:
                data = json.load(f)
                # Verify it's the right prompt (optional but safer)
                if data.get("prompt") == prompt and data.get("model") == model:
                    return data.get("response")
        except Exception as e:
            logger.warning(f"Failed to read cache file {cache_file}: {e}")
            
        return None

    def set(self, prompt: str, model: str, temperature: float, response: Any) -> None:
        """Cache a response if temperature is 0."""
        if temperature > 0:
            return
            
        cache_key = self._get_hash(prompt, model)
        cache_file = self.cache_dir / f"{cache_key}.json"
        
        try:
            cache_data = {
                "model": model,
                "prompt": prompt,
                "response": response,
                "timestamp": os.path.getmtime(os.getcwd()) # placeholder or use time.time()
            }
            # Use atomic write pattern locally
            import tempfile
            with tempfile.NamedTemporaryFile("w", dir=self.cache_dir, delete=False) as tf:
                json.dump(cache_data, tf, indent=2)
                temp_name = tf.name
            os.replace(temp_name, cache_file)
        except Exception as e:
            logger.warning(f"Failed to write cache file {cache_file}: {e}")

# Global singleton
_cache = None

def get_llm_cache() -> LLMCache:
    global _cache
    if _cache is None:
        _cache = LLMCache()
    return _cache
