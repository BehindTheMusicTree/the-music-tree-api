from django.test import TestCase
from rest_framework import status
import json

from bodzify_api.exception.spotify import SpotifyAuthenticationException
from bodzify_api.view.error.ErrorResponse import ErrorResponse
from bodzify_api.view.error.ApiErrorCode import ApiErrorCodeNumeric


class TestSpotifyGlobalErrorHandling(TestCase):
    def test_spotify_authentication_exception_then_401_unauthorized(self):
        exception = SpotifyAuthenticationException("Invalid Spotify credentials")
        response = ErrorResponse.handle_exception(exception)
        response_data = json.loads(response.content)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response_data['code'] == ApiErrorCodeNumeric.AUTH_INVALID_CREDENTIALS
        assert response_data['details']['message'] == "Invalid Spotify credentials"
        assert response_data['details']['code'] == 'spotify_authentication_error'
        assert not response_data['success']

    def test_spotify_authentication_exception_with_empty_message_then_401_unauthorized(self):
        exception = SpotifyAuthenticationException("")
        response = ErrorResponse.handle_exception(exception)
        response_data = json.loads(response.content)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response_data['code'] == ApiErrorCodeNumeric.AUTH_INVALID_CREDENTIALS
        assert response_data['details']['message'] == ""
        assert response_data['details']['code'] == 'spotify_authentication_error'
        assert not response_data['success']

    def test_spotify_authentication_exception_with_none_message_then_401_unauthorized(self):
        exception = SpotifyAuthenticationException(None)
        response = ErrorResponse.handle_exception(exception)
        response_data = json.loads(response.content)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response_data['code'] == ApiErrorCodeNumeric.AUTH_INVALID_CREDENTIALS
        assert response_data['details']['message'] == "None"
        assert response_data['details']['code'] == 'spotify_authentication_error'
        assert not response_data['success']
