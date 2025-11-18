"""
LLM client for OpenAI API interactions.
"""

import logging

from openai import AsyncOpenAI, OpenAIError
from pydantic import BaseModel

from ..config import Settings

logger = logging.getLogger(__name__)


class LLMClient:
    """Handles interactions with OpenAI's LLM API."""

    def __init__(self, settings: Settings):
        self.settings = settings
        self.client: AsyncOpenAI | None = None

        if settings.openai_api_key:
            self.client = AsyncOpenAI(api_key=settings.openai_api_key)
            logger.info("LLM client initialized")
        else:
            logger.warning("LLM client not initialized (missing API key)")

    async def call_text(self, prompt: str, max_tokens: int | None = None) -> str:
        """Call LLM with text output."""
        if not self.client:
            logger.warning("LLM unavailable")
            return "LLM unavailable (missing OPENAI_API_KEY)."

        if max_tokens is None:
            max_tokens = self.settings.llm_tokens_summarize

        try:
            response = await self.client.responses.create(
                model=self.settings.openai_model,
                input=[{"role": "user", "content": prompt}],
                temperature=self.settings.openai_temperature,
                max_output_tokens=max_tokens,
            )
            text = response.output_text or ""
            logger.debug(f"LLM call successful ({len(text)} chars)")
            return text.strip()
        except OpenAIError as exc:
            logger.error(f"OpenAI API call failed: {exc}")
            return "LLM request failed."
        except Exception as exc:
            logger.error(f"Unexpected error during LLM call: {exc}")
            return "LLM request failed."

    async def call_structured(
        self,
        prompt: str,
        response_model: type[BaseModel],
        max_tokens: int | None = None,
    ) -> BaseModel | None:
        """Call LLM with structured output."""
        if not self.client:
            logger.warning("LLM unavailable")
            return None

        if max_tokens is None:
            max_tokens = self.settings.llm_tokens_better_queries

        try:
            response = await self.client.responses.parse(
                model=self.settings.openai_model,
                input=[{"role": "user", "content": prompt}],
                temperature=self.settings.openai_temperature,
                max_output_tokens=max_tokens,
                text_format=response_model,
            )
            logger.debug("LLM structured call successful")
            return response.output_parsed
        except OpenAIError as exc:
            logger.error(f"OpenAI API call failed: {exc}")
            return None
        except Exception as exc:
            logger.error(f"Unexpected error during LLM call: {exc}")
            return None
