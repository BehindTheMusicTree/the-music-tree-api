from typing import Optional

from django.http import HttpResponse
from rest_framework.test import APIClient

from bodzify_api.utils import data_transformer


# This class is only used for getting the correct type hinting when getting responses from the API
class AppApiClient(APIClient):

    def get(self, path, data: Optional[dict] = None, follow=False, **extra) -> HttpResponse:
        data_url_encoded = None
        if data:
            data_url_encoded = data_transformer.replace_none_with_empty_string(**data)
        return super().get(path, data_url_encoded, follow, **extra)

    def post(self, path, data: Optional[dict] = None, format=None, content_type=None, follow=False, **extra
             ) -> HttpResponse:
        data_url_encoded = None
        if data:
            data_url_encoded = data_transformer.replace_none_with_empty_string(**data)
        return super().post(path, data_url_encoded, format, content_type, follow, **extra)

    def put(self, path, data: Optional[dict] = None, format=None, content_type=None, follow=False, **extra
            ) -> HttpResponse:
        data_url_encoded = None
        if data:
            data_url_encoded = data_transformer.replace_none_with_empty_string(**data)
        return super().put(path, data_url_encoded, format, content_type, follow, **extra)

    def delete(self, path, data: Optional[dict] = None, format=None, content_type=None, follow=False, **extra
               ) -> HttpResponse:
        data_url_encoded = None
        if data:
            data_url_encoded = data_transformer.replace_none_with_empty_string(**data)
        return super().delete(path, data_url_encoded, format, content_type, follow, **extra)
