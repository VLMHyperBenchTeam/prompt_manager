# Prompt Manager

English | [Русский](README.ru.md)

Гибкая библиотека для управления и разрешения промптов в VLMHyperBench.

## Возможности

- **Динамическое разрешение**: Выбор промптов на основе метаданных элемента (например, `doc_type`).
- **Приоритеты разрешения**:
  1. Ручные переопределения (`fixed_prompt`, `fixed_system_prompt`).
  2. Маппинг типов (сопоставление `doc_type` конкретным шаблонам).
  3. Fallback (шаблоны по умолчанию).
- **Шаблонизация Jinja2**: Мощная подстановка переменных в шаблоны промптов.
- **Строгая валидация**: Схема конфигурации валидируется через Pydantic v2.

## Установка

```bash
pip install prompt_manager
```

## Использование

### 1. Конфигурация

```json
{
  "prompt_config": {
    "system_prompt": "Вы — помощник по распознаванию документов.",
    "user_prompt": "Проанализируйте этот документ типа {{ doc_type }}.",
    "type_mapping": {
      "passport": {
        "system_prompt": "Вы — специалист по паспортам.",
        "user_prompt": "Извлеките данные из этого паспорта: {{ number }}"
      }
    }
  }
}
```

### 2. Python API

```python
from prompt_manager.manager import PromptManager

# Загрузка из файла
manager = PromptManager.from_json("config.json")

# Получение промптов для элемента
metadata = {"doc_type": "passport", "number": "12345"}
prompts = manager.get_prompts(metadata)

print(prompts["system_prompt"]) # "Вы — специалист по паспортам."
print(prompts["user_prompt"])   # "Извлеките данные из этого паспорта: 12345"
```

## Лицензия

MIT