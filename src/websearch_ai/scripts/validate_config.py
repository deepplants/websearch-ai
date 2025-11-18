#!/usr/bin/env python3
"""
Validate configuration files.

Usage:
    python scripts/validate_config.py [--config CONFIG_PATH]
"""
import argparse
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from websearch.config import Settings
from pydantic import ValidationError


def validate_config(config_path: str = None):
    """Validate a configuration file."""
    print("🔍 Validating Configuration...")
    print("=" * 60)
    
    try:
        if config_path:
            print(f"Loading: {config_path}")
            settings = Settings.from_yaml(config_path)
        else:
            print(f"Loading: config/config.yaml (default)")
            settings = Settings.from_yaml()
        
        print("\n✅ Configuration is valid!")
        print("\nSettings:")
        print(f"  Model: {settings.openai_model}")
        print(f"  Temperature: {settings.openai_temperature}")
        print(f"  Better Queries: {settings.search_num_better_queries}")
        print(f"  Results per Query: {settings.search_max_results_per_query}")
        print(f"  Min Relevance: {settings.min_relevance_score}")
        print(f"  Cache Enabled: {settings.cache_enabled}")
        print(f"  Cache Dir: {settings.cache_dir}")
        print(f"  Disallowed Domains: {len(settings.disallowed_domains)}")
        
        if settings.disallowed_domains:
            print(f"\n  Blocked Domains:")
            for domain in settings.disallowed_domains:
                print(f"    - {domain}")
        
        # Check prompts file
        print(f"\nPrompts File: {settings.prompts_path}")
        if settings.prompts_path.exists():
            print("  ✅ Prompts file exists")
        else:
            print("  ⚠️  Warning: Prompts file not found")
        
        # Check API key
        if settings.openai_api_key and settings.openai_api_key != "dummy":
            print(f"\nAPI Key: {'*' * 20}{settings.openai_api_key[-4:]}")
            print("  ✅ API key is set")
        else:
            print("\n⚠️  Warning: OPENAI_API_KEY not set or using dummy key")
        
        print("\n✅ Configuration validation complete!")
        return True
        
    except ValidationError as e:
        print("\n❌ Configuration validation failed!")
        print("\nErrors:")
        for error in e.errors():
            field = '.'.join(str(x) for x in error['loc'])
            print(f"  • {field}: {error['msg']}")
        return False
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Validate configuration file")
    parser.add_argument(
        "--config",
        help="Path to config file (default: config/config.yaml)"
    )
    
    args = parser.parse_args()
    
    success = validate_config(args.config)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

