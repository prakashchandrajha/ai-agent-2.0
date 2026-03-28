"""Unified LLM client — stolen from LocalMind, adapted for agent use.

Supports Ollama, LM Studio, and OpenAI-compatible backends.
Both sync and async generation with streaming.
"""

from collections.abc import AsyncGenerator
from typing import Any

import httpx
from openai import AsyncOpenAI

from agent.config import get_settings


class LLMClient:
    """Unified async interface for local and remote LLM backends."""

    def __init__(self):
        self.settings = get_settings()
        self._openai_client: AsyncOpenAI | None = None

    @property
    def backend(self) -> str:
        return self.settings.llm_backend

    @property
    def base_url(self) -> str:
        if self.backend == "ollama":
            return self.settings.ollama_base_url
        elif self.backend == "lmstudio":
            return self.settings.lmstudio_base_url
        else:  # openai
            return "https://api.openai.com/v1"

    @property
    def openai_client(self) -> AsyncOpenAI:
        if self._openai_client is None:
            kwargs: dict[str, Any] = {"base_url": self.base_url}
            if self.backend == "openai":
                kwargs["api_key"] = self.settings.openai_api_key
            else:
                kwargs["api_key"] = "not-needed"
            self._openai_client = AsyncOpenAI(**kwargs)
        return self._openai_client

    # ── Core generation ──────────────────────────────────────────

    async def generate(
        self,
        prompt: str,
        model: str | None = None,
        system_prompt: str | None = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        json_mode: bool = True,
    ) -> str:
        """Generate a complete response (non-streaming)."""
        model = model or self.settings.default_model
        if self.backend == "ollama":
            return await self._generate_ollama(
                prompt, model, system_prompt, temperature, max_tokens, json_mode
            )
        return await self._generate_openai(
            prompt, model, system_prompt, temperature, max_tokens
        )

    async def stream_generate(
        self,
        prompt: str,
        model: str | None = None,
        system_prompt: str | None = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
    ) -> AsyncGenerator[str, None]:
        """Generate with streaming."""
        model = model or self.settings.default_model
        if self.backend == "ollama":
            async for chunk in self._stream_ollama(
                prompt, model, system_prompt, temperature, max_tokens
            ):
                yield chunk
        else:
            async for chunk in self._stream_openai(
                prompt, model, system_prompt, temperature, max_tokens
            ):
                yield chunk

    # ── Ollama backend ───────────────────────────────────────────

    async def _generate_ollama(
        self, prompt: str, model: str, system_prompt: str | None,
        temperature: float, max_tokens: int, json_mode: bool = True,
    ) -> str:
        async with httpx.AsyncClient() as client:
            payload: dict[str, Any] = {
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": temperature,
                    "num_predict": max_tokens,
                },
            }
            if json_mode:
                payload["format"] = "json"
            if system_prompt:
                payload["system"] = system_prompt

            response = await client.post(
                f"{self.settings.ollama_base_url}/api/generate",
                json=payload,
                timeout=300,
            )
            response.raise_for_status()
            return response.json().get("response", "")

    async def _stream_ollama(
        self, prompt: str, model: str, system_prompt: str | None,
        temperature: float, max_tokens: int,
    ) -> AsyncGenerator[str, None]:
        import json as _json

        async with httpx.AsyncClient() as client:
            payload: dict[str, Any] = {
                "model": model,
                "prompt": prompt,
                "stream": True,
                "options": {
                    "temperature": temperature,
                    "num_predict": max_tokens,
                },
            }
            if system_prompt:
                payload["system"] = system_prompt

            async with client.stream(
                "POST",
                f"{self.settings.ollama_base_url}/api/generate",
                json=payload,
                timeout=120,
            ) as response:
                async for line in response.aiter_lines():
                    if line:
                        try:
                            data = _json.loads(line)
                            if "response" in data:
                                yield data["response"]
                        except _json.JSONDecodeError:
                            continue

    # ── OpenAI-compatible backend ────────────────────────────────

    async def _generate_openai(
        self, prompt: str, model: str, system_prompt: str | None,
        temperature: float, max_tokens: int,
    ) -> str:
        messages: list[dict[str, str]] = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = await self.openai_client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content or ""

    async def _stream_openai(
        self, prompt: str, model: str, system_prompt: str | None,
        temperature: float, max_tokens: int,
    ) -> AsyncGenerator[str, None]:
        messages: list[dict[str, str]] = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        stream = await self.openai_client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=True,
        )
        async for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    # ── Health check ─────────────────────────────────────────────

    async def check_health(self) -> dict[str, Any]:
        try:
            if self.backend == "ollama":
                async with httpx.AsyncClient() as client:
                    r = await client.get(
                        f"{self.settings.ollama_base_url}/api/tags", timeout=5
                    )
                    return {
                        "status": "healthy" if r.status_code == 200 else "unhealthy",
                        "backend": self.backend,
                    }
            else:
                models = await self.openai_client.models.list()
                return {
                    "status": "healthy" if models.data else "unhealthy",
                    "backend": self.backend,
                }
        except Exception as e:
            return {"status": "unhealthy", "backend": self.backend, "error": str(e)}


# ── Singleton ────────────────────────────────────────────────────
_llm_client: LLMClient | None = None


def get_llm_client() -> LLMClient:
    global _llm_client
    if _llm_client is None:
        _llm_client = LLMClient()
    return _llm_client
