from rest_framework import status

from bodzify_api import settings
from bodzify_api.test.utils.AppTestCase import AppTestCase
from bodzify_api.view.error.ApiErrorCode import ApiErrorCodeNumeric


class TestCase(AppTestCase):
    def test_invalid_credentials_then_401(self):
        response = self.api_client.post(f'/{settings.API_ROOT_BASE}auth/token/', data={
            'username': 'invalid_user',
            'password': 'invalid_password'
        })

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json()['code'] == ApiErrorCodeNumeric.AUTH_INVALID_CREDENTIALS
        assert 'message' in response.json()['details']
        assert 'code' in response.json()['details']

    def test_not_logged_in_then_401(self):
        response = self._post_lib_track_being_logged_out()

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_refresh_fails_then_401(self):
        response = self.api_client.post(f'/{settings.API_ROOT_BASE}auth/token/refresh/', data={
            'refresh': 'invalid_refresh_token'
        })

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
