import pytest
from unittest.mock import Mock, MagicMock
from django.http import HttpRequest, QueryDict
from rest_framework.exceptions import ParseError
from rest_framework.request import Request

from bodzify_api.middleware.content_validity.middleware import ContentValidityMiddleware


class TestContentValidityMiddleware:

    def test_json_request_data_access_exception_then_400_parse_error(self):
        """Test that if accessing request.data raises an exception, the request is rejected."""
        middleware = ContentValidityMiddleware(get_response=Mock())

        request = MagicMock(spec=Request)
        request.method = 'POST'
        request.content_type = 'application/json'
        # Simulate request.data raising an exception when accessed

        def raise_exception():
            raise Exception("Corrupted data")
        type(request).data = property(lambda self: raise_exception())  # type: ignore

        response = middleware.__call__(request)

        assert response.status_code == 400
        import json
        response_data = json.loads(response.content)
        assert 'details' in response_data
        assert 'message' in response_data['details']
        assert 'parse' in response_data['details']['message'].lower(
        ) or 'malformed' in response_data['details']['message'].lower()

    def test_json_request_data_accessible_then_passes(self):
        """Test that if request.data is accessible, the request passes through."""
        mock_response = Mock()
        mock_response.status_code = 200

        def mock_get_response(req):
            return mock_response

        middleware = ContentValidityMiddleware(get_response=mock_get_response)

        request = MagicMock(spec=Request)
        request.method = 'POST'
        request.content_type = 'application/json'
        request.data = {'artistsNames': ['Muse']}  # Accessible data

        response = middleware.__call__(request)

        # Should pass through to next middleware/view
        assert response == mock_response

    def test_multipart_post_post_access_exception_then_400_parse_error(self):
        """Test that if accessing request.POST raises an exception, the request is rejected."""
        middleware = ContentValidityMiddleware(get_response=Mock())

        request = MagicMock(spec=Request)
        request.method = 'POST'
        request.content_type = 'multipart/form-data'
        request._request = MagicMock()
        # Simulate request._request.POST raising an exception when accessed

        def raise_exception():
            raise Exception("Corrupted POST data")
        type(request._request).POST = property(lambda self: raise_exception())  # type: ignore

        response = middleware.__call__(request)

        assert response.status_code == 400
        import json
        response_data = json.loads(response.content)
        assert 'details' in response_data
        assert 'parse' in response_data['details']['message'].lower(
        ) or 'malformed' in response_data['details']['message'].lower()

    def test_multipart_post_post_accessible_then_passes(self):
        """Test that if request.POST is accessible, the request passes through."""
        mock_response = Mock()
        mock_response.status_code = 200

        def mock_get_response(req):
            return mock_response

        middleware = ContentValidityMiddleware(get_response=mock_get_response)

        request = MagicMock(spec=Request)
        request.method = 'POST'
        request.content_type = 'multipart/form-data'
        request._request = MagicMock()
        request._request.POST = QueryDict()  # Accessible POST data

        response = middleware.__call__(request)

        # Should pass through
        assert response == mock_response

    def test_multipart_put_parse_exception_then_400_parse_error(self):
        """Test that if parsing multipart data for PUT raises an exception, the request is rejected."""
        middleware = ContentValidityMiddleware(get_response=Mock())
        
        request = MagicMock(spec=Request)
        request.method = 'PUT'
        request.content_type = 'multipart/form-data'
        request.META = {'CONTENT_TYPE': 'multipart/form-data; boundary=invalid'}
        # Simulate body access raising an exception
        def raise_exception():
            raise Exception("Corrupted data")
        type(request).body = property(lambda self: raise_exception())  # type: ignore

        response = middleware.__call__(request)

        assert response.status_code == 400
        import json
        response_data = json.loads(response.content)
        assert 'details' in response_data
        assert 'parse' in response_data['details']['message'].lower() or 'malformed' in response_data['details']['message'].lower()

    def test_multipart_put_data_accessible_then_passes(self):
        """Test that if multipart data can be parsed for PUT, the request passes through."""
        mock_response = Mock()
        mock_response.status_code = 200
        
        def mock_get_response(req):
            return mock_response
        
        middleware = ContentValidityMiddleware(get_response=mock_get_response)
        
        request = MagicMock(spec=Request)
        request.method = 'PUT'
        request.content_type = 'multipart/form-data'
        request.META = {'CONTENT_TYPE': 'multipart/form-data; boundary=----WebKitFormBoundary'}
        request.body = b'------WebKitFormBoundary\r\nContent-Disposition: form-data; name="test"\r\n\r\nvalue\r\n------WebKitFormBoundary--\r\n'
        request._body = request.body
        
        response = middleware.__call__(request)
        
        # Should pass through
        assert response == mock_response

    def test_get_request_then_passes(self):
        """Test that GET requests pass through without validation."""
        mock_response = Mock()
        mock_response.status_code = 200

        def mock_get_response(req):
            return mock_response

        middleware = ContentValidityMiddleware(get_response=mock_get_response)

        request = HttpRequest()
        request.method = 'GET'
        request.content_type = ''

        response = middleware.__call__(request)

        # Should pass through
        assert response == mock_response
