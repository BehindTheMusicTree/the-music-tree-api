from typing import Dict, Union, Any, List
import os

from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import IntegrityError
from django.http import FileResponse
from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework.response import Response
from rest_framework import status


class FileResponseHeaders:
    """Constants for file response headers."""
    CONTENT_TYPE = 'file'
    CONTENT_LENGTH = 'Content-Length'
    CONTENT_DISPOSITION = 'Content-Disposition'
    CONTENT_DISPOSITION_VALUE = 'attachment; filename="%s"'


class APIErrorMessages:
    """Constants for API error messages."""
    INTEGRITY_ERROR = "There is an issue with the object sent"
    INVALID_UUID = "A valid UUID is required."
    SERVICE_NOT_DEFINED = "Service not defined in viewset"
    PAGINATION_NOT_SET = "Pagination not set"
    FILE_NOT_FOUND = "The requested file could not be found"
    SERIALIZER_NOT_DEFINED = {
        'detailed': "detailed_serializer_class not defined in viewset",
        'simple': "simple_serializer_class not defined in viewset",
        'create': "create_serializer_class not defined in viewset",
        'update': "update_serializer_class not defined in viewset"
    }
    INVALID_QUERY_PARAMS = "Invalid query parameters provided"


class APIErrorResponse:
    """Utility class for creating standardized API error responses."""
    
    @staticmethod
    def create_error_response(error_data: Union[Dict[str, Any], str, List[str]]) -> Response:
        """
        Create a standardized error response.
        
        Args:
            error_data: Dictionary of field errors, a string message, or a list of error messages
        """
        if isinstance(error_data, list):
            error_message = {'non_field_errors': error_data}
        elif isinstance(error_data, str):
            error_message = {'error': error_data}
        elif isinstance(error_data, dict):
            error_message = error_data
        else:
            error_message = {'error': str(error_data)}

        return Response(
            data={
                'status': '400',
                'message': 'Bad Request',
                'success': False,
                'errors': error_message
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    @staticmethod
    def from_validation_error(exc: Union[DRFValidationError, DjangoValidationError, IntegrityError]) -> Response:
        """Create an error response from a validation error."""
        if isinstance(exc, IntegrityError):
            return APIErrorResponse.create_error_response(APIErrorMessages.INTEGRITY_ERROR)
        
        if isinstance(exc, DRFValidationError):
            if isinstance(exc.detail, dict):
                error_dict = {
                    field: [str(error) for error in errors]
                    for field, errors in exc.detail.items()
                }
                return APIErrorResponse.create_error_response(error_dict)
            return APIErrorResponse.create_error_response(str(exc.detail))
        
        if isinstance(exc, DjangoValidationError):
            if hasattr(exc, 'message_dict'):
                return APIErrorResponse.create_error_response(exc.message_dict)
            return APIErrorResponse.create_error_response(exc.messages)

        return APIErrorResponse.create_error_response(str(exc))


class APIFileResponse:
    """Utility class for creating file download responses."""
    
    @staticmethod
    def from_file(file_path: str, filename: str) -> FileResponse:
        """
        Create a file response for downloading files.
        
        Args:
            file_path: The full path to the file
            filename: The name to use for the downloaded file
        
        Raises:
            FileNotFoundError: If the file does not exist
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(APIErrorMessages.FILE_NOT_FOUND)

        file_handle = open(file_path, "rb")
        response = FileResponse(file_handle, content_type=FileResponseHeaders.CONTENT_TYPE)
        response[FileResponseHeaders.CONTENT_LENGTH] = os.path.getsize(file_path)
        response[FileResponseHeaders.CONTENT_DISPOSITION] = (
            FileResponseHeaders.CONTENT_DISPOSITION_VALUE % filename
        )
        return response