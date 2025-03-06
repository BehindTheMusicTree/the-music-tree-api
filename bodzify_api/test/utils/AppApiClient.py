import json

from django.http import HttpResponse
from rest_framework.test import APIClient

from bodzify_api.utils import data_transformer
from bodzify_api.utils.json_utils import UUIDJSONEncoder


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

    def get(self, path, data: dict | None = None, content_type=None, follow=False, **extra) -> HttpResponse:
        data_url_encoded = None
        if data:
            data_url_encoded = data_transformer.replace_none_with_empty_string(**data)

        # Set default content type and headers for JSON
        if not content_type:
            content_type = 'application/json'
        if content_type == 'application/json' and 'HTTP_ACCEPT' not in extra:
            extra['HTTP_ACCEPT'] = 'application/json'

        # Extract response handler from extra if present
        handle_response = extra.pop('handle_response', None)
        response = super().get(path, data_url_encoded, follow, **extra)
        return self._handle_response(response, handle_response)

    def post(self, path,
             data: dict | str | None = None,
             follow=False,
             format='json',
             **extra) -> HttpResponse:

        if data and not isinstance(data, str):
            data = data_transformer.replace_none_with_empty_string(**data)
        data_url_encoded = None
        if data:
            if isinstance(data, str):
                data_url_encoded = data
            else:
                data_url_encoded = data_transformer.replace_none_with_empty_string(**data)

                if format != 'multipart':
                    if isinstance(data_url_encoded, dict):
                        data_url_encoded = json.dumps(data_url_encoded, cls=UUIDJSONEncoder)

        if format == 'json':
            content_type = 'application/json'
        elif format != 'multipart':  # Don't set content_type for multipart
            content_type = 'application/x-www-form-urlencoded'
        else:
            content_type = None  # Let DRF handle multipart content type

        if 'HTTP_ACCEPT' not in extra:
            extra['HTTP_ACCEPT'] = 'application/json'

        # Extract response handler from extra if present
        handle_response = extra.pop('handle_response', None)
        response = super().post(
            path, data_url_encoded, follow=follow, format=format, content_type=content_type, **extra)
        return self._handle_response(response, handle_response)

    def put(
            self, path, data: dict | str | None = None, format=None, content_type=None, follow=False, **extra
    ) -> HttpResponse:
        data_url_encoded = None
        if data:
            if isinstance(data, str):
                data_url_encoded = data
            else:
                data_url_encoded = data_transformer.replace_none_with_empty_string(**data)
                if format != 'multipart':
                    data_url_encoded = json.dumps(data_url_encoded, cls=UUIDJSONEncoder)

        if format == 'json':
            content_type = 'application/json'
        elif format != 'multipart':  # Don't set content_type for multipart
            content_type = 'application/x-www-form-urlencoded'
        else:
            content_type = None  # Let DRF handle multipart content type

        # Set default headers for JSON content type
        if 'HTTP_ACCEPT' not in extra:
            extra['HTTP_ACCEPT'] = 'application/json'

        # Extract response handler from extra if present
        handle_response = extra.pop('handle_response', None)
        response = super().put(path, data_url_encoded, format, content_type, follow, **extra)
        return self._handle_response(response, handle_response)

    def delete(self, path, data: dict | None = None, format=None, content_type=None, follow=False, **extra
               ) -> HttpResponse:
        data_url_encoded = None
        if data:
            data_url_encoded = data_transformer.replace_none_with_empty_string(**data)
            if format != 'multipart':
                data_url_encoded = json.dumps(data_url_encoded, cls=UUIDJSONEncoder)

        if format == 'json':
            content_type = 'application/json'
        elif format != 'multipart':  # Don't set content_type for multipart
            content_type = 'application/x-www-form-urlencoded'
        else:
            content_type = None  # Let DRF handle multipart content type

        # Set default headers for JSON content type
        if 'HTTP_ACCEPT' not in extra:
            extra['HTTP_ACCEPT'] = 'application/json'

        # Extract response handler from extra if present
        handle_response = extra.pop('handle_response', None)
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
                        if hasattr(response.content, 'decode') else str(response.content), 'content_type': content_type,
                        'status_code': response.status_code}
            else:
                # For success responses, maintain strict JSON checking
                if not content_type.startswith('application/json'):
                    raise ValueError(
                        f'Content-Type header is "{content_type}", not "application/json"'
                    )
                response._json = json.loads(response.content)

        return response._json
