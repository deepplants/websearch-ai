#!/usr/bin/env python3
"""
Benchmark the web search pipeline with different configurations.

Usage:
    python scripts/benchmark.py [--query QUERY] [--runs RUNS]
"""

import argparse
import asyncio
import statistics
import sys
import time
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from websearch_ai import Settings, WebSearchPipeline


async def run_single_benchmark(settings: Settings, query: str) -> dict:
    """Run a single benchmark."""
    start_time = time.time()

    pipeline = WebSearchPipeline(settings)
    results, answer = await pipeline.run(query)

    elapsed = time.time() - start_time

    return {
        "elapsed": elapsed,
        "num_results": len(results),
        "answer_length": len(answer),
    }


async def benchmark_configuration(
    config_name: str, settings: Settings, query: str, runs: int
) -> dict:
    """Benchmark a specific configuration multiple times."""
    print(f"\n🔍 Testing {config_name}...")
    print(f"   Queries: {settings.search_num_better_queries}")
    print(f"   Min Relevance: {settings.min_relevance_score}")

    times = []
    result_counts = []

    for i in range(runs):
        print(f"   Run {i + 1}/{runs}...", end=" ", flush=True)

        result = await run_single_benchmark(settings, query)
        times.append(result["elapsed"])
        result_counts.append(result["num_results"])

        print(f"{result['elapsed']:.2f}s ({result['num_results']} results)")

    return {
        "config": config_name,
        "avg_time": statistics.mean(times),
        "min_time": min(times),
        "max_time": max(times),
        "std_dev": statistics.stdev(times) if len(times) > 1 else 0,
        "avg_results": statistics.mean(result_counts),
        "settings": {
            "queries": settings.search_num_better_queries,
            "results_per_query": settings.search_max_results_per_query,
            "min_relevance": settings.min_relevance_score,
        },
    }


async def main():
    parser = argparse.ArgumentParser(description="Benchmark web search pipeline")
    parser.add_argument(
        "--query",
        default="latest AI developments 2025",
        help="Search query to benchmark",
    )
    parser.add_argument(
        "--runs", type=int, default=3, help="Number of runs per configuration"
    )

    args = parser.parse_args()

    print("=" * 80)
    print("websearch Benchmark")
    print("=" * 80)
    print(f"Query: {args.query}")
    print(f"Runs per config: {args.runs}")

    # Define configurations to test
    configs = [
        (
            "Fast Mode",
            Settings(
                openai_api_key="dummy",
                search_num_better_queries=5,
                search_max_results_per_query=3,
                min_relevance_score=2,
                max_concurrent_fetches=30,
                cache_enabled=False,
            ),
        ),
        (
            "Balanced Mode",
            Settings(
                openai_api_key="dummy",
                search_num_better_queries=10,
                search_max_results_per_query=5,
                min_relevance_score=3,
                cache_enabled=False,
            ),
        ),
        (
            "Quality Mode",
            Settings(
                openai_api_key="dummy",
                search_num_better_queries=15,
                search_max_results_per_query=8,
                min_relevance_score=4,
                cache_enabled=False,
            ),
        ),
    ]

    results = []
    for config_name, settings in configs:
        try:
            result = await benchmark_configuration(
                config_name, settings, args.query, args.runs
            )
            results.append(result)
        except Exception as e:
            print(f"   ❌ Error: {e}")
            continue

    # Print summary
    print("\n" + "=" * 80)
    print("BENCHMARK SUMMARY")
    print("=" * 80)

    for result in results:
        print(f"\n{result['config']}:")
        print(f"  Average Time: {result['avg_time']:.2f}s")
        print(f"  Range: {result['min_time']:.2f}s - {result['max_time']:.2f}s")
        print(f"  Std Dev: {result['std_dev']:.2f}s")
        print(f"  Avg Results: {result['avg_results']:.1f}")
        print(f"  Settings: {result['settings']}")

    # Find fastest
    if results:
        fastest = min(results, key=lambda x: x["avg_time"])
        print(f"\n🏆 Fastest: {fastest['config']} ({fastest['avg_time']:.2f}s)")


if __name__ == "__main__":
    asyncio.run(main())
