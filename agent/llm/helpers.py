"""LLM helper utilities — stolen from PageIndex utils.py.

Provides JSON extraction, retry-wrapped completions, and token counting.
"""

import asyncio
import json
import logging
import time
from typing import Any

from agent.llm.client import get_llm_client

logger = logging.getLogger(__name__)


# ── JSON extraction (from PageIndex) ─────────────────────────────

def extract_json(content: str) -> dict | list:
    """Extract JSON from LLM output, handling ```json blocks and common issues.

    Stolen from PageIndex utils.py — handles None→null, trailing commas,
    whitespace noise, and markdown code fences.
    """
    try:
        start_idx = content.find("```json")
        if start_idx != -1:
            start_idx += 7
            end_idx = content.rfind("```")
            json_content = content[start_idx:end_idx].strip()
        else:
            # Try raw JSON — find first { or [
            json_content = content.strip()
            for i, ch in enumerate(json_content):
                if ch in ('{', '['):
                    json_content = json_content[i:]
                    break

        # Clean common LLM output issues
        json_content = json_content.replace('None', 'null')
        json_content = json_content.replace('True', 'true')
        json_content = json_content.replace('False', 'false')

        return json.loads(json_content)
    except json.JSONDecodeError:
        try:
            # Remove trailing commas before ] or }
            cleaned = json_content.replace(',]', ']').replace(',}', '}')
            return json.loads(cleaned)
        except Exception:
            logger.error(f"Failed to parse JSON from LLM output: {content[:200]}...")
            return {}
    except Exception as e:
        logger.error(f"Unexpected error extracting JSON: {e}")
        return {}


# ── Retry-wrapped completions ────────────────────────────────────

async def llm_complete(
    prompt: str,
    system_prompt: str | None = None,
    model: str | None = None,
    temperature: float = 0.1,
    max_tokens: int = 4096,
    max_retries: int = 3,
    parse_json: bool = False,
) -> str | dict | list:
    """Complete a prompt with automatic retries.

    Args:
        prompt: User prompt.
        system_prompt: Optional system prompt.
        model: Model override.
        temperature: Sampling temperature (low for structured output).
        max_tokens: Max tokens to generate.
        max_retries: Number of retries on failure.
        parse_json: If True, parse response as JSON.

    Returns:
        Raw string or parsed JSON depending on parse_json flag.
    """
    client = get_llm_client()

    for attempt in range(max_retries):
        try:
            response = await client.generate(
                prompt=prompt,
                model=model,
                system_prompt=system_prompt,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            if parse_json:
                result = extract_json(response)
                if result:  # Got valid JSON
                    return result
                if attempt < max_retries - 1:
                    logger.warning(f"JSON parse failed, retrying ({attempt + 1}/{max_retries})")
                    await asyncio.sleep(0.5)
                    continue
                return result  # Return empty dict/list on final attempt
            return response
        except Exception as e:
            logger.error(f"LLM completion failed (attempt {attempt + 1}): {e}")
            if attempt < max_retries - 1:
                await asyncio.sleep(1)
            else:
                raise

    return "" if not parse_json else {}


async def llm_complete_json(
    prompt: str,
    system_prompt: str | None = None,
    model: str | None = None,
    temperature: float = 0.0,
    max_retries: int = 3,
) -> dict | list:
    """Convenience wrapper — complete and parse as JSON."""
    return await llm_complete(
        prompt=prompt,
        system_prompt=system_prompt,
        model=model,
        temperature=temperature,
        max_retries=max_retries,
        parse_json=True,
    )
