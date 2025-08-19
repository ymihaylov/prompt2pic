import json
from openai import OpenAI
from app.core.interfaces import LLMProvider


class OpenAILLMProvider(LLMProvider):
    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def generate_prompts(self, populated_prompt: str) -> dict:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "system", "content": populated_prompt}],
                temperature=0.7,
                max_tokens=2000,
            )
            
            content = response.choices[0].message.content
            return json.loads(content)
            
        except json.JSONDecodeError as e:
            raise ValueError(f"LLM returned invalid JSON: {e}")
        except Exception as e:
            raise RuntimeError(f"LLM API call failed: {e}")
