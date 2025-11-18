#!/usr/bin/env python3
"""
Example usage of the websearch-ai library.

Before running, make sure to set your OpenAI API key:
    export OPENAI_API_KEY='your-api-key-here'
"""

import asyncio
import sys
from websearch_ai import WebSearchPipeline, Settings


async def main():
    """Run a simple web search example."""
    # Get query from command line or use default
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "latest developments in AI"
    
    print(f"Searching for: {query}\n")
    
    try:
        # Initialize settings from environment variables
        settings = Settings.from_env()
        
        # Create the pipeline
        pipeline = WebSearchPipeline(settings)
        
        # Run the search
        results, answer = await pipeline.run(query)
        
        # Display results
        print("=" * 80)
        print("SEARCH RESULTS")
        print("=" * 80)
        print(f"\nFound {len(results)} sources:\n")
        
        for i, result in enumerate(results, 1):
            print(f"{i}. {result.title}")
            print(f"   URL: {result.url}")
            print(f"   Snippet: {result.snippet[:100]}...")
            print()
        
        print("=" * 80)
        print("FINAL ANSWER")
        print("=" * 80)
        print(f"\n{answer}\n")
        
    except ValueError as e:
        print(f"Error: {e}")
        print("\nMake sure to set your OPENAI_API_KEY environment variable:")
        print("    export OPENAI_API_KEY='your-api-key-here'")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())

