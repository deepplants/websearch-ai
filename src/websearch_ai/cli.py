#!/usr/bin/env python3
"""
Web Search Pipeline - Command Line Interface.

Usage:
    python -m websearch.cli "your search query"

Environment Variables:
    OPENAI_API_KEY: Your OpenAI API key (required)
"""

import asyncio
import json
import logging
import sys

from pydantic import ValidationError

from .config import Settings
from .core import WebSearchPipeline

logger = logging.getLogger(__name__)


async def async_main():
    """Async main entry point for the script."""
    # Parse query from command line
    query = (
        " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "latest nvidia earnings 2025"
    )

    # Initialize settings and pipeline
    try:
        settings = Settings.from_env()

        # Configure logging based on settings
        logging.basicConfig(
            level=getattr(logging, settings.log_level.upper()),
            format=settings.log_format,
            force=True,
        )
    except ValidationError as e:
        # Extract user-friendly error messages from ValidationError
        for error in e.errors():
            field = error["loc"][0] if error["loc"] else "unknown"
            logger.error(f"Configuration error for '{field}': {error['msg']}")
        sys.exit(1)
    except ValueError as e:
        logger.error(f"ERROR: {e}\nExample: export OPENAI_API_KEY='your-api-key-here'")
        sys.exit(1)

    pipeline = WebSearchPipeline(settings)

    # Run pipeline
    try:
        results, final_answer = await pipeline.run(query)

        # Print results
        print("\n" + "=" * 80)
        print("SEARCH RESULTS")
        print("=" * 80)
        for result in results:
            print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))

        print("\n" + "=" * 80)
        print("FINAL ANSWER")
        print("=" * 80)
        print(final_answer)

    except Exception as e:
        logger.error(f"Pipeline failed: {e}", exc_info=True)
        sys.exit(1)


def main():
    """Synchronous entry point for CLI (used by setuptools entry_points)."""
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
