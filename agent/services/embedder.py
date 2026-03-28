"""Embedding service with automatic CUDA/CPU acceleration."""

import logging

import httpx
import numpy as np

from agent.config import get_settings
from agent.utils.hardware import AcceleratorType, detect_hardware

logger = logging.getLogger(__name__)


class Embedder:
    """Generates embeddings using local model or Ollama."""

    def __init__(self):
        self.settings = get_settings()
        self._local_model = None
        self._device = None
        self._hardware = detect_hardware()
        self._init_device()

    def _init_device(self) -> None:
        if self._hardware.primary_gpu.is_available:
            self._device = "cuda"
            logger.info(f"Embedder using CUDA: {self._hardware.primary_gpu.name}")
        else:
            self._device = "cpu"
            logger.info(f"Embedder using CPU with {self._hardware.cpu.total_cores} threads")

    @property
    def local_model(self):
        if self._local_model is None and self.settings.embedding_backend == "local":
            try:
                from sentence_transformers import SentenceTransformer
                model_name = self.settings.local_embedding_model
                self._local_model = SentenceTransformer(
                    model_name,
                    device=self._device,
                )
                if self._device == "cuda" and self._hardware.primary_gpu.supports_fp16:
                    self._local_model.half()
                logger.info(f"Loaded embedding model '{model_name}' on {self._device}")
            except ImportError:
                logger.error("sentence-transformers not installed. Please pip install it.")
                raise
        return self._local_model

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
            
        if self.settings.embedding_backend == "local":
            return self._embed_local_batch(texts)
        else:
            return self._embed_ollama_batch(texts)

    def _embed_local_batch(self, texts: list[str]) -> list[list[float]]:
        batch_size = 32 if self._device == "cuda" else min(32, self._hardware.cpu.total_cores * 2)
        
        embeddings = self.local_model.encode(
            texts,
            batch_size=batch_size,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=False,
        )
        return [emb.tolist() for emb in embeddings]

    def _embed_ollama_batch(self, texts: list[str]) -> list[list[float]]:
        embeddings = []
        with httpx.Client(timeout=60) as client:
            for text in texts:
                try:
                    response = client.post(
                        f"{self.settings.ollama_base_url}/api/embeddings",
                        json={
                            "model": self.settings.embedding_model,
                            "prompt": text,
                        },
                    )
                    response.raise_for_status()
                    embeddings.append(response.json()["embedding"])
                except Exception as e:
                    raise RuntimeError(f"Ollama embedding failed: {e}") from e
        return embeddings

    def embed_batch(self, texts: list[str]) -> np.ndarray:
        """Embed a batch of texts and return as a numpy array."""
        embeddings = self.embed_texts(texts)
        return np.array(embeddings)

    def cosine_similarity_matrix(self, embeddings: np.ndarray) -> np.ndarray:
        """Compute the full cosine similarity matrix for a set of embeddings.
        
        Assumes input is a 2D numpy array of shape (n_texts, dim).
        If embeddings are normalized, this is a simple dot product.
        """
        if embeddings.size == 0:
            return np.array([[]])
            
        # Ensure normalization for cosine similarity calculation
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        # Avoid division by zero
        norms[norms == 0] = 1.0
        norm_embeddings = embeddings / norms
        
        return np.dot(norm_embeddings, norm_embeddings.T)


_embedder: Embedder | None = None


def get_embedder() -> Embedder:
    global _embedder
    if _embedder is None:
        _embedder = Embedder()
    return _embedder
