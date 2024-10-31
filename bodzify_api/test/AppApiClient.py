
from django.http import HttpResponse
from rest_framework.test import APIClient


# This class is only used for getting the correct type hinting when getting responses from the API
class AppApiClient(APIClient):

    def get(self, path, data=None, follow=False, **extra) -> HttpResponse:
        return super().get(path, data, follow, **extra)  # type: ignore

    def post(self, path, data=None, format=None, content_type=None, follow=False, **extra) -> HttpResponse:
        return super().post(path, data, format, content_type, follow, **extra)  # type: ignore

    def put(self, path, data=None, format=None, content_type=None, follow=False, **extra) -> HttpResponse:
        return super().put(path, data, format, content_type, follow, **extra)  # type: ignore

    def delete(self, path, data=None, format=None, content_type=None, follow=False, **extra) -> HttpResponse:
        return super().delete(path, data, format, content_type, follow, **extra)  # type: ignore
