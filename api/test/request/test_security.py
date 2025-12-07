import logging
from rest_framework import status

from api.test.utils.AppTestCase import AppTestCase
from api.view.error.ApiErrorCode import ApiErrorCodeNumeric


class TestCase(AppTestCase):
    def setUp(self):
        super().setUp()
        self.logger = logging.getLogger('exceptions')

    def test_disallowed_host_then_400_bad_request(self):
        """Test that requests with invalid Host headers return appropriate error response"""
        with self.assertLogs('exceptions', level='ERROR') as log:
            self.api_client.credentials(HTTP_HOST='malicious.example.com')
            response = self.api_client.get('/')  # Any endpoint will trigger the DisallowedHost check

            # Verify response format
            assert response.status_code == status.HTTP_400_BAD_REQUEST
            response_json = response.json()
            assert response_json['code'] == ApiErrorCodeNumeric.SECURITY_ERROR
            assert response_json['details']['message'] == 'Invalid host header'

            # Verify logging
            assert len(log.output) >= 2  # Should have at least exception type and message
            assert "DisallowedHost" in log.output[0]  # Exception type
            assert "Invalid HTTP_HOST header" in log.output[1]  # Exception message
