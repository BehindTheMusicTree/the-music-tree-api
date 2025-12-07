import pytest
from unittest.mock import Mock
from django.http import HttpRequest
from rest_framework.exceptions import ParseError
from rest_framework.request import Request

from api.middleware.ContentTypeValidationMiddleware import ContentTypeValidationMiddleware


class TestContentTypeValidationMiddleware:

    def test_json_array_as_root_then_400_parse_error(self):
        """Test that JSON arrays as root are rejected."""
        middleware = ContentTypeValidationMiddleware(get_response=Mock())

        request = HttpRequest()
        request.method = 'POST'
        request.content_type = 'application/json'
        request._body = b'["Muse", ""]'  # Use _body to set the body
        request.META = {}

        response = middleware.__call__(request)

        assert response.status_code == 400
        import json
        response_data = json.loads(response.content)
        assert 'details' in response_data
        assert 'message' in response_data['details']
        assert 'array' in response_data['details']['message'].lower(
        ) or 'object' in response_data['details']['message'].lower()

    def test_json_object_as_root_then_passes(self):
        """Test that JSON objects as root are accepted."""
        middleware = ContentTypeValidationMiddleware(get_response=Mock())

        mock_response = Mock()
        mock_response.status_code = 200

        def mock_get_response(req):
            return mock_response

        middleware.get_response = mock_get_response

        request = HttpRequest()
        request.method = 'POST'
        request.content_type = 'application/json'
        request._body = b'{"artistsNames": ["Muse"]}'
        request.META = {}

        response = middleware.__call__(request)

        # Should pass through to next middleware/view
        assert response == mock_response

    def test_empty_json_body_then_passes(self):
        """Test that empty JSON body is accepted."""
        middleware = ContentTypeValidationMiddleware(get_response=Mock())

        mock_response = Mock()
        mock_response.status_code = 200

        def mock_get_response(req):
            return mock_response

        middleware.get_response = mock_get_response

        request = HttpRequest()
        request.method = 'POST'
        request.content_type = 'application/json'
        request._body = b''
        request.META = {}

        response = middleware.__call__(request)

        # Should pass through
        assert response == mock_response

    def test_json_string_double_encoded_then_400_parse_error(self):
        """Test that double-encoded JSON strings are rejected."""
        middleware = ContentTypeValidationMiddleware(get_response=Mock())

        request = HttpRequest()
        request.method = 'POST'
        request.content_type = 'application/json'
        request._body = b'"{"key": "value"}"'  # Double-encoded
        request.META = {}

        response = middleware.__call__(request)

        assert response.status_code == 400
        import json
        response_data = json.loads(response.content)
        assert 'details' in response_data
        assert 'double-encoded' in response_data['details']['message'].lower()
