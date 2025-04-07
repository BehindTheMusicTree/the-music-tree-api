from uuid import uuid4
from rest_framework import status

from bodzify_api.test.view.spotify_lib_track.SpotifyLibTrackTestCase import SpotifyLibTrackTestCase
from bodzify_api.serializer.model.spotify.lib_track.output.Fields import Fields as SerializerFields


class TestGet(SpotifyLibTrackTestCase):
    def setUp(self):
        super().setUp()
        self.track = self.model_fixture_factory.create_spotify_lib_track(
            name="Test Track",
            duration_ms=300000,
            popularity=80,
            album={"name": "Test Album"},
            preview_url="https://example.com/preview",
            explicit=True
        )

    def test_retrieve_spotify_lib_track_then_ok(self):
        response = self._retrieve_spotify_lib_track(self.track.spotify_id)
        assert response.status_code == status.HTTP_200_OK
        result = response.json()

        # Test all fields from the model
        assert result[SerializerFields.SPOTIFY_ID] == self.track.spotify_id
        assert result[SerializerFields.NAME] == self.track.name
        assert result[SerializerFields.DURATION_MS] == self.track.duration_ms
        assert result[SerializerFields.DURATION_STR_IN_HOUR_MIN_SEC] == self.track.duration_str_in_hour_min_sec
        assert result[SerializerFields.POPULARITY] == self.track.popularity
        assert result[SerializerFields.SPOTIFY_LINK] == self.track.spotify_link
        assert result[SerializerFields.ALBUM] == self.track.album
        assert result[SerializerFields.PREVIEW_URL] == self.track.preview_url
        assert result[SerializerFields.EXPLICIT] == self.track.explicit
        assert result[SerializerFields.SPOTIFY_ARTISTS] == []
        assert result[SerializerFields.CREATED_ON] is not None
        assert result[SerializerFields.UPDATED_ON] is not None
        assert result[SerializerFields.LAST_SYNCED_AT] is None
        assert result[SerializerFields.IS_REMOVED] is False
        assert 'genres' in result
        assert result['genres'] == []

    def test_retrieve_spotify_lib_track_with_invalid_id_then_404_not_found(self):
        response = self._retrieve_spotify_lib_track(str(uuid4()))
        assert response.status_code == status.HTTP_404_NOT_FOUND
