import os
from io import BytesIO
from typing import Any
from urllib.parse import urlparse

import requests
from django.core.files.uploadedfile import UploadedFile, InMemoryUploadedFile
from rest_framework.exceptions import ValidationError
from rest_framework.fields import URLField

from bodzify_api.serializer.field.AppField import AppField
from bodzify_api.serializer.field.AppFileField import AppFileField
from bodzify_api.validator.TrackFileValidator import TrackFileValidator
from bodzify_api.validator.TrackUrlValidator import TrackUrlValidator


class TrackFileField(AppField):
    """
    A unified field that handles both URL and file uploads for tracks.
    When a URL is provided, downloads the file and converts it to an InMemoryUploadedFile.
    Automatically detects input type and processes accordingly.
    """

    def __init__(self, **kwargs):
        self._allow_null = kwargs.get('allow_null', True)
        super().__init__(**kwargs)

        # Initialize URL validation
        self.url_field = URLField(
            validators=[TrackUrlValidator()],
            allow_null=self._allow_null
        )

        # Initialize file validation
        self.file_field = AppFileField(
            validators=[TrackFileValidator()],
            allow_null=self._allow_null
        )

    def bind(self, field_name: str, parent: Any) -> None:
        """
        Called when the field is bound to a serializer.
        Propagate the field name to child fields for proper error reporting.
        """
        super().bind(field_name, parent)
        if self.url_field:
            self.url_field.bind(field_name, parent)
        if self.file_field:
            self.file_field.bind(field_name, parent)

    def _download_file_from_url(self, url: str) -> InMemoryUploadedFile:
        """
        Downloads a file from a URL and returns it as an InMemoryUploadedFile.
        Raises ValidationError if download fails or file is invalid.
        """
        try:
            # Download the file in chunks
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()

            # Get the filename from the URL or Content-Disposition header
            filename = os.path.basename(urlparse(url).path)
            if not filename:
                filename = 'downloaded_track'
            content_disposition = response.headers.get('Content-Disposition')
            if content_disposition and 'filename=' in content_disposition:
                filename = content_disposition.split('filename=')[1].strip('"\'')

            # Ensure filename has an extension
            if not os.path.splitext(filename)[1]:
                content_type = response.headers.get('Content-Type', '')
                if 'mpeg' in content_type:
                    filename += '.mp3'
                elif 'wav' in content_type:
                    filename += '.wav'
                elif 'flac' in content_type:
                    filename += '.flac'
                else:
                    filename += '.mp3'  # default to mp3

            # Create a BytesIO object to store the file content
            content = BytesIO()
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:  # filter out keep-alive chunks
                    content.write(chunk)
            content.seek(0)

            # Create an InMemoryUploadedFile
            return InMemoryUploadedFile(
                file=content,
                field_name=None,
                name=filename,
                content_type=response.headers.get('Content-Type', 'audio/mpeg'),
                size=len(content.getvalue()),
                charset=None,
                content_type_extra={}
            )
        except requests.Timeout:
            raise ValidationError('URL request timed out. Please try again.')
        except requests.RequestException as e:
            raise ValidationError(f'Failed to download file: {str(e)}')
        except Exception as e:
            raise ValidationError(f'Unexpected error while downloading file: {str(e)}')

    def to_internal_value(self, data: Any) -> Any:
        if data in [None, '']:
            if not self._allow_null:
                self.fail('null')
            return None

        # If it's a file upload
        if isinstance(data, UploadedFile):
            return self.file_field.to_internal_value(data)

        # If it's a URL
        if isinstance(data, str):
            # First validate the URL
            validated_url = self.url_field.to_internal_value(data)
            # Then download the file and convert to InMemoryUploadedFile
            downloaded_file = self._download_file_from_url(validated_url)
            # Validate and return the downloaded file
            return self.file_field.to_internal_value(downloaded_file)

        self.fail('invalid', detail='Field must be either a valid audio file or URL.')

    def to_representation(self, value: Any) -> str:
        """
        Convert the native value into a string representation.
        Returns empty string for None values to maintain string type consistency.
        """
        if value is None:
            return ''
        # For URLs, return as is
        if isinstance(value, str):
            return value
        # For files, return the file URL or empty string if no URL
        return value.url if value and hasattr(value, 'url') else ''
