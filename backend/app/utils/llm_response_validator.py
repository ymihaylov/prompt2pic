import logging
from typing import Dict, Any

from pydantic import ValidationError

from app.models.dto.llm_image_response import LLMImageResponse

logger = logging.getLogger(__name__)


class LLMResponseValidationError(Exception):
    pass


class LLMResponseValidator:

    def validate_image_response(self, raw_response: Dict[str, Any]) -> LLMImageResponse:
        try:
            validated_response = LLMImageResponse(**raw_response)
            return validated_response

        except ValidationError as e:
            error_details = self._format_validation_errors(e)
            raise LLMResponseValidationError(f"Invalid LLM response: {error_details}")

    def _format_validation_errors(self, validation_error: ValidationError) -> str:
        errors = []
        for error in validation_error.errors():
            field = " -> ".join(str(loc) for loc in error["loc"])
            message = error["msg"]
            errors.append(f"{field}: {message}")

        return "; ".join(errors)

    def is_valid_response(self, raw_response: Dict[str, Any]) -> bool:
        try:
            LLMImageResponse(**raw_response)
            return True
        except ValidationError:
            return False
