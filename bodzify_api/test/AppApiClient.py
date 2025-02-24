import json
from typing import Optional

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

    def get(self, path, data: Optional[] = None, content_type=None, follow=False, **extra) -> HttpResponse:
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

    def post(self, path, data: Optional[] = None, content_type=None, follow=False, format=None, **extra
             ) -> HttpResponse:
        data_url_encoded = None
        if data:
            data_url_encoded = data_transformer.replace_none_with_empty_string(**data)
            if format != 'multipart':
                data_url_encoded = json.dumps(data_url_encoded, cls=UUIDJSONEncoder)
                if not content_type:
                    content_type = 'application/json'

        # Set default headers for JSON content type
        if content_type == 'application/json' and 'HTTP_ACCEPT' not in extra:
            extra['HTTP_ACCEPT'] = 'application/json'

        # Extract response handler from extra if present
        handle_response = extra.pop('handle_response', None)
        response = super().post(path, data_url_encoded, content_type=content_type, follow=follow, format=format, **extra)
        return self._handle_response(response, handle_response)

    def put(self, path, data: Optional[] = None, format=None, content_type=None, follow=False, **extra
            ) -> HttpResponse:
        data_url_encoded = None
        if data:
            data_url_encoded = data_transformer.replace_none_with_empty_string(**data)
            if format != 'multipart':
                data_url_encoded = json.dumps(data_url_encoded, cls=UUIDJSONEncoder)
                if not content_type:
                    content_type = 'application/json'

        # Set default headers for JSON content type
        if content_type == 'application/json' and 'HTTP_ACCEPT' not in extra:
            extra['HTTP_ACCEPT'] = 'application/json'

        # Extract response handler from extra if present
        handle_response = extra.pop('handle_response', None)
        response = super().put(path, data_url_encoded, format, content_type, follow, **extra)
        return self._handle_response(response, handle_response)

    def delete(self, path, data: Optional[] = None, format=None, content_type=None, follow=False, **extra
               ) -> HttpResponse:
        data_url_encoded = None
        if data:
            data_url_encoded = data_transformer.replace_none_with_empty_string(**data)
            if format != 'multipart':
                data_url_encoded = json.dumps(data_url_encoded, cls=UUIDJSONEncoder)
                if not content_type:
                    content_type = 'application/json'

        # Set default headers for JSON content type
        if content_type == 'application/json' and 'HTTP_ACCEPT' not in extra:
            extra['HTTP_ACCEPT'] = 'application/json'

        # Extract response handler from extra if present
        handle_response = extra.pop('handle_response', None)
        response = super().delete(path, data_url_encoded, format, content_type, follow, **extra)
        return self._handle_response(response, handle_response)
