from unittest import mock

from api.exception.spotify import SpotifyAuthenticationException
from api.test.utils.AppTestCase import AppTestCase
from api.utils.spotify_api.oauth import SpotifyOAuthService
from api.serializer.token.Fields import Fields


class TestSpotifyOAuthAuth(AppTestCase):
    @mock.patch('api.utils_api.oauth.SpotifyOAuth')
    def test_get_auth_url_then_returns_url(self, mock_oauth):
        mock_oauth.return_value.get_authorize_url.return_value = "https://accounts.spotify.com/authorize"

        service = SpotifyOAuthService()
        url = service.get_auth_url()

        assert url == "https://accounts.spotify.com/authorize"
        mock_oauth.return_value.get_authorize_url.assert_called_once()

    @mock.patch('api.utils_api.oauth.SpotifyOAuth')
    def test_get_access_token_with_valid_code_then_returns_tokens(self, mock_oauth):
        mock_oauth.return_value.get_access_token.return_value = {
            Fields.ACCESS_TOKEN: "test_access_token",
            Fields.REFRESH_TOKEN: "test_refresh_token",
            Fields.EXPIRES_IN: 3600
        }

        service = SpotifyOAuthService()
        tokens = service.get_access_token("valid_code")

        assert tokens[Fields.ACCESS_TOKEN] == "test_access_token"
        assert tokens[Fields.REFRESH_TOKEN] == "test_refresh_token"
        assert tokens[Fields.EXPIRES_IN] == 3600
        mock_oauth.return_value.get_access_token.assert_called_once_with("valid_code")

    @mock.patch('api.utils_api.oauth.SpotifyOAuth')
    def test_get_access_token_with_invalid_code_then_raises_exception(self, mock_oauth):
        mock_oauth.return_value.get_access_token.side_effect = Exception("Invalid code")

        service = SpotifyOAuthService()
        with self.assertRaises(SpotifyAuthenticationException) as context:
            service.get_access_token("invalid_code")
        assert "Failed to get access token" in str(context.exception)

    @mock.patch('api.utils_api.oauth.SpotifyOAuth')
    def test_refresh_access_token_with_valid_token_then_returns_new_token(self, mock_oauth):
        mock_oauth.return_value.refresh_access_token.return_value = {
            Fields.ACCESS_TOKEN: "new_access_token",
            Fields.EXPIRES_IN: 3600
        }

        service = SpotifyOAuthService()
        tokens = service.refresh_access_token("valid_refresh_token")

        assert tokens[Fields.ACCESS_TOKEN] == "new_access_token"
        assert tokens[Fields.EXPIRES_IN] == 3600
        mock_oauth.return_value.refresh_access_token.assert_called_once_with("valid_refresh_token")

    @mock.patch('api.utils_api.oauth.SpotifyOAuth')
    def test_refresh_access_token_with_invalid_token_then_raises_exception(self, mock_oauth):
        mock_oauth.return_value.refresh_access_token.side_effect = Exception("Invalid refresh token")

        service = SpotifyOAuthService()
        with self.assertRaises(SpotifyAuthenticationException) as context:
            service.refresh_access_token("invalid_refresh_token")
        assert "Failed to refresh access token" in str(context.exception)

    @mock.patch('api.utils_api.oauth.spotipy.Spotify')
    def test_get_user_info_with_valid_token_then_returns_user_info(self, mock_spotify):
        mock_spotify.return_value.current_user.return_value = {
            "id": "test_user",
            "email": "test@example.com",
            "display_name": "Test User"
        }

        service = SpotifyOAuthService()
        user_info = service.get_user_info("valid_token")

        assert user_info["id"] == "test_user"
        assert user_info["email"] == "test@example.com"
        assert user_info["display_name"] == "Test User"
        mock_spotify.return_value.current_user.assert_called_once()

    @mock.patch('api.utils_api.oauth.spotipy.Spotify')
    def test_get_user_info_with_invalid_token_then_raises_exception(self, mock_spotify):
        mock_spotify.return_value.current_user.side_effect = Exception("Invalid token")

        service = SpotifyOAuthService()
        with self.assertRaises(SpotifyAuthenticationException) as context:
            service.get_user_info("invalid_token")
        assert "Failed to get user info" in str(context.exception)
