from unittest import mock

from django.test import override_settings

from bodzify_api.exception.spotify import SpotifyAPIException
from bodzify_api.test.utils.AppTestCase import AppTestCase
from bodzify_api.utils.spotify_api.SpotifyClient import SpotifyClient


class TestClientCredentialsAuth(AppTestCase):
    @mock.patch('bodzify_api.utils.spotify_api.SpotifyClient.SpotifyCredentialManager')
    @mock.patch('spotipy.Spotify')
    def test_authenticate_with_valid_credentials_then_succeeds(self, mock_spotify, mock_credentials):
        # Reset singleton to ensure fresh instance
        SpotifyClient._instance = None
        SpotifyClient._initialized = False
        
        mock_instance = mock_spotify.return_value
        mock_instance.me.return_value = {"id": "test_user", "product": "premium"}
        
        mock_cred_instance = mock.MagicMock()
        mock_cred_instance.validate_credentials.return_value = None
        mock_cred_instance.get_client_credentials.return_value = {
            "client_id": "test_id",
            "client_secret": "test_secret",
            "redirect_uri": "http://test.com",
            "scope": "test_scope"
        }
        mock_credentials.return_value = mock_cred_instance

        service = SpotifyClient()

        mock_credentials.assert_called_once()
        mock_spotify.assert_called_once()
        assert service.spotify == mock_instance

    @mock.patch('bodzify_api.utils.spotify_api.SpotifyClient.SpotifyCredentialManager')
    @mock.patch('spotipy.Spotify')
    def test_authenticate_with_empty_credentials_then_raises_exception(self, mock_spotify, mock_cred_manager_class):
        # Reset singleton to ensure fresh instance
        SpotifyClient._instance = None
        SpotifyClient._initialized = False
        
        from bodzify_api.exception.spotify import SpotifyAPIException
        mock_instance = mock.MagicMock()
        mock_instance.validate_credentials.side_effect = SpotifyAPIException("Spotify client credentials are not configured")
        mock_cred_manager_class.return_value = mock_instance

        with self.assertRaises(SpotifyAPIException) as context:
            SpotifyClient()
        assert "Spotify client credentials are not configured" in str(context.exception)

    @mock.patch('bodzify_api.utils.spotify_api.SpotifyClient.SpotifyCredentialManager')
    @mock.patch('spotipy.Spotify')
    def test_authenticate_with_invalid_credentials_then_raises_exception(self, mock_spotify, mock_credentials):
        # Reset singleton to ensure fresh instance
        SpotifyClient._instance = None
        SpotifyClient._initialized = False
        
        mock_instance = mock.MagicMock()
        mock_instance.validate_credentials.return_value = None
        mock_instance.get_client_credentials.return_value = {
            "client_id": "test_id",
            "client_secret": "test_secret",
            "redirect_uri": "http://test.com",
            "scope": "test_scope"
        }
        mock_credentials.return_value = mock_instance
        
        from bodzify_api.exception.spotify import SpotifyAPIException
        mock_spotify.side_effect = SpotifyAPIException("Invalid client")

        with self.assertRaises(SpotifyAPIException) as context:
            SpotifyClient()
        assert "Invalid client" in str(context.exception)

    @mock.patch('bodzify_api.utils.spotify_api.SpotifyClient.SpotifyCredentialManager')
    @mock.patch('spotipy.Spotify')
    def test_authenticate_with_network_error_then_raises_exception(self, mock_spotify, mock_credentials):
        # Reset singleton to ensure fresh instance
        SpotifyClient._instance = None
        SpotifyClient._initialized = False
        
        mock_instance = mock.MagicMock()
        mock_instance.validate_credentials.return_value = None
        mock_instance.get_client_credentials.return_value = {
            "client_id": "test_id",
            "client_secret": "test_secret",
            "redirect_uri": "http://test.com",
            "scope": "test_scope"
        }
        mock_credentials.return_value = mock_instance
        
        mock_spotify.side_effect = SpotifyAPIException("Connection error")

        with self.assertRaises(SpotifyAPIException) as context:
            SpotifyClient()
        assert "Connection error" in str(context.exception)

    @mock.patch('bodzify_api.utils.spotify_api.SpotifyClient.SpotifyCredentialManager')
    @mock.patch('spotipy.Spotify')
    def test_authenticate_with_rate_limit_then_raises_exception(self, mock_spotify, mock_credentials):
        # Reset singleton to ensure fresh instance
        SpotifyClient._instance = None
        SpotifyClient._initialized = False
        
        mock_instance = mock.MagicMock()
        mock_instance.validate_credentials.return_value = None
        mock_instance.get_client_credentials.return_value = {
            "client_id": "test_id",
            "client_secret": "test_secret",
            "redirect_uri": "http://test.com",
            "scope": "test_scope"
        }
        mock_credentials.return_value = mock_instance
        
        mock_spotify.side_effect = SpotifyAPIException("Rate limit exceeded")

        with self.assertRaises(SpotifyAPIException) as context:
            SpotifyClient()
        assert "Rate limit exceeded" in str(context.exception)

    def test_authenticate_with_settings_then_uses_configured_values(self):
        # Reset singleton to ensure fresh instance
        SpotifyClient._instance = None
        SpotifyClient._initialized = False

        service = SpotifyClient()
        assert service.spotify is not None
