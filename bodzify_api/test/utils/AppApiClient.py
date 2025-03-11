import json
from typing import Any

from django.http import HttpResponse
from rest_framework.test import APIClient

from bodzify_api.utils import data_transformer
from bodzify_api.utils.json_utils import transform_uuids


class AppApiClient(APIClient):
    def __init__(self, test_case=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.test_case = test_case

    def _handle_response(self, response: HttpResponse, handle_response=None) -> HttpResponse:
        """Handle API response using a unified response handler.

        Args:
            response: The API response to handle
            handle_response: Optional callback to handle the response regardless of status code
        """
        if handle_response:
            handle_response(response)
        return response

    def _get_content_type(self, format: str | None, content_type: str | None) -> str | None:
        """Determine the appropriate content type based on format and explicit content_type.

        Args:
            format: The format of the request ('json', 'multipart', etc.)
            content_type: Explicitly specified content type

        Returns:
            The determined content type or None for multipart
        """
        if format in ['multipart', 'json']:
            return None
        return content_type

    def _prepare_data(self, data: dict | str | None, format: str | None) -> Any:
        """Prepare data for the request based on format and type.

        Args:
            data: The input data to prepare
            format: The format of the request ('json', 'multipart', etc.)

        Returns:
            Prepared data ready for the request
        """
        if not data:
            # Initialize empty data for json/multipart to ensure proper content type
            return {} if format in ['json', 'multipart'] else None

        if isinstance(data, str):
            return data

        prepared_data = data_transformer.replace_none_with_empty_string(**data)
        if format == 'json' and isinstance(prepared_data, dict):
            return transform_uuids(prepared_data)  # Only convert UUIDs to strings, let client handle JSON encoding

        # For multipart, ensure empty arrays are preserved by sending an empty string
        if format == 'multipart' and isinstance(prepared_data, dict):
            result = {}
            for key, value in prepared_data.items():
                if isinstance(value, list):
                    if len(value) == 0:
                        # Send empty string for empty arrays to ensure field is preserved
                        result[key] = ['']
                    else:
                        result[key] = value
                else:
                    result[key] = value
            return result

        return prepared_data

    def _prepare_request_kwargs(
            self, extra: dict, format: str | None, content_type: str | None) -> tuple[dict, Any, str | None]:
        """Prepare common request keyword arguments.

        Args:
            extra: Additional request arguments
            format: The format of the request
            content_type: The content type for the request
            data: The request data to be sent. If None and format is 'json' or 'multipart',
                 it will be initialized to {} to ensure proper content type headers are set.
                 This is important because leaving data as None won't set the correct
                 content type headers for the request.

        Returns:
            Tuple of (prepared extra kwargs, response handler, determined content type, initialized data)
        """
        extra = extra.copy()
        content_type = self._get_content_type(format, content_type)
        extra['HTTP_ACCEPT'] = 'application/json'
        handle_response = extra.pop('handle_response', None)

        return extra, handle_response, content_type

    def get(self, path, data: dict | None = None, content_type=None, follow=False, **extra) -> HttpResponse:
        if data:
            # For GET requests, ensure data is a valid query string format
            data_url_encoded = data_transformer.replace_none_with_empty_string(**data)
        else:
            data_url_encoded = None

        extra, handle_response, content_type = self._prepare_request_kwargs(extra, 'json', content_type)
        response = super().get(path, data_url_encoded, follow, **extra)
        return self._handle_response(response, handle_response)

    def post(self, path, data: dict | str | None = None, format='json', content_type=None, follow=False, **extra) -> HttpResponse:
        data_url_encoded = self._prepare_data(data, format)
        extra, handle_response, content_type = self._prepare_request_kwargs(extra, format, content_type)
        response = super().post(path, data_url_encoded, follow=follow,
                                format=format, content_type=content_type, **extra)
        return self._handle_response(response, handle_response)

    def put(self, path, data: dict | str | None = None, format='json', content_type=None, follow=False, **extra) -> HttpResponse:
        data_url_encoded = self._prepare_data(data, format)
        extra, handle_response, content_type = self._prepare_request_kwargs(extra, format, content_type)

        response = super().put(path, data_url_encoded, format, content_type, follow, **extra)
        return self._handle_response(response, handle_response)

    def delete(self, path, data: dict | None = None, format=None, content_type=None, follow=False, **extra) -> HttpResponse:
        data_url_encoded = self._prepare_data(data, format)
        extra, handle_response, content_type = self._prepare_request_kwargs(extra, format, content_type)

        response = super().delete(path, data_url_encoded, format, content_type, follow, **extra)
        return self._handle_response(response, handle_response)

    def _parse_json(self, response, **extra):
        """Parse JSON from response while handling non-JSON responses gracefully.

        For error responses (4xx, 5xx), we don't require JSON content-type as they
        might return HTML error pages.
        """
        if not hasattr(response, '_json'):
            content_type = response.get('Content-Type', '')

            # For error responses, don't enforce JSON content-type
            if response.status_code >= 400:
                try:
                    response._json = json.loads(response.content)
                except (ValueError, json.JSONDecodeError):
                    # For non-JSON error responses, create a basic error structure
                    response._json = {
                        'detail': response.content.decode('utf-8')
                        if hasattr(response.content, 'decode') else str(response.content),
                        'content_type': content_type,
                        'status_code': response.status_code
                    }
            else:
                # For success responses, maintain strict JSON checking
                if not content_type.startswith('application/json'):
                    raise ValueError(
                        f'Content-Type header is "{content_type}", not "application/json"'
                    )
                response._json = json.loads(response.content)

        return response._json
