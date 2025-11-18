#!/usr/bin/env python3
"""
Export search results to various formats (JSON, CSV, Markdown).

Usage:
    python scripts/export_results.py "query" --format json --output results.json
"""
import asyncio
import argparse
import json
import csv
import sys
from pathlib import Path
from typing import List

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from websearch import Settings, WebSearchPipeline, SearchResult


def export_json(results: List[SearchResult], answer: str, output_file: str):
    """Export results to JSON format."""
    data = {
        "final_answer": answer,
        "results": [r.to_dict() for r in results]
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Exported to JSON: {output_file}")


def export_csv(results: List[SearchResult], answer: str, output_file: str):
    """Export results to CSV format."""
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        # Header
        writer.writerow(['Title', 'URL', 'Relevance', 'Query', 'Snippet', 'Summary'])
        
        # Results
        for r in results:
            writer.writerow([
                r.title,
                r.url,
                r.relevance,
                r.better_query,
                r.snippet,
                r.summary or ''
            ])
    
    print(f"✅ Exported to CSV: {output_file}")


def export_markdown(results: List[SearchResult], answer: str, output_file: str):
    """Export results to Markdown format."""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Search Results\n\n")
        
        f.write("## Final Answer\n\n")
        f.write(f"{answer}\n\n")
        
        f.write("## Sources\n\n")
        for i, r in enumerate(results, 1):
            f.write(f"### {i}. {r.title}\n\n")
            f.write(f"**URL:** {r.url}  \n")
            f.write(f"**Relevance:** {r.relevance}/5  \n")
            f.write(f"**Query:** {r.better_query}  \n\n")
            
            if r.summary:
                f.write(f"**Summary:** {r.summary}\n\n")
            
            f.write("---\n\n")
    
    print(f"✅ Exported to Markdown: {output_file}")


async def main():
    parser = argparse.ArgumentParser(description="Export search results")
    parser.add_argument("query", help="Search query")
    parser.add_argument(
        "--format",
        choices=["json", "csv", "markdown"],
        default="json",
        help="Output format"
    )
    parser.add_argument(
        "--output",
        help="Output file path (default: results.{format})"
    )
    
    args = parser.parse_args()
    
    # Default output filename
    if not args.output:
        args.output = f"results.{args.format}"
    
    print(f"🔍 Running search: {args.query}")
    
    # Load settings and run search
    settings = Settings.from_yaml()
    pipeline = WebSearchPipeline(settings)
    
    try:
        results, answer = await pipeline.run(args.query)
        
        print(f"\n✅ Search complete: {len(results)} results")
        
        # Export based on format
        if args.format == "json":
            export_json(results, answer, args.output)
        elif args.format == "csv":
            export_csv(results, answer, args.output)
        elif args.format == "markdown":
            export_markdown(results, answer, args.output)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())

