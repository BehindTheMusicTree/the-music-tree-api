from typing import Optional, TypedDict
import logging

import spotipy
from django.conf import settings
from spotipy.oauth2 import SpotifyOAuth

from api.exception import spotify as spotify_exception

logger = logging.getLogger(settings.APP_NAME)


class TokenInfo(TypedDict):
    access_token: str
    refresh_token: str
    expires_in: int


class SpotifyOAuthService:
    """Service class for handling Spotify OAuth authentication"""

    def __init__(self):
        """Initialize with Spotify OAuth configuration"""
        self.oauth = SpotifyOAuth(
            client_id=settings.SPOTIFY_CLIENT_ID,
            client_secret=settings.SPOTIFY_CLIENT_SECRET,
            redirect_uri=settings.SPOTIFY_REDIRECT_URI,
            scope='user-read-email user-read-private user-library-read'
        )

    def get_auth_url(self, state: Optional[str] = None) -> str:
        """
        Get the Spotify authorization URL

        Args:
            state: Optional state parameter for CSRF protection

        Returns:
            The authorization URL
        """
        return self.oauth.get_authorize_url(state=state)

    def get_access_token(self, code: str) -> TokenInfo:
        """
        Exchange authorization code for access token

        Args:
            code: The authorization code from Spotify

        Returns:
            Dictionary containing access token and refresh token
        """
        try:
            token_info = self.oauth.get_access_token(code)
            if token_info is None:
                raise spotify_exception.SpotifyAuthenticationException(
                    "Failed to get access token: No token info returned")
            return token_info
        except Exception as e:
            logger.error(f"Failed to get access token: {str(e)}")
            raise spotify_exception.SpotifyAuthenticationException(f"Failed to get access token: {str(e)}")

    def refresh_access_token(self, refresh_token: str) -> TokenInfo:
        """
        Refresh an expired access token

        Args:
            refresh_token: The refresh token

        Returns:
            Dictionary containing new access token
        """
        try:
            token_info = self.oauth.refresh_access_token(refresh_token)
            if token_info is None:
                raise spotify_exception.SpotifyAuthenticationException(
                    "Failed to refresh access token: No token info returned")
            return token_info
        except Exception as e:
            logger.error(f"Failed to refresh access token: {str(e)}")
            raise spotify_exception.SpotifyAuthenticationException(f"Failed to refresh access token: {str(e)}")

    def get_user_info(self, access_token: str) -> dict:
        """
        Get user information from Spotify

        Args:
            access_token: The access token

        Returns:
            Dictionary containing user information
        """
        try:
            sp = spotipy.Spotify(auth=access_token)
            user_info = sp.current_user()
            if user_info is None:
                raise spotify_exception.SpotifyAuthenticationException("Failed to get user info: No user info returned")
            return user_info
        except Exception as e:
            logger.error(f"Failed to get user info: {str(e)}")
            raise spotify_exception.SpotifyAuthenticationException(f"Failed to get user info: {str(e)}")
