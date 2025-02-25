import os

from django.http import FileResponse

from bodzify_api.view.error.ApiErrorCode import ApiErrorCode
from bodzify_api.view.error.ErrorResponseFields import ErrorResponseFields
from bodzify_api.view.file_response.FileResponseHeaders import \
    FileResponseHeaders


class AppFileResponse:
    @staticmethod
    def from_file(file_path: str, filename: str) -> FileResponse:
        if not os.path.exists(file_path):
            raise FileNotFoundError(ErrorResponseFields.MESSAGES[ApiErrorCode.RESOURCE_FILE_NOT_FOUND])

        file_handle = open(file_path, "rb")
        response = FileResponse(file_handle, content_type=FileResponseHeaders.CONTENT_TYPE)
        response[FileResponseHeaders.CONTENT_LENGTH] = os.path.getsize(file_path)
        response[FileResponseHeaders.CONTENT_DISPOSITION] = (
            FileResponseHeaders.CONTENT_DISPOSITION_VALUE % filename
        )
        return response
