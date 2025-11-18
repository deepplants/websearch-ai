"""
Prompt manager for loading and formatting prompts from YAML.
"""
import logging
from pathlib import Path
from typing import Dict, Optional

import yaml

logger = logging.getLogger(__name__)


class PromptManager:
    """Manages loading and formatting of prompts from YAML configuration."""
    
    def __init__(self, prompts_path: Path):
        self.prompts_path = prompts_path
        self._prompts: Optional[Dict[str, str]] = None
    
    def load_prompts(self) -> Dict[str, str]:
        """Load prompts from YAML file."""
        if self._prompts is not None:
            return self._prompts
        
        try:
            with self.prompts_path.open("r", encoding="utf-8") as fh:
                data = yaml.safe_load(fh) or {}
        except FileNotFoundError as exc:
            logger.error(f"Prompt configuration missing at {self.prompts_path}")
            raise FileNotFoundError(
                f"Prompt configuration missing at {self.prompts_path}"
            ) from exc
        
        if not isinstance(data, dict):
            raise ValueError(
                f"Prompt configuration at {self.prompts_path} must be a mapping"
            )
        
        self._prompts = data
        logger.info(f"Loaded {len(self._prompts)} prompts from {self.prompts_path}")
        return self._prompts
    
    def get_prompt(self, name: str) -> str:
        """Retrieve a specific prompt by name."""
        prompts = self.load_prompts()
        try:
            return prompts[name]
        except KeyError as exc:
            logger.error(f"Prompt '{name}' not found in {self.prompts_path}")
            raise KeyError(
                f"Prompt '{name}' is not defined in {self.prompts_path}"
            ) from exc
    
    @staticmethod
    def _escape_braces(value: str) -> str:
        """Escape braces for string formatting."""
        return value.replace("{", "{{").replace("}", "}}")
    
    def format_prompt(self, template: str, **values: str) -> str:
        """Format prompt template with escaped values."""
        safe_values = {k: self._escape_braces(str(v)) for k, v in values.items()}
        return template.format(**safe_values)

