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

import re

def extract_json(content: str) -> dict | list | None:
    """Extract JSON from LLM output, handling think tags, markdown fences, and noise.
    """
    if not content:
        return None
        
    try:
        # 1. Strip reasoning model think tags (greedy to handle nested tags)
        content = re.sub(r'<think>.*</think>', '', content, flags=re.DOTALL)
        
        # 2. Extract content from markdown code blocks if present
        json_match = re.search(r'```(?:json)?\s*(.*?)\s*```', content, re.DOTALL)
        if json_match:
            json_content = json_match.group(1)
        else:
            json_content = content

        # 3. Find absolute JSON boundaries (first {/[ to last }/])
        first_brace = json_content.find('{')
        first_bracket = json_content.find('[')
        
        if first_brace == -1 and first_bracket == -1:
            return None
            
        start_idx = first_brace if (first_brace != -1 and (first_bracket == -1 or first_brace < first_bracket)) else first_bracket
        
        last_brace = json_content.rfind('}')
        last_bracket = json_content.rfind(']')
        end_idx = max(last_brace, last_bracket) + 1
        
        if end_idx <= start_idx:
            return None
            
        json_content = json_content[start_idx:end_idx].strip()

        # 4. Clean common Python/LLM literal noise
        json_content = json_content.replace(': None', ': null').replace(': True', ': true').replace(': False', ': false')
        json_content = json_content.replace(':None', ':null').replace(':True', ':true').replace(':False', ':false')

        try:
            return json.loads(json_content)
        except json.JSONDecodeError:
            # Try fixing trailing commas before giving up
            cleaned = re.sub(r',\s*([\]}])', r'\1', json_content)
            return json.loads(cleaned)
            
    except Exception as e:
        logger.error(f"Unexpected error extracting JSON: {e}")
        return None


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
