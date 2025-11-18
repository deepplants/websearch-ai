#!/usr/bin/env python3
"""
Clear the cache directory.

Usage:
    python scripts/clear_cache.py [--cache-dir CACHE_DIR]
"""
import argparse
import shutil
from pathlib import Path


def clear_cache(cache_dir: str = "cache_async"):
    """Clear all cached files."""
    cache_path = Path(cache_dir)
    
    if not cache_path.exists():
        print(f"✅ Cache directory '{cache_dir}' doesn't exist - nothing to clear")
        return
    
    # Count files before deletion
    cache_files = list(cache_path.glob("*.txt"))
    file_count = len(cache_files)
    
    if file_count == 0:
        print(f"✅ Cache directory '{cache_dir}' is already empty")
        return
    
    # Calculate total size
    total_size = sum(f.stat().st_size for f in cache_files)
    size_mb = total_size / (1024 * 1024)
    
    print(f"🗑️  Clearing cache directory: {cache_dir}")
    print(f"   Files: {file_count}")
    print(f"   Size: {size_mb:.2f} MB")
    
    # Delete cache directory
    shutil.rmtree(cache_path)
    cache_path.mkdir(parents=True, exist_ok=True)
    
    print(f"✅ Cache cleared successfully!")


def main():
    parser = argparse.ArgumentParser(description="Clear the cache directory")
    parser.add_argument(
        "--cache-dir",
        default="cache_async",
        help="Cache directory to clear (default: cache_async)"
    )
    
    args = parser.parse_args()
    clear_cache(args.cache_dir)


if __name__ == "__main__":
    main()

