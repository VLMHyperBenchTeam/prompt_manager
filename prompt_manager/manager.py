import json
from typing import Dict, Any, Optional, Union
from pathlib import Path
from .schemas.prompt_config import PromptConfig
from .resolver import PromptResolver

class PromptManager:
    """
    Main entry point for prompt management.
    Loads configurations and coordinates resolution.
    """

    def __init__(self, config: Union[PromptConfig, Dict[str, Any]]):
        """
        Initialize PromptManager.

        Args:
            config: PromptConfig instance or dictionary.
        """
        if isinstance(config, dict):
            self.config = PromptConfig(**config)
        else:
            self.config = config
        
        self.resolver = PromptResolver(self.config)

    @classmethod
    def from_json(cls, file_path: Union[str, Path]) -> "PromptManager":
        """
        Load configuration from a JSON file.

        Args:
            file_path: Path to the JSON file.

        Returns:
            PromptManager instance.
        """
        with open(file_path, "r", encoding="utf-8") as f:
            config_data = json.load(f)
        
        # If the JSON has a top-level "prompt_config" key, use its value
        if "prompt_config" in config_data:
            config_data = config_data["prompt_config"]
            
        return cls(config_data)

    def get_prompts(
        self, 
        item_metadata: Dict[str, Any], 
        overrides: Optional[Dict[str, Any]] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, str]:
        """
        Get resolved and rendered prompts for an item, applying optional overrides.

        Args:
            item_metadata: Metadata for resolution (e.g., doc_type).
            overrides: Manual overrides for 'fixed_prompt' or 'fixed_system_prompt'.
            context: Context for rendering templates.

        Returns:
            Dictionary with 'system_prompt' and 'user_prompt'.
        """
        # Resolve templates
        prompts = self.resolver.resolve_and_render(item_metadata, context)

        # Apply overrides (ADR-009: Override has highest priority)
        if overrides:
            if "fixed_system_prompt" in overrides and overrides["fixed_system_prompt"] is not None:
                prompts["system_prompt"] = overrides["fixed_system_prompt"]
            if "fixed_prompt" in overrides and overrides["fixed_prompt"] is not None:
                prompts["user_prompt"] = overrides["fixed_prompt"]

        return prompts