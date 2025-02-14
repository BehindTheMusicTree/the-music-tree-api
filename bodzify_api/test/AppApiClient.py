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

    def _handle_response(self, response: HttpResponse, on_success=None, on_bad_request=None) -> HttpResponse:
        """Handle API response by setting appropriate results based on status code.

        Args:
            response: The API response to handle
            on_success: Optional callback to execute after setting result on successful response
            on_bad_request: Optional callback to execute after setting result on bad request
        """
        if hasattr(self.test_case, '_set_result') and hasattr(self.test_case, '_set_bad_request_result'):
            if response.status_code in [200, 201]:
                self.test_case._set_result(response)
                if on_success:
                    on_success(response)
            elif response.status_code == 400:
                self.test_case._set_bad_request_result(response)
                if on_bad_request:
                    on_bad_request(response)
        return response

    def get(self, path, data: Optional[dict] = None, content_type=None, follow=False, **extra) -> HttpResponse:
        data_url_encoded = None
        if data:
            data_url_encoded = data_transformer.replace_none_with_empty_string(**data)

        # Set default content type and headers for JSON
        if not content_type:
            content_type = 'application/json'
        if content_type == 'application/json' and 'HTTP_ACCEPT' not in extra:
            extra['HTTP_ACCEPT'] = 'application/json'

        return super().get(path, data_url_encoded, follow, **extra)

    def post(self, path, data: Optional[dict] = None, content_type=None, follow=False, format=None, **extra
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

        # Extract callbacks from extra if present
        on_success = extra.pop('on_success', None)
        on_bad_request = extra.pop('on_bad_request', None)
        response = super().post(path, data_url_encoded, content_type=content_type, follow=follow, format=format, **extra)
        return self._handle_response(response, on_success, on_bad_request)

    def put(self, path, data: Optional[dict] = None, format=None, content_type=None, follow=False, **extra
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

        # Extract callbacks from extra if present
        on_success = extra.pop('on_success', None)
        on_bad_request = extra.pop('on_bad_request', None)
        response = super().put(path, data_url_encoded, format, content_type, follow, **extra)
        return self._handle_response(response, on_success, on_bad_request)

    def delete(self, path, data: Optional[dict] = None, format=None, content_type=None, follow=False, **extra
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

        return super().delete(path, data_url_encoded, format, content_type, follow, **extra)
