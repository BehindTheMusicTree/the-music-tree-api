from unittest import mock
from spotipy.exceptions import SpotifyException as SpotipyException

from bodzify_api.exception.spotify import (
    SpotifyResourceNotFoundException,
    SpotifyNetworkException
)
from bodzify_api.model.spotify_resource.children.track.SpotifyTrack import SpotifyTrack
from bodzify_api.test.utils.AppTestCase import AppTestCase
from bodzify_api.utils.spotify.service import SpotifyAPIService, search_spotify_tracks, get_or_create_spotify_track
from bodzify_api.utils.spotify.ApiFields import ApiFields


class TestSpotifyAPIOperations(AppTestCase):
    """
    Test suite for Spotify API operations
    """

    def setUp(self):
        super().setUp()
        self._login_as_test_user1()

        # Set up common mocks
        self.mock_spotify_patcher = mock.patch('bodzify_api.utils.spotify.service.spotipy.Spotify')
        self.mock_credentials_patcher = mock.patch('bodzify_api.utils.spotify.service.SpotifyClientCredentials')

        self.mock_spotify = self.mock_spotify_patcher.start()
        self.mock_credentials = self.mock_credentials_patcher.start()

        # Configure the SpotifyClientCredentials mock
        self.mock_credentials.return_value = mock.MagicMock()

        # Configure the Spotify client mock
        self.mock_spotify_instance = self.mock_spotify.return_value

    def tearDown(self):
        self.mock_spotify_patcher.stop()
        self.mock_credentials_patcher.stop()
        super().tearDown()

    def test_search_track_with_valid_query_then_returns_results(self):
        # Configure the mock Spotify client to return search results
        mock_track = {
            ApiFields.Names.ID: "track123",
            ApiFields.Names.NAME: "Test Track",
            ApiFields.Names.POPULARITY: 85,
            ApiFields.Names.DURATION_MS: 240000,
            ApiFields.Names.ARTISTS: [
                {ApiFields.Names.ID: "artist123", ApiFields.Names.NAME: "Test Artist"}
            ],
            ApiFields.Names.ALBUM: {
                ApiFields.Names.ID: "album123",
                ApiFields.Names.NAME: "Test Album",
                "release_date": "2023-01-01"  # Using string literal as it's not in ApiFields
            }
        }

        mock_search_result = {
            ApiFields.Names.TRACKS: {
                ApiFields.Names.ITEMS: [mock_track]
            }
        }

        self.mock_spotify_instance.search.return_value = mock_search_result

        # Test the search function
        service = SpotifyAPIService()
        result = service.search_track("Test Query")

        # Verify the search was performed correctly
        self.mock_spotify_instance.search.assert_called_once_with(q="Test Query", type='track', limit=5)
        assert result == mock_search_result

    def test_search_track_with_no_results_then_returns_empty_list(self):
        # Configure the mock to return empty results
        self.mock_spotify_instance.search.return_value = {ApiFields.Names.TRACKS: {ApiFields.Names.ITEMS: []}}

        # Test the search function
        service = SpotifyAPIService()
        result = service.search_track("Nonexistent Track")

        # Verify the search was performed and returned empty results
        assert result[ApiFields.Names.TRACKS][ApiFields.Names.ITEMS] == []

    def test_search_track_with_api_error_then_raises_spotify_api_exception(self):
        # Configure the mock to raise an exception
        spotify_exception = type('SpotipyException', (Exception,), {'http_status': 500})
        self.mock_spotify_instance.search.side_effect = spotify_exception("API error")

        # Test the search function raises the appropriate exception
        service = SpotifyAPIService()
        with self.assertRaises(SpotifyNetworkException):
            service.search_track("Test Query")

    def test_get_track_by_id_with_valid_id_then_returns_track(self):
        # Configure the mock to return a track
        mock_track = {
            ApiFields.Names.ID: "track123",
            ApiFields.Names.NAME: "Test Track",
            ApiFields.Names.POPULARITY: 85
        }
        self.mock_spotify_instance.track.return_value = mock_track

        # Test getting a track by ID
        service = SpotifyAPIService()
        result = service.get_track_by_id("track123")

        # Verify the track was fetched correctly
        self.mock_spotify_instance.track.assert_called_once_with("track123")
        assert result == mock_track

    def test_get_track_by_id_with_nonexistent_id_then_raises_not_found_exception(self):
        # Configure the mock to raise a not found exception
        self.mock_spotify_instance.track.side_effect = SpotipyException(
            http_status=404, msg="Track not found", code=404)

        # Test getting a nonexistent track raises the appropriate exception
        service = SpotifyAPIService()
        with self.assertRaises(SpotifyResourceNotFoundException):
            service.get_track_by_id("nonexistent_track")

    def test_get_track_by_isrc_with_valid_isrc_then_returns_track(self):
        # Configure the mock to return search results
        mock_track = {
            ApiFields.Names.ID: "track123",
            ApiFields.Names.NAME: "Test Track",
            "external_ids": {"isrc": "USRC12345678"}  # Using string literal as it's not in ApiFields
        }

        mock_search_result = {
            ApiFields.Names.TRACKS: {
                ApiFields.Names.ITEMS: [mock_track]
            }
        }

        self.mock_spotify_instance.search.return_value = mock_search_result

        # Test finding a track by ISRC
        service = SpotifyAPIService()
        result = service.get_track_by_isrc("USRC12345678")

        # Verify the search was performed correctly
        self.mock_spotify_instance.search.assert_called_once_with(q="isrc:USRC12345678", type='track')

    @mock.patch('bodzify_api.utils.spotify.utils.create_spotify_track_instance_from_dict')
    def test_search_spotify_tracks_with_valid_query_then_creates_track_models(self, mock_create_track):
        # Configure mocks
        mock_track_data = {
            ApiFields.Names.ID: "track123",
            ApiFields.Names.NAME: "Test Track"
        }

        mock_search_result = {
            ApiFields.Names.TRACKS: {
                ApiFields.Names.ITEMS: [mock_track_data]
            }
        }

        self.mock_spotify_instance.search.return_value = mock_search_result

        # Create a mock track instance
        mock_track_instance = mock.MagicMock(spec=SpotifyTrack)
        mock_create_track.return_value = mock_track_instance

        # Test the function
        # Use the user instance created in AppTestCase.setUp
        result = search_spotify_tracks(self.test_user1, "Test Query")

        # Verify correct behavior
        self.mock_spotify_instance.search.assert_called_once()
        mock_create_track.assert_called_once_with("track123", mock_track_data)
        assert len(result) == 1
        assert result[0] == mock_track_instance

    @mock.patch('bodzify_api.utils.spotify.utils.create_spotify_track_instance_from_dict')
    @mock.patch('bodzify_api.model.spotify_resource.children.track.SpotifyTrack.SpotifyTrack.objects.get')
    def test_get_or_create_spotify_track_with_existing_track_then_returns_existing_track(
            self, mock_track_get, mock_create_track):
        # Configure mock to return an existing track
        mock_track = mock.MagicMock(spec=SpotifyTrack)
        mock_track_get.return_value = mock_track

        # Test the function
        # Use the user instance created in AppTestCase.setUp
        result = get_or_create_spotify_track(self.test_user1, "track123")

        # Verify correct behavior
        mock_track_get.assert_called_once_with(spotify_id="track123")
        mock_create_track.assert_not_called()
        assert result == mock_track

    @mock.patch('bodzify_api.utils.spotify.utils.create_spotify_track_instance_from_dict')
    @mock.patch('bodzify_api.model.spotify_resource.children.track.SpotifyTrack.SpotifyTrack.objects.get')
    def test_get_or_create_spotify_track_with_new_track_then_creates_and_returns_track(
            self, mock_track_get, mock_create_track):
        # Configure mocks
        from django.core.exceptions import ObjectDoesNotExist
        mock_track_get.side_effect = ObjectDoesNotExist()

        mock_track_data = {
            ApiFields.Names.ID: "track123",
            ApiFields.Names.NAME: "Test Track"
        }
        self.mock_spotify_instance.track.return_value = mock_track_data

        mock_track = mock.MagicMock(spec=SpotifyTrack)
        mock_create_track.return_value = mock_track

        # Test the function
        # Use the user instance created in AppTestCase.setUp
        result = get_or_create_spotify_track(self.test_user1, "track123")

        # Verify correct behavior
        mock_track_get.assert_called_once_with(spotify_id="track123")
        self.mock_spotify_instance.track.assert_called_once_with("track123")
        mock_create_track.assert_called_once_with("track123", mock_track_data)
        assert result == mock_track
