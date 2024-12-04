from typing import Dict, Any, Callable
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.serializers import Serializer
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError as DrfValidationError
from bodzify_api.view.error.ErrorResponse import ErrorResponse


class RequestHandler:
    def validate_request_data(
            self, request_data: Dict[str, Any],
            serializer_class: type[Serializer],
            request: Request) -> None:
        serializer = serializer_class(data=request_data, context={'request': request})
        serializer.is_valid(raise_exception=True)

    def handle_validated_request(
            self, request_data: Dict[str, Any],
            operation: Callable[[], Response],
            serializer_class: type[Serializer],
            request: Request) -> Response:
        try:
            self.validate_request_data(request_data, serializer_class, request)
            return operation()
        except (IntegrityError, DrfValidationError) as exception:
            return ErrorResponse.from_validation_error(exception)
