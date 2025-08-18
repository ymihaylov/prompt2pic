"""
LLM service for OpenAI integration.
"""

import json

from openai import OpenAI


class LLMService:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    def generate_image_prompts(self, populated_prompt: str) -> dict:
        return self.simulate_image_prompts(populated_prompt)

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

    def simulate_image_prompts(self, populated_prompt: str) -> dict:
        return {
            "hero": {
                "prompt": "A vibrant and inviting landscape banner that captures the essence of PawPrint, showcasing a beautiful outdoor pet-friendly environment filled with families and adults enjoying quality time with their pets. The scene features lush greenery in forest green tones, complemented by accents of golden yellow in the sunlit atmosphere. The image conveys a sense of community and joy among pet owners, highlighting the love for animals while ensuring it appeals to the target demographic of adults aged 25-55. Soft natural light bathes the scene, creating an inviting and modern feel.",
                "aspect": "16:9",
            },
            "about": {
                "prompt": "A warm and personal portrait image showcasing the dedicated staff of PawPrint interacting with happy customers and their pets in a cozy store setting. The staff members, reflecting a diverse group of adults, are engaged in conversation, helping families choose products, and showcasing the brand's friendly personality. The background features soft forest green and golden yellow accents, enhancing the welcoming atmosphere. The lighting is soft and inviting, creating a trustworthy and approachable vibe.",
                "aspect": "3:4",
            },
            "gallery": [
                {
                    "prompt": "A clean and professional square image capturing a beautifully arranged selection of PawPrint's top pet products, including toys, treats, and accessories, displayed on rustic wooden shelves. The products are shot from a slightly elevated angle to showcase their quality and texture, with soft natural light highlighting the vibrant colors of the items against a background of forest green elements. This image aims to represent the customer experience by inviting viewers to explore the offerings while maintaining brand consistency.",
                    "aspect": "1:1",
                }
            ],
            "negative_prompt": "text, watermark, logo, trademark, blurry",
        }
