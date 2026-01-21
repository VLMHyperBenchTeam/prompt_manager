import pytest
import json
import os
from prompt_manager.manager import PromptManager
from prompt_manager.schemas.prompt_config import PromptConfig

@pytest.fixture
def sample_config():
    return {
        "system_prompt": "Default System",
        "user_prompt": "Default User: {{ name }}",
        "type_mapping": {
            "passport": {
                "system_prompt": "Passport System",
                "user_prompt": "Passport User: {{ number }}"
            },
            "invoice": {
                "user_prompt": "Invoice User: {{ amount }}"
            }
        }
    }

def test_basic_resolution(sample_config):
    manager = PromptManager(sample_config)
    
    # Test default resolution
    res = manager.get_prompts({"name": "John"}, context={"name": "John"})
    assert res["system_prompt"] == "Default System"
    assert res["user_prompt"] == "Default User: John"

def test_mapping_resolution(sample_config):
    manager = PromptManager(sample_config)
    
    # Test mapping for passport
    res = manager.get_prompts({"doc_type": "passport", "number": "123"})
    assert res["system_prompt"] == "Passport System"
    assert res["user_prompt"] == "Passport User: 123"
    
    # Test mapping for invoice (partial mapping, system prompt should be default)
    res = manager.get_prompts({"doc_type": "invoice", "amount": "100"})
    assert res["system_prompt"] == "Default System"
    assert res["user_prompt"] == "Invoice User: 100"

def test_overrides(sample_config):
    manager = PromptManager(sample_config)
    
    overrides = {
        "fixed_system_prompt": "Overridden System",
        "fixed_prompt": "Overridden User"
    }
    
    res = manager.get_prompts({"doc_type": "passport"}, overrides=overrides)
    assert res["system_prompt"] == "Overridden System"
    assert res["user_prompt"] == "Overridden User"

def test_config_fixed_prompts(sample_config):
    # Test fixed prompts directly in PromptConfig
    sample_config["fixed_system_prompt"] = "Config Fixed System"
    sample_config["fixed_prompt"] = "Config Fixed User"
    manager = PromptManager(sample_config)
    
    res = manager.get_prompts({"doc_type": "passport", "number": "123"})
    assert res["system_prompt"] == "Config Fixed System"
    assert res["user_prompt"] == "Config Fixed User"

def test_from_json(tmp_path, sample_config):
    config_file = tmp_path / "config.json"
    with open(config_file, "w") as f:
        json.dump({"prompt_config": sample_config}, f)
    
    manager = PromptManager.from_json(config_file)
    res = manager.get_prompts({"doc_type": "passport", "number": "456"})
    assert res["system_prompt"] == "Passport System"
    assert res["user_prompt"] == "Passport User: 456"