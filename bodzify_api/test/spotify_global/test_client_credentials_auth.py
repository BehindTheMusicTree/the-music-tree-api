from unittest import mock

from django.test import override_settings

from bodzify_api.exception.spotify import SpotifyAPIException
from bodzify_api.test.utils.AppTestCase import AppTestCase
from bodzify_api.utils.spotify_api.SpotifyClient import SpotifyClient


class TestClientCredentialsAuth(AppTestCase):
    @mock.patch('bodzify_api.utils.spotify_api.lib_track_manager.SpotifyClientCredentials')
    @mock.patch('bodzify_api.utils.spotify_api.SpotifyClient.spotipy.Spotify')
    def test_authenticate_with_valid_credentials_then_succeeds(self, mock_spotify, mock_credentials):
        mock_instance = mock_spotify.return_value
        mock_instance.me.return_value = {"id": "test_user", "product": "premium"}

        service = SpotifyClient()

        mock_credentials.assert_called_once()
        mock_spotify.assert_called_once()
        assert service.spotify == mock_instance

    @mock.patch('bodzify_api.utils.spotify_api.lib_track_manager.SpotifyClientCredentials')
    @mock.patch('bodzify_api.utils.spotify_api.SpotifyClient.spotipy.Spotify')
    @override_settings(SPOTIFY_CLIENT_ID="", SPOTIFY_CLIENT_SECRET="")
    def test_authenticate_with_empty_credentials_then_raises_exception(self, mock_spotify, mock_credentials):
        mock_credentials.side_effect = ValueError("Client ID and Secret cannot be empty")

        with self.assertRaises(SpotifyAPIException) as context:
            SpotifyClient()
        assert "Client ID and Secret cannot be empty" in str(context.exception)

    @mock.patch('bodzify_api.utils.spotify_api.lib_track_manager.SpotifyClientCredentials')
    @mock.patch('bodzify_api.utils.spotify_api.SpotifyClient.spotipy.Spotify')
    def test_authenticate_with_invalid_credentials_then_raises_exception(self, mock_spotify, mock_credentials):
        mock_credentials.return_value = mock.MagicMock()
        spotify_exception = type('SpotipyException', (Exception,), {'http_status': 401})
        mock_spotify.side_effect = spotify_exception("Invalid client")

        with self.assertRaises(SpotifyAPIException) as context:
            SpotifyClient()
        assert "Invalid client" in str(context.exception)

    @mock.patch('bodzify_api.utils.spotify_api.lib_track_manager.SpotifyClientCredentials')
    @mock.patch('bodzify_api.utils.spotify_api.SpotifyClient.spotipy.Spotify')
    def test_authenticate_with_network_error_then_raises_exception(self, mock_spotify, mock_credentials):
        mock_credentials.return_value = mock.MagicMock()
        spotify_exception = type('SpotipyException', (Exception,), {'http_status': None})
        mock_spotify.side_effect = spotify_exception("Connection error")

        with self.assertRaises(SpotifyAPIException) as context:
            SpotifyClient()
        assert "Connection error" in str(context.exception)

    @mock.patch('bodzify_api.utils.spotify_api.lib_track_manager.SpotifyClientCredentials')
    @mock.patch('bodzify_api.utils.spotify_api.SpotifyClient.spotipy.Spotify')
    def test_authenticate_with_rate_limit_then_raises_exception(self, mock_spotify, mock_credentials):
        mock_credentials.return_value = mock.MagicMock()
        spotify_exception = type('SpotipyException', (Exception,), {'http_status': 429})
        mock_spotify.side_effect = spotify_exception("Rate limit exceeded")

        with self.assertRaises(SpotifyAPIException) as context:
            SpotifyClient()
        assert "Rate limit exceeded" in str(context.exception)

    @mock.patch('bodzify_api.utils.spotify_api.lib_track_manager.settings')
    def test_authenticate_with_settings_then_uses_configured_values(self, mock_settings):
        mock_settings.SPOTIFY_CLIENT_ID = "test_client_id"
        mock_settings.SPOTIFY_CLIENT_SECRET = "test_client_secret"

        service = SpotifyClient()
        assert service.spotify is not None
