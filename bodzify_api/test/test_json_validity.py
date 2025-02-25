

from django.http import HttpResponse
from django.test import RequestFactory, TestCase

from bodzify_api.middleware.duplicate_fields.middleware import \
    DuplicateFieldsMiddleware
from bodzify_api.serializer.model.criteria.input.Fields import \
    Fields as CriteriaFields


class DuplicateFieldsMiddlewareTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = DuplicateFieldsMiddleware(lambda req: HttpResponse())

    def test_valid_json_passes(self):
        # Create a request with valid JSON (no duplicates)
        json_data = '{' + CriteriaFields.NAME_PUBLIC + ': "test", "description": "test description"}'
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
