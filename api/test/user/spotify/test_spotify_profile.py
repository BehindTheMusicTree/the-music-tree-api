from unittest import mock

from api.exception.spotify import SpotifyAuthenticationException
from api.test.utils.AppTestCase import AppTestCase
from api.utils.spotify_api.oauth import SpotifyOAuthService
from api.model.user.spotify.Fields import Fields
from api.model.user.spotify.SpotifyUser import SpotifyUser


class TestSpotifyProfile(AppTestCase):
    def setUp(self):
        super().setUp()
        self.test_user1 = SpotifyUser.objects.create_instance(
            username='spotify_user1', password='spotify_user1', email='spotify@user1.com', is_test_user=True,
            spotify_id='spotify_user1_id')
        self.test_user2 = SpotifyUser.objects.create_instance(
            username='spotify_user2', password='spotify_user2', email='spotify@user2.com', is_test_user=True,
            spotify_id='spotify_user2_id')
        self._login_as_test_user1()

    @mock.patch('api.utils_api.oauth.spotipy.Spotify')
    def test_get_user_info_with_valid_token_then_returns_complete_profile(self, mock_spotify):
        mock_spotify.return_value.current_user.return_value = {
            Fields.ID: "test_user",
            Fields.EMAIL: "test@example.com",
            Fields.DISPLAY_NAME: "Test User",
            Fields.COUNTRY: "US",
            Fields.PRODUCT: "premium",
            Fields.IMAGES: [{Fields.URL: "https://example.com/image.jpg"}]
        }

        service = SpotifyOAuthService()
        user_info = service.get_user_info("valid_token")

        assert user_info[Fields.ID] == "test_user"
        assert user_info[Fields.EMAIL] == "test@example.com"
        assert user_info[Fields.DISPLAY_NAME] == "Test User"
        assert user_info[Fields.COUNTRY] == "US"
        assert user_info[Fields.PRODUCT] == "premium"
        assert len(user_info[Fields.IMAGES]) == 1
        assert user_info[Fields.IMAGES][0][Fields.URL] == "https://example.com/image.jpg"
        mock_spotify.return_value.current_user.assert_called_once()

    @mock.patch('api.utils_api.oauth.spotipy.Spotify')
    def test_get_user_info_with_minimal_profile_then_returns_basic_fields(self, mock_spotify):
        mock_spotify.return_value.current_user.return_value = {
            Fields.ID: "test_user",
            Fields.DISPLAY_NAME: "Test User"
        }

        service = SpotifyOAuthService()
        user_info = service.get_user_info("valid_token")

        assert user_info[Fields.ID] == "test_user"
        assert user_info[Fields.DISPLAY_NAME] == "Test User"
        assert Fields.EMAIL not in user_info
        assert Fields.COUNTRY not in user_info
        assert Fields.PRODUCT not in user_info
        assert Fields.IMAGES not in user_info
        mock_spotify.return_value.current_user.assert_called_once()

    @mock.patch('api.utils_api.oauth.spotipy.Spotify')
    def test_get_user_info_with_invalid_token_then_raises_exception(self, mock_spotify):
        mock_spotify.return_value.current_user.side_effect = Exception("Invalid token")

        service = SpotifyOAuthService()
        with self.assertRaises(SpotifyAuthenticationException) as context:
            service.get_user_info("invalid_token")
        assert "Failed to get user info" in str(context.exception)

    @mock.patch('api.utils_api.oauth.spotipy.Spotify')
    def test_get_user_info_with_network_error_then_raises_exception(self, mock_spotify):
        mock_spotify.return_value.current_user.side_effect = Exception("Network error")

        service = SpotifyOAuthService()
        with self.assertRaises(SpotifyAuthenticationException) as context:
            service.get_user_info("valid_token")
        assert "Failed to get user info" in str(context.exception)
