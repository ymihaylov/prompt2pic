"""
Image generation service using OpenAI DALL-E.
"""

from openai import OpenAI


class ImageGenerationService:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    def generate(
        self, prompt: str, aspect_ratio: str = "1:1", model: str = "dall-e-3"
    ) -> dict:
        try:
            # Map aspect ratios to DALL-E sizes
            size_map = {"1:1": "1024x1024", "16:9": "1792x1024", "3:4": "1024x1792"}

            size = size_map.get(aspect_ratio, "1024x1024")
            # quality="standard"
            response = self.client.images.generate(
                model=model, prompt=prompt, size=size, n=1
            )

            return {
                "url": response.data[0].url,
                "prompt": prompt,
                "aspect_ratio": aspect_ratio,
                "size": size,
                "model": model,
            }

        except Exception as e:
            raise RuntimeError(f"Image generation failed: {e}")


# ImagesResponse(
#     created=1755499647,
#     background=None,
#     data=[
#         Image(
#             b64_json=None,
#             revised_prompt="...",
#             url="https://oaidalleapiprodscus.blob.core.windows.net/private/org-VoATYqH6vJCmrxisNmZlo0Zt/user-NnpixfVul4LLc3gprILjVfAT/img-tp13ExHP6UfuZsgXc6CmevU1.png?st=2025-08-18T05%3A47%3A27Z&se=2025-08-18T07%3A47%3A27Z&sp=r&sv=2024-08-04&sr=b&rscd=inline&rsct=image/png&skoid=c6569cb0-0faa-463d-9694-97df3dc1dfb1&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2025-08-17T16%3A12%3A14Z&ske=2025-08-18T16%3A12%3A14Z&sks=b&skv=2024-08-04&sig=YPVPWH%2Bgm%2B%2BF7jmDE/5D92iSDyTcgL%2BXR7rgDJc9DQw%3D",
#         )
#     ],
#     output_format=None,
#     quality=None,
#     size=None,
#     usage=None,
# )
