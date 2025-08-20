from app.infrastructure.providers.llm.llm_provider_factory import LLMProviderFactory
from app.models.dto.image_generation_request import ImageGenerationRequest
from app.models.dto.llm_image_response import LLMImageResponse
from app.utils.llm_response_validator import (
    LLMResponseValidationError,
    LLMResponseValidator,
)
from app.utils.prompt_template_service import PromptTemplateService


class LLMProcessingService:
    def __init__(
        self,
        llm_model_factory: LLMProviderFactory,
        prompt_template_service: PromptTemplateService,
        llm_response_validator: LLMResponseValidator,
    ):
        self.llm_factory = llm_model_factory
        self.prompt_service = prompt_template_service
        self.llm_response_validator = llm_response_validator

    def generate_enhanced_prompts(
        self, request: ImageGenerationRequest
    ) -> LLMImageResponse:
        llm_model_provider = self.llm_factory.create(request.llm_model)
        populated_prompt = self.prompt_service.get_populated_prompt(
            template_name="image_generation",
            variables={
                "business_description": request.prompt,
                "gallery_count": request.gallery_count,
            },
        )

        raw_llm_response = llm_model_provider.generate_prompt(populated_prompt)

        try:
            validated_llm_response = (
                self.llm_response_validator.validate_image_response(raw_llm_response)
            )
        except LLMResponseValidationError:
            raise

        return validated_llm_response
