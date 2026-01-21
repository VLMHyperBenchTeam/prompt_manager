from typing import Dict, Optional
from pydantic import BaseModel, Field

class PromptTemplate(BaseModel):
    """
    Template for prompts.
    """
    system_prompt: Optional[str] = Field(None, description="System prompt template")
    user_prompt: Optional[str] = Field(None, description="User prompt template")

class PromptConfig(BaseModel):
    """
    Configuration for prompt management.
    """
    system_prompt: Optional[str] = Field(None, description="Default global system prompt")
    user_prompt: Optional[str] = Field(None, description="Default global user prompt")
    type_mapping: Dict[str, PromptTemplate] = Field(
        default_factory=dict, 
        description="Mapping from doc_type to specific templates"
    )