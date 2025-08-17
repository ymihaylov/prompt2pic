"""
LLM service for OpenAI integration.
"""

import json

from openai import OpenAI


class LLMService:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    def generate_image_prompts(self, populated_prompt: str) -> dict:
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "system", "content": populated_prompt}],
                temperature=0.7,
                max_tokens=2000,
            )

            content = response.choices[0].message.content

            # Parse JSON response
            result = json.loads(content)
            return result

        except json.JSONDecodeError as e:
            raise ValueError(f"LLM returned invalid JSON: {e}")
        except Exception as e:
            raise RuntimeError(f"LLM API call failed: {e}")
