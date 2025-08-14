import json
import logging

from openai import OpenAI

from app.infrastructure.providers.llm.base_llm_provider import BaseLLMProvider


class OpenAILLMProviderBase(BaseLLMProvider):
    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def generate_prompt(self, populated_prompt: str) -> dict:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "system", "content": populated_prompt}],
                temperature=0.7,
                max_tokens=2000,
                timeout=60,
            )

            content = response.choices[0].message.content

            return json.loads(content)

        except json.JSONDecodeError as e:
            logging.getLogger(__name__).exception("Invalid JSON from LLM")
            raise ValueError(f"LLM returned invalid JSON: {e}")
        except Exception as e:
            logging.getLogger(__name__).exception("LLM API call failed")
            raise RuntimeError(f"LLM API call failed: {e}")
