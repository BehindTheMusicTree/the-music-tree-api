import json
from typing import cast


from rest_framework import status
from django.http import HttpRequest, HttpResponse
from django.test import RequestFactory, TestCase

from bodzify_api import settings
from bodzify_api.middleware.ContentTypeValidationMiddleware import ContentTypeValidationMiddleware


class ContentTypeValidationMiddlewareTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        def get_response(request: HttpRequest) -> HttpResponse:
            return HttpResponse(status=200)
        self.middleware = ContentTypeValidationMiddleware(get_response)

    def test_double_encoded_json_then_error(self):
        # Create a double-encoded JSON string
        data = {"file": "https://example.com/file.mp3"}
        double_encoded = json.dumps(json.dumps(data))  # Encode twice to simulate the issue

        request = self.factory.post(
            f'/api/{settings.APP_VERSION}/tracks/', data=double_encoded, content_type='application/json')
        response = self.middleware(request)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_regular_json_then_ok(self):
        data = {"file": "https://example.com/file.mp3"}
        request = self.factory.post(
            f'/api/{settings.APP_VERSION} /tracks/', data=json.dumps(data), content_type='application/json')

        response = cast(HttpResponse, self.middleware(request))
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_missing_content_type_then_error(self):
        data = {"file": "https://example.com/file.mp3"}
        request = self.factory.post(f'/api/{settings.APP_VERSION}/tracks/', data=json.dumps(data), content_type='')
        response = self.middleware(request)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_non_json_request_then_ok(self):
        request = self.factory.get(f'/api/{settings.APP_VERSION}/tracks/')
        response = cast(HttpResponse, self.middleware(request))
        self.assertEqual(status.HTTP_200_OK, response.status_code)
