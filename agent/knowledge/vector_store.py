"""Vector store interface — stub implementation.

This module provides the interface for semantic search and storage.
It decouples the agent from the specific vector database (e.g., ChromaDB).
"""

import logging
from typing import Any

from agent.config import feature_enabled
from agent.knowledge.eku_schema import ExecutableKnowledgeUnit

logger = logging.getLogger(__name__)


class VectorStore:
    """Interface for semantic knowledge storage.
    
    Currently a stub that returns empty results if ChromaDB is disabled.
    """

    def __init__(self):
        self.enabled = feature_enabled("chromadb_enabled")
        if not self.enabled:
            logger.info("VectorStore initialized in STUB mode (ChromaDB disabled).")

    async def add(self, eku: ExecutableKnowledgeUnit) -> None:
        """Add an EKU to the semantic index."""
        if not self.enabled:
            return
        
        # Placeholder for actual ChromaDB logic
        logger.debug(f"VectorStore.add: {eku.id} (stub)")

    async def search(self, query: str, top_k: int = 5) -> list[dict[str, Any]]:
        """Search for similar EKUs by query string.
        
        Returns a list of match dictionaries, or [] if no matches/disabled.
        """
        if not self.enabled:
            return []

        # Placeholder for actual ChromaDB query logic
        logger.debug(f"VectorStore.search: '{query}' (stub)")
        return []
