import json
import logging
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from agent.config import get_settings

logger = logging.getLogger(__name__)

class SessionLogger:
    """Non-buffered JSON logger for tracking agent sessions.
    
    Ensures every log entry is written to disk immediately to prevent
    data loss during crashes or interruptions.
    """
    
    def __init__(self, session_id: str):
        settings = get_settings()
        self.session_id = session_id
        self.log_dir = Path(settings.logs_path)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        # Use filename pattern requested by user's glob
        self.log_file = self.log_dir / f"session_{session_id}.json"
        
        logger.info(f"Session logger initialized for {session_id} at {self.log_file}")

    def log(self, phase: str, event: str, data: Any = None) -> None:
        """Log a generic event to the session file."""
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "phase": phase,
            "event": event,
            "data": data,
        }
        self._flush(entry)

    def log_scrape_failure(self, url: str, reason: str) -> None:
        """Specialized log for scraping failures."""
        self.log(
            phase="collection",
            event="scrape_failure",
            data={"url": url, "reason": reason}
        )

    def log_gate_failure(self, gate: str, diagnostic: Any) -> None:
        """Specialized log for EKU storage gate failures."""
        self.log(
            phase="storage",
            event="gate_failure",
            data={"gate": gate, "diagnostic": diagnostic}
        )

    def _flush(self, entry: dict) -> None:
        """Write entry to disk immediately with no buffering (JSONL)."""
        try:
            # Use JSONL (one JSON object per line)
            # This is the standard for non-buffered logging.
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry) + "\n")
                f.flush()
                os.fsync(f.fileno())
        except Exception as e:
            logger.error(f"Failed to write to session log {self.log_file}: {e}")
