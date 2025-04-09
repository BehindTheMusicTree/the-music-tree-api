from typing import Optional
import requests
import spotipy

from bodzify_api.exception import spotify as spotify_exception
from bodzify_api.utils.spotify_api.SpotifyCredentialManager import SpotifyCredentialManager


class SpotifyClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self.credential_manager = SpotifyCredentialManager()
        self.credential_manager.validate_credentials()
        self.base_url = "https://api.spotify.com/v1"
        self.auth_url = "https://accounts.spotify.com/api/token"
        self.spotify = spotipy.Spotify()
        self._initialized = True

    def get_access_token_from_code(self, code: str) -> dict:
        """
        Get access token from Spotify API using authorization code.
        """
        credentials = self.credential_manager.get_client_credentials()
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": credentials["redirect_uri"],
            "client_id": credentials["client_id"],
            "client_secret": credentials["client_secret"],
        }
        response = requests.post(self.auth_url, data=data)
        if response.status_code != 200:
            raise spotify_exception.SpotifyAuthenticationException(
                f"Failed to get access token: {response.text}"
            )
        return response.json()

    def refresh_access_token(self, refresh_token: str) -> dict:
        """
        Refresh access token using refresh token.
        """
        credentials = self.credential_manager.get_client_credentials()
        data = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": credentials["client_id"],
            "client_secret": credentials["client_secret"],
        }
        response = requests.post(self.auth_url, data=data)
        if response.status_code != 200:
            raise spotify_exception.SpotifyAuthenticationException(
                f"Failed to refresh access token: {response.text}"
            )
        return response.json()

    def retrieve_track_by_id(self, track_id: str) -> dict | None:
        try:
            return self.spotify.track(track_id)
        except Exception as e:
            raise spotify_exception.SpotifyException(f"Failed to retrieve track: {str(e)}")

    def search_track(self, query: str, limit: int = 5) -> dict | None:
        try:
            return self.spotify.search(q=query, type='track', limit=limit)
        except Exception as e:
            raise spotify_exception.SpotifyException(f"Failed to search tracks: {str(e)}")

    def _make_request(
        self, method: str, endpoint: str, access_token: str, params: Optional[dict] = None
    ) -> dict:
        headers = {"Authorization": f"Bearer {access_token}"}
        url = f"{self.base_url}/{endpoint}"
        response = requests.request(method, url, headers=headers, params=params)

        if response.status_code == 401:
            raise spotify_exception.SpotifyAuthenticationException(
                "Invalid or expired access token"
            )
        elif response.status_code == 403:
            raise spotify_exception.SpotifyException(
                "Insufficient permissions"
            )
        elif response.status_code == 404:
            raise spotify_exception.SpotifyResourceNotFoundException(
                "Resource not found"
            )
        elif response.status_code == 429:
            raise spotify_exception.SpotifyRateLimitException(
                "Rate limit exceeded"
            )
        elif response.status_code != 200:
            raise spotify_exception.SpotifyException(
                f"Spotify API error: {response.text}"
            )

        return response.json()

    def get_user_saved_tracks(
        self, access_token: str, limit: int = 50, offset: int = 0
    ) -> dict:
        return self._make_request(
            "GET",
            "me/tracks",
            access_token,
            params={"limit": limit, "offset": offset},
        )

    def get_user_playlists(
        self, access_token: str, limit: int = 50, offset: int = 0
    ) -> dict:
        return self._make_request(
            "GET",
            "me/playlists",
            access_token,
            params={"limit": limit, "offset": offset},
        )

    def get_playlist_tracks(
        self, access_token: str, playlist_id: str, limit: int = 50, offset: int = 0
    ) -> dict:
        """
        Get tracks from a playlist.
        """
        return self._make_request(
            "GET",
            f"playlists/{playlist_id}/tracks",
            access_token,
            params={"limit": limit, "offset": offset},
        )

    def get_track(self, access_token: str, track_id: str) -> dict:
        """
        Get track details.
        """
        return self._make_request("GET", f"tracks/{track_id}", access_token)

    def search_tracks(
        self, access_token: str, query: str, limit: int = 50, offset: int = 0
    ) -> dict:
        """
        Search for tracks.
        """
        return self._make_request(
            "GET",
            "search",
            access_token,
            params={
                "q": query,
                "type": "track",
                "limit": limit,
                "offset": offset,
            },
        )

    def get_user_profile(self, access_token: str) -> dict:
        """
        Get user's profile.
        """
        return self._make_request("GET", "me", access_token)


spotify_client = SpotifyClient()
