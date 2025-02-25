from typing import Any, Callable, dict

from django.db import IntegrityError
from rest_framework.exceptions import ValidationError as DrfValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from bodzify_api.view.error.ErrorResponse import ErrorResponse


class RequestHandler:
    def validate_request_data(self, request_data: dict[str, Any], serializer_class: type[Serializer], request: Request
                              ) -> None:
        serializer = serializer_class(data=request_data, context={'request': request})
        serializer.is_valid(raise_exception=True)

    def handle_validated_request(self,
                                 request_data: dict[str, Any],
                                 operation: Callable[[], Response],
                                 serializer_class: type[Serializer],
                                 request: Request) -> Response:
        try:
            self.validate_request_data(request_data, serializer_class, request)
            return operation()
        except DrfValidationError as exception:
            return ErrorResponse.from_validation_error(exception)
        except IntegrityError as exception:
            # Let system-level integrity errors propagate
            # Validation-related integrity errors should be caught and handled at the model level
            # (see Criteria.save() for an example)
            return ErrorResponse.from_unhandled_integrity_error(exception)
