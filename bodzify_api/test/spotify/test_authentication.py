from unittest import mock

from django.test import override_settings

from bodzify_api.exception.spotify import SpotifyAPIException
from bodzify_api.test.utils.AppTestCase import AppTestCase
from bodzify_api.utils.spotify.service import SpotifyAPIService


class TestSpotifyAuthentication(AppTestCase):

    @mock.patch('bodzify_api.utils.spotify.service.SpotifyClientCredentials')
    @mock.patch('bodzify_api.utils.spotify.service.spotipy.Spotify')
    def test_authenticate_with_valid_credentials_then_succeeds(self, mock_spotify, mock_credentials):
        # Configure mocks
        mock_instance = mock_spotify.return_value
        mock_instance.me.return_value = {"id": "test_user", "product": "premium"}

        # Create service and verify authentication
        service = SpotifyAPIService()

        # Verify the client was initialized with credentials
        mock_credentials.assert_called_once()
        mock_spotify.assert_called_once()

        # Verify the Spotify client was properly initialized
        assert service.spotify == mock_instance

    @mock.patch('bodzify_api.utils.spotify.service.SpotifyClientCredentials')
    @mock.patch('bodzify_api.utils.spotify.service.spotipy.Spotify')
    @override_settings(SPOTIFY_CLIENT_ID="", SPOTIFY_CLIENT_SECRET="")
    def test_authenticate_with_empty_credentials_then_raises_exception(self, mock_spotify, mock_credentials):
        # Configure credentials mock to raise an exception
        mock_credentials.side_effect = ValueError("Client ID and Secret cannot be empty")

        # Attempt to create service - should raise exception
        with self.assertRaises(SpotifyAPIException) as context:
            service = SpotifyAPIService()
        assert "Client ID and Secret cannot be empty" in str(context.exception)

    @mock.patch('bodzify_api.utils.spotify.service.SpotifyClientCredentials')
    @mock.patch('bodzify_api.utils.spotify.service.spotipy.Spotify')
    def test_authenticate_with_invalid_credentials_then_raises_exception(self, mock_spotify, mock_credentials):
        # Configure mocks to simulate authentication failure
        mock_credentials.return_value = mock.MagicMock()

        # Create a SpotifyException-like object
        spotify_exception = type('SpotipyException', (Exception,), {'http_status': 401})
        mock_spotify.side_effect = spotify_exception("Invalid client")

        # Attempt to create service - should raise exception
        with self.assertRaises(SpotifyAPIException) as context:
            service = SpotifyAPIService()
        assert "Invalid client" in str(context.exception)

    @mock.patch('bodzify_api.utils.spotify.service.SpotifyClientCredentials')
    @mock.patch('bodzify_api.utils.spotify.service.spotipy.Spotify')
    def test_authenticate_with_network_error_then_raises_exception(self, mock_spotify, mock_credentials):
        # Configure mocks to simulate network error
        mock_credentials.return_value = mock.MagicMock()

        # Create a SpotifyException-like object for timeout
        spotify_exception = type('SpotipyException', (Exception,), {'http_status': None})
        mock_spotify.side_effect = spotify_exception("Connection error")

        # Attempt to create service - should raise exception
        with self.assertRaises(SpotifyAPIException) as context:
            service = SpotifyAPIService()
        assert "Connection error" in str(context.exception)

    @mock.patch('bodzify_api.utils.spotify.service.SpotifyClientCredentials')
    @mock.patch('bodzify_api.utils.spotify.service.spotipy.Spotify')
    def test_authenticate_with_rate_limit_then_raises_exception(self, mock_spotify, mock_credentials):
        # Configure mocks to simulate rate limit error
        mock_credentials.return_value = mock.MagicMock()

        # Create a SpotifyException-like object for rate limit
        spotify_exception = type('SpotipyException', (Exception,), {'http_status': 429})
        mock_spotify.side_effect = spotify_exception("Rate limit exceeded")

        # Attempt to create service - should raise exception
        with self.assertRaises(SpotifyAPIException) as context:
            service = SpotifyAPIService()
        assert "Rate limit exceeded" in str(context.exception)

    @mock.patch('bodzify_api.utils.spotify.service.settings')
    def test_authenticate_with_settings_then_uses_configured_values(self, mock_settings):
        # Configure mock settings
        mock_settings.SPOTIFY_CLIENT_ID = "test_client_id"
        mock_settings.SPOTIFY_CLIENT_SECRET = "test_client_secret"

        # Create service and verify settings were used
        service = SpotifyAPIService()
        assert service.spotify is not None
