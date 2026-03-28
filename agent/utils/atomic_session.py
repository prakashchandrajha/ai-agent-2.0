"""Atomic Learning Sessions.

Provides context managers for atomic file operations and safe writes.
"""

import json
import logging
import os
import shutil
import tempfile
from pathlib import Path

logger = logging.getLogger(__name__)

class AtomicLearningSession:
    """Context manager for atomic learning session saves."""
    
    def __init__(self, concept: str, base_dir: str | Path | None = None):
        """Initialize the session."""
        self.concept = concept
        
        if base_dir is None:
            try:
                from agent.config import get_settings
                self.base_dir = Path(get_settings().internal_memory_dir)
            except Exception:
                self.base_dir = Path(".data/memory")
        else:
            self.base_dir = Path(base_dir)
            
        self._temp_dir_path: Path | None = None
        self._committed = False

    @property
    def _temp_dir(self) -> Path:
        """Returns the temporary directory path."""
        if not self._temp_dir_path:
            raise RuntimeError("Temporary directory not initialized. Use within context manager.")
        return self._temp_dir_path

    def __enter__(self) -> "AtomicLearningSession":
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self._temp_dir_path = Path(tempfile.mkdtemp(prefix=f".tmp_{self.concept}_", dir=self.base_dir))
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self._committed and self._temp_dir_path and self._temp_dir_path.exists():
            try:
                shutil.rmtree(self._temp_dir_path)
                logger.debug(f"Cleaned up uncommitted atomic session temp dir: {self._temp_dir_path}")
            except Exception as e:
                logger.error(f"Failed to clean up atomic session temp dir {self._temp_dir_path}: {e}")

    def save_intermediate(self, filename: str, data: dict) -> None:
        """Saves a dict as JSON to the temp directory."""
        file_path = self._temp_dir / filename
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
            
    def commit(self, final_dest: Path) -> None:
        """Commit the session by atomically moving temp dir to final_dest."""
        if self._committed:
            return
            
        if not self._temp_dir_path or not self._temp_dir_path.exists():
            raise RuntimeError("Cannot commit: Temporary directory does not exist.")
            
        final_dest = Path(final_dest)
        
        if final_dest.exists():
            shutil.rmtree(final_dest, ignore_errors=True)
        else:
            # Ensure parent directories exist
            final_dest.parent.mkdir(parents=True, exist_ok=True)
            
        # os.replace requires rename to be on same filesystem. 
        # temp_dir is created inside base_dir, and user script tests move to 'data/tmp/...'. 
        # If 'data/tmp' is on the same FS, os.replace works. Otherwise we fallback to shutil.move.
        try:
            os.replace(self._temp_dir_path, final_dest)
        except OSError:
            shutil.move(str(self._temp_dir_path), str(final_dest))
            
        self._committed = True
        logger.debug(f"Committed atomic session for concept '{self.concept}' to {final_dest}")
