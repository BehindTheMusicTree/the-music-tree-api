
from django.test import TestCase, RequestFactory
from django.http import HttpResponse
import json
from typing import cast, Dict, Any
from bodzify_api.middleware.DuplicateFieldsMiddleware import DuplicateFieldsMiddleware
from rest_framework.exceptions import ValidationError


class DuplicateFieldsMiddlewareTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = DuplicateFieldsMiddleware(lambda req: HttpResponse())

    def test_duplicate_fields_detection(self):
        # Create a request with duplicate fields in JSON
        json_data = '{"name": "a", "name": "b"}'
        request = self.factory.put(
            '/api/v0.1.1/genres/72271809-6325-4efb-a7ce-3ecfeb16940c/',
            data=json_data,
            content_type='application/json'
        )

        # Test that middleware raises ValidationError for duplicate fields
        with self.assertRaises(ValidationError) as context:
            self.middleware(request)

        # Verify the error message
        error_detail = cast(Dict[str, Any], context.exception.detail)
        self.assertIn('duplicate_fields', error_detail)

        duplicate_fields = error_detail.get('duplicate_fields', {})
        self.assertIsInstance(duplicate_fields, dict)
        self.assertEqual(duplicate_fields.get('code'), 'duplicate_fields')
        self.assertIn('name', duplicate_fields.get('fields', []))

    def test_valid_json_passes(self):
        # Create a request with valid JSON (no duplicates)
        json_data = '{"name": "test", "description": "test description"}'
        request = self.factory.put(
            '/api/v0.1.1/genres/72271809-6325-4efb-a7ce-3ecfeb16940c/',
            data=json_data,
            content_type='application/json'
        )

        # Test that middleware allows valid JSON to pass through
        response = self.middleware(request)
        self.assertEqual(response.status_code, 200)

    def test_non_json_request_passes(self):
        # Create a non-JSON request
        request = self.factory.get('/api/v0.1.1/genres/')

        # Test that middleware allows non-JSON requests to pass through
        response = self.middleware(request)
        self.assertEqual(response.status_code, 200)
