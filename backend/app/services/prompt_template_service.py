from pathlib import Path
from typing import Dict, Any

from app.core.prompt_config import PROMPT_CONFIGS, PromptConfig


class PromptTemplateService:
    def __init__(self):
        self._template_cache: Dict[str, str] = {}

    def get_populated_prompt(
            self, template_name: str, variables: Dict[str, Any]
    ) -> str:
        config = self._get_config(template_name)

        template_content = self._load_template(config.file_path)

        self._validate_variables(variables, config)

        populated_prompt = self._populate_template(template_content, variables)

        return populated_prompt

    def _get_config(self, template_name: str) -> PromptConfig:
        if template_name not in PROMPT_CONFIGS:
            raise ValueError(f"Unknown template: {template_name}")

        return PROMPT_CONFIGS[template_name]

    def _load_template(self, file_path: str) -> str:
        # Use cache if available
        if file_path in self._template_cache:
            return self._template_cache[file_path]

        # Load from file
        template_path = Path(file_path)
        if not template_path.exists():
            raise FileNotFoundError(f"Template file not found: {file_path}")

        with open(template_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Cache the content
        self._template_cache[file_path] = content

        return content

    def _validate_variables(
            self, variables: Dict[str, Any], config: PromptConfig
    ) -> None:
        missing_vars = []
        for required_var in config.required_variables:
            if required_var not in variables:
                missing_vars.append(required_var)

        if missing_vars:
            raise ValueError(
                f"Missing required variables for template '{config.name}': {missing_vars}"
            )

    def _populate_template(self, template: str, variables: Dict[str, Any]) -> str:
        result = template
        for var_name, var_value in variables.items():
            placeholder = "{{" + var_name + "}}"
            result = result.replace(placeholder, str(var_value))
        return result
