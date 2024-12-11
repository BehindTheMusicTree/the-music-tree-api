from typing import Dict, Any, Union
from rest_framework.exceptions import ErrorDetail as DRFErrorDetail
from rest_framework.exceptions import ValidationError as DrfValidationError
from django.core.exceptions import ValidationError as DjangoValidationError
import logging

from bodzify_api import settings
from bodzify_api.view.error.ErrorMessages import AppErrorMessages
from bodzify_api.view.error.ErrorCode import ErrorCode


class ErrorProcessor:
    """Process and format validation errors from different sources."""

    @staticmethod
    def format_error_message(message: Union[str, DRFErrorDetail]) -> str:
        """Format error messages, handling special cases like UUID validation."""
        message_str = str(message)
        return AppErrorMessages.MESSAGES[ErrorCode.VALIDATION_INVALID_UUID] if 'UUID' in message_str else message_str

    def process_validation_errors(self, exc: Union[DrfValidationError, DjangoValidationError]) -> Dict[str, Any]:
        """
        Process validation errors from DRF or Django into a consistent format.
        
        Args:
            exc: The validation error to process.
        
        Returns:
            A dictionary containing formatted error messages.
        """
        custom_errors: Dict[str, Any] = {}

        if isinstance(exc, DrfValidationError):
            detail = getattr(exc, 'detail', None)
            if isinstance(detail, dict):
                custom_errors = {
                    field: [self.format_error_message(msg) for msg in messages]
                    if isinstance(messages, (list, tuple))
                    else self.format_error_message(messages)
                    for field, messages in detail.items()
                }
            elif detail:
                custom_errors['non_field_errors'] = (
                    [self.format_error_message(msg) for msg in detail]
                    if isinstance(detail, (list, tuple))
                    else self.format_error_message(detail)
                )
        elif isinstance(exc, DjangoValidationError):
            message_dict = getattr(exc, 'message_dict', None)
            if message_dict:
                custom_errors = {
                    field: [self.format_error_message(msg) for msg in messages]
                    for field, messages in message_dict.items()
                }
            else:
                custom_errors['non_field_errors'] = [
                    self.format_error_message(msg) for msg in exc.messages
                ]
        else:
            logging.getLogger(settings.LOGGERS_NAME.EXCEPTIONS).warning("Unhandled exception type: %s", type(exc))

        return custom_errors
