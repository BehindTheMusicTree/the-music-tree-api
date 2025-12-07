from typing import Any
import spotipy
from spotipy import exceptions as spotipy_exceptions
from spotipy.oauth2 import SpotifyOAuth

from api.exception import spotify as spotify_exception
from api.utils.spotify_api.SpotifyCredentialManager import SpotifyCredentialManager


class SpotifyClient:
    _instance: 'SpotifyClient | None' = None

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
        credentials = self.credential_manager.get_client_credentials()

        self.auth_manager = SpotifyOAuth(
            client_id=credentials["client_id"],
            client_secret=credentials["client_secret"],
            redirect_uri=credentials["redirect_uri"],
            scope=credentials["scope"]
        )
        self.spotify = spotipy.Spotify(auth_manager=self.auth_manager, requests_timeout=30)
        self._initialized = True

    def get_access_token_from_code(self, code: str) -> dict[str, Any]:
        try:
            token = self.auth_manager.get_access_token(code)
            if not token:
                raise spotify_exception.SpotifyAuthenticationException("Failed to get access token: No token returned")
            return token
        except Exception as e:
            raise spotify_exception.SpotifyAuthenticationException(
                f"Failed to get access token: {str(e)}"
            )

    def refresh_access_token(self, refresh_token: str) -> dict[str, Any]:
        try:
            token = self.auth_manager.refresh_access_token(refresh_token)
            if not token:
                raise spotify_exception.SpotifyAuthenticationException(
                    "Failed to refresh access token: No token returned")
            return token
        except Exception as e:
            raise spotify_exception.SpotifyAuthenticationException(
                f"Failed to refresh access token: {str(e)}"
            )

    def retrieve_track_by_id(self, track_id: str) -> dict[str, Any]:
        try:
            track = self.spotify.track(track_id)
            if not track:
                raise spotify_exception.SpotifyResourceNotFoundException(f"Track not found: {track_id}")
            return track
        except spotipy_exceptions.SpotifyException as e:
            if hasattr(e, 'http_status') and e.http_status == 404:
                raise spotify_exception.SpotifyResourceNotFoundException(f"Track not found: {track_id}")
            raise spotify_exception.SpotifyException(f"Failed to retrieve track: {str(e)}")
        except Exception as e:
            raise spotify_exception.SpotifyException(f"Failed to retrieve track: {str(e)}")

    def search_track(self, query: str, limit: int = 5) -> dict[str, Any]:
        try:
            result = self.spotify.search(q=query, type='track', limit=limit)
            if not result:
                return {"tracks": {"items": []}}
            return result
        except Exception as e:
            raise spotify_exception.SpotifyException(f"Failed to search tracks: {str(e)}")

    def get_user_saved_tracks(
        self, access_token: str, limit: int = 50, offset: int = 0
    ) -> dict[str, Any]:
        try:
            tracks = self.spotify.current_user_saved_tracks(limit=limit, offset=offset)
            if not tracks:
                return {"items": []}
            return tracks
        except Exception as e:
            raise spotify_exception.SpotifyException(f"Failed to get saved tracks: {str(e)}")

    def get_user_playlists(
        self, access_token: str, limit: int = 50, offset: int = 0
    ) -> dict[str, Any]:
        try:
            playlists = self.spotify.current_user_playlists(limit=limit, offset=offset)
            if not playlists:
                return {"items": []}
            return playlists
        except Exception as e:
            raise spotify_exception.SpotifyException(f"Failed to get playlists: {str(e)}")

    def get_playlist_tracks(
        self, access_token: str, playlist_id: str, limit: int = 50, offset: int = 0
    ) -> dict[str, Any]:
        try:
            tracks = self.spotify.playlist_tracks(playlist_id, limit=limit, offset=offset)
            if not tracks:
                return {"items": []}
            return tracks
        except Exception as e:
            raise spotify_exception.SpotifyException(f"Failed to get playlist tracks: {str(e)}")

    def get_track(self, access_token: str, track_id: str) -> dict[str, Any]:
        try:
            track = self.spotify.track(track_id)
            if not track:
                raise spotify_exception.SpotifyResourceNotFoundException(f"Track not found: {track_id}")
            return track
        except Exception as e:
            raise spotify_exception.SpotifyException(f"Failed to get track: {str(e)}")

    def search_tracks(
        self, access_token: str, query: str, limit: int = 50, offset: int = 0
    ) -> dict[str, Any]:
        try:
            result = self.spotify.search(q=query, type='track', limit=limit, offset=offset)
            if not result:
                return {"tracks": {"items": []}}
            return result
        except Exception as e:
            raise spotify_exception.SpotifyException(f"Failed to search tracks: {str(e)}")

    def get_user_profile(self, access_token: str) -> dict[str, Any]:
        try:
            profile = self.spotify.current_user()
            if not profile:
                raise spotify_exception.SpotifyResourceNotFoundException("User profile not found")
            return profile
        except Exception as e:
            raise spotify_exception.SpotifyException(f"Failed to get user profile: {str(e)}")


spotify_client = SpotifyClient()
