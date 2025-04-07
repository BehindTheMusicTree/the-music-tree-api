from django.test import TestCase
from rest_framework import status
import json

from bodzify_api.exception.spotify import SpotifyAuthenticationException
from bodzify_api.view.error.ErrorResponse import ErrorResponse
from bodzify_api.view.error.ApiErrorCode import ApiErrorCodeNumeric
from bodzify_api.view.error.ErrorResponseFields import ErrorResponseFields


class TestSpotifyGlobalErrorHandling(TestCase):
    def test_spotify_authentication_exception_then_401_unauthorized(self):
        exception = SpotifyAuthenticationException("Invalid Spotify credentials")
        response = ErrorResponse.handle_exception(exception)
        response_data = json.loads(response.content)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response_data[ErrorResponseFields.CODE] == ApiErrorCodeNumeric.AUTH_INVALID_CREDENTIALS
        assert response_data[ErrorResponseFields.DETAILS][ErrorResponseFields.MESSAGE] == "Invalid Spotify credentials"
        assert response_data[ErrorResponseFields.DETAILS][ErrorResponseFields.CODE] == 'spotify_authentication_error'
        assert not response_data[ErrorResponseFields.SUCCESS]

    def test_spotify_authentication_exception_with_empty_message_then_401_unauthorized(self):
        exception = SpotifyAuthenticationException("")
        response = ErrorResponse.handle_exception(exception)
        response_data = json.loads(response.content)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response_data[ErrorResponseFields.CODE] == ApiErrorCodeNumeric.AUTH_INVALID_CREDENTIALS
        assert response_data[ErrorResponseFields.DETAILS][ErrorResponseFields.MESSAGE] == ""
        assert response_data[ErrorResponseFields.DETAILS][ErrorResponseFields.CODE] == 'spotify_authentication_error'
        assert not response_data[ErrorResponseFields.SUCCESS]

    def test_spotify_authentication_exception_with_none_message_then_401_unauthorized(self):
        exception = SpotifyAuthenticationException(None)
        response = ErrorResponse.handle_exception(exception)
        response_data = json.loads(response.content)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response_data[ErrorResponseFields.CODE] == ApiErrorCodeNumeric.AUTH_INVALID_CREDENTIALS
        assert response_data[ErrorResponseFields.DETAILS][ErrorResponseFields.MESSAGE] == "None"
        assert response_data[ErrorResponseFields.DETAILS][ErrorResponseFields.CODE] == 'spotify_authentication_error'
        assert not response_data[ErrorResponseFields.SUCCESS]
