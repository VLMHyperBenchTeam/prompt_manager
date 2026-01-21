# Prompt Manager

[Русский](README.ru.md) | English

A flexible prompt management and resolution library for VLMHyperBench.

## Features

- **Dynamic Resolution**: Select prompts based on item metadata (e.g., `doc_type`).
- **Resolution Priority**:
  1. Manual Overrides (`fixed_prompt`, `fixed_system_prompt`).
  2. Type Mapping (mapping `doc_type` to specific templates).
  3. Default Fallback (global templates).
- **Jinja2 Templating**: Powerful variable substitution in prompt templates.
- **Strict Validation**: Configuration schema validated with Pydantic v2.

## Installation

```bash
pip install prompt_manager
```

## Usage

### 1. Configuration

```json
{
  "prompt_config": {
    "system_prompt": "You are a helpful assistant.",
    "user_prompt": "Analyze this {{ doc_type }}.",
    "type_mapping": {
      "passport": {
        "system_prompt": "You are a passport specialist.",
        "user_prompt": "Extract data from this passport: {{ number }}"
      }
    }
  }
}
```

### 2. Python API

```python
from prompt_manager.manager import PromptManager

# Load from file
manager = PromptManager.from_json("config.json")

# Get prompts for an item
metadata = {"doc_type": "passport", "number": "12345"}
prompts = manager.get_prompts(metadata)

print(prompts["system_prompt"]) # "You are a passport specialist."
print(prompts["user_prompt"])   # "Extract data from this passport: 12345"
```

## License

MIT