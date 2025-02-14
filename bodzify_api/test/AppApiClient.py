import json
from typing import Optional

from django.http import HttpResponse
from rest_framework.test import APIClient

from bodzify_api.utils import data_transformer
from bodzify_api.utils.json_utils import UUIDJSONEncoder


class AppApiClient(APIClient):

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

        return super().post(path, data_url_encoded, content_type=content_type, follow=follow, format=format, **extra)

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

        return super().put(path, data_url_encoded, format, content_type, follow, **extra)

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
