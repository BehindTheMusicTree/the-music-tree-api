"""
Examples of malformed requests that bypass middleware validation.

These are edge cases where the middleware might not catch validation errors,
requiring field-level validation as a fallback.
"""
import pytest
from unittest.mock import Mock, MagicMock
from django.http import HttpRequest, QueryDict
from rest_framework.request import Request

from bodzify_api.middleware.list_value_validation.middleware import ListValueValidationMiddleware


class TestMalformedRequestsBypassMiddleware:
    """
    Examples of malformed requests that bypass middleware validation.
    
    These demonstrate why field-level validation is needed as a fallback.
    """
    
    def test_json_request_with_list_as_root_then_bypasses_middleware(self):
        """
        Example 1: JSON request with list as root (not a dict)
        
        If someone sends a JSON array as the root (e.g., ["Muse", ""]),
        CamelToSnakeMiddleware will set request.data to a list, not a dict.
        The middleware checks `isinstance(data, dict)` and skips validation.
        
        Request:
            POST /api/endpoint
            Content-Type: application/json
            Body: ["Muse", ""]
        
        Middleware behavior:
            - Line 51: `if isinstance(data, dict):` → False (data is a list)
            - Validation skipped
        """
        middleware = ListValueValidationMiddleware(get_response=Mock())
        
        # Simulate request.data being a list (not a dict)
        request = MagicMock(spec=Request)
        request.method = 'POST'
        request.content_type = 'application/json'
        request.data = ["Muse", ""]  # List, not dict!
        
        # Middleware skips validation because data is not a dict
        response = middleware.__call__(request)
        
        # Should not raise - validation was skipped
        assert response is not None
    
    def test_json_request_with_nested_structure_then_bypasses_middleware(self):
        """
        Example 2: JSON request with nested structure that middleware doesn't check
        
        If the data is nested in an unexpected way, the middleware only checks
        top-level keys. Nested list fields might not be caught.
        
        Request:
            POST /api/endpoint
            Content-Type: application/json
            Body: {"wrapper": {"artistsNames": ["Muse", ""]}}
        
        Middleware behavior:
            - Checks top-level keys: ["wrapper"]
            - Doesn't recursively check nested structures
            - Validation skipped for nested list
        """
        middleware = ListValueValidationMiddleware(get_response=Mock())
        
        request = MagicMock(spec=Request)
        request.method = 'POST'
        request.content_type = 'application/json'
        request.data = {"wrapper": {"artistsNames": ["Muse", ""]}}
        
        # Middleware only checks top-level, not nested
        response = middleware.__call__(request)
        
        # Should not raise - nested validation was skipped
        assert response is not None
    
    def test_multipart_put_with_parsing_failure_then_bypasses_middleware(self):
        """
        Example 3: PUT/PATCH multipart request with parsing failure
        
        If manual multipart parsing fails (e.g., malformed boundary, corrupted data),
        the middleware catches the exception and continues without validation.
        
        Request:
            PUT /api/endpoint
            Content-Type: multipart/form-data (with malformed boundary)
            Body: [corrupted multipart data]
        
        Middleware behavior:
            - Line 94-95: Parsing exception caught, logged, continues
            - data_to_check remains None
            - Line 98: `if data_to_check:` → False, validation skipped
        """
        middleware = ListValueValidationMiddleware(get_response=Mock())
        
        request = MagicMock(spec=Request)
        request.method = 'PUT'
        request.content_type = 'multipart/form-data'
        request.body = b'corrupted multipart data'
        request.META = {}
        request._body = None
        request._stream = None
        request._read_started = False
        
        # Simulate parsing failure
        def mock_get_response(req):
            return Mock()
        middleware.get_response = mock_get_response
        
        # Middleware will try to parse, fail, and skip validation
        response = middleware.__call__(request)
        
        # Should not raise - parsing failed, validation skipped
        assert response is not None
    
    def test_post_multipart_with_empty_post_then_bypasses_middleware(self):
        """
        Example 4: POST multipart request with empty/malformed request.POST
        
        If request.POST is empty or doesn't have expected structure,
        data_to_check remains None and validation is skipped.
        
        Request:
            POST /api/endpoint
            Content-Type: multipart/form-data
            Body: [empty or malformed]
        
        Middleware behavior:
            - Line 69: `len(post_data) > 0` → False
            - Line 71: `len(request.POST) > 0` → False
            - data_to_check remains None
            - Line 98: `if data_to_check:` → False, validation skipped
        """
        middleware = ListValueValidationMiddleware(get_response=Mock())
        
        request = MagicMock(spec=Request)
        request.method = 'POST'
        request.content_type = 'multipart/form-data'
        request._request = MagicMock()
        request._request.POST = QueryDict()  # Empty!
        request.POST = QueryDict()  # Also empty!
        
        def mock_get_response(req):
            return Mock()
        middleware.get_response = mock_get_response
        
        # Middleware skips validation because POST is empty
        response = middleware.__call__(request)
        
        # Should not raise - validation was skipped
        assert response is not None
    
    def test_content_type_mismatch_then_bypasses_middleware(self):
        """
        Example 5: Content-Type header doesn't match actual body format
        
        If Content-Type says JSON but body is actually multipart (or vice versa),
        the middleware checks the wrong format and skips validation.
        
        Request:
            POST /api/endpoint
            Content-Type: application/json (but body is actually multipart)
            Body: [multipart data]
        
        Middleware behavior:
            - Line 45: `content_type == 'application/json'` → True
            - Tries to access request.data (which might fail or be empty)
            - Doesn't check multipart format
            - Validation skipped
        """
        middleware = ListValueValidationMiddleware(get_response=Mock())
        
        request = MagicMock(spec=Request)
        request.method = 'POST'
        request.content_type = 'application/json'  # Wrong! Body is actually multipart
        request.data = {}  # Empty because parsing failed or wrong format
        
        def mock_get_response(req):
            return Mock()
        middleware.get_response = mock_get_response
        
        # Middleware checks JSON format, but data is empty/wrong
        response = middleware.__call__(request)
        
        # Should not raise - wrong format checked, validation skipped
        assert response is not None

