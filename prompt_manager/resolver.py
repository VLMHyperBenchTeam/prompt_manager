from typing import Dict, Any, Optional
from jinja2 import Template
from .schemas.prompt_config import PromptConfig, PromptTemplate

class PromptResolver:
    """
    Resolves and renders prompts based on item metadata and configuration.
    """

    def __init__(self, config: PromptConfig):
        """
        Initialize the resolver with a prompt configuration.

        Args:
            config: The PromptConfig instance containing templates and mappings.
        """
        self.config = config

    def resolve(self, item_metadata: Dict[str, Any]) -> PromptTemplate:
        """
        Resolves the appropriate templates based on metadata.

        Args:
            item_metadata: Metadata of the current item (e.g., containing 'doc_type').

        Returns:
            A PromptTemplate containing the resolved system and user prompt templates.
        """
        doc_type = item_metadata.get("doc_type")
        
        # Start with defaults
        resolved_system = self.config.system_prompt
        resolved_user = self.config.user_prompt

        # Apply mapping if doc_type exists and is in type_mapping
        if doc_type and doc_type in self.config.type_mapping:
            mapping = self.config.type_mapping[doc_type]
            if mapping.system_prompt is not None:
                resolved_system = mapping.system_prompt
            if mapping.user_prompt is not None:
                resolved_user = mapping.user_prompt

        return PromptTemplate(
            system_prompt=resolved_system,
            user_prompt=resolved_user
        )

    def render(self, template_str: Optional[str], context: Dict[str, Any]) -> str:
        """
        Renders a template string with the provided context using Jinja2.

        Args:
            template_str: The template string to render.
            context: Dictionary of variables to use in the template.

        Returns:
            The rendered string, or an empty string if template_str is None.
        """
        if not template_str:
            return ""
        
        template = Template(template_str)
        return template.render(**context)

    def resolve_and_render(
        self, 
        item_metadata: Dict[str, Any], 
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, str]:
        """
        Resolves templates and renders them.

        Args:
            item_metadata: Metadata for resolution (e.g., doc_type).
            context: Context for rendering. If None, uses item_metadata.

        Returns:
            Dictionary with 'system_prompt' and 'user_prompt'.
        """
        resolved_templates = self.resolve(item_metadata)
        render_context = context if context is not None else item_metadata

        return {
            "system_prompt": self.render(resolved_templates.system_prompt, render_context),
            "user_prompt": self.render(resolved_templates.user_prompt, render_context)
        }