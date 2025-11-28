from uuid import uuid4
from rest_framework import status

from bodzify_api.test.view.spotify_lib_track.SpotifyLibTrackTestCase import SpotifyLibTrackTestCase
from bodzify_api.serializer.model.spotify.lib_track.output.Fields import Fields as SerializerFields
from bodzify_api.model.spotify_resource.children.track.Fields import Fields as ModelFields
from bodzify_api.utils.data_transformer import to_camel_case


class TestGet(SpotifyLibTrackTestCase):
    def setUp(self):
        super().setUp()
        genres_artist1 = ["Rock", "Pop"]
        genres_artist2 = ["Jazz", "Blues", "Pop"]
        self.spotify_artist1 = self.model_fixture_factory.create_spotify_artist(
            name="Test Artist 1",
            genres=genres_artist1
        )
        self.spotify_artist_2 = self.model_fixture_factory.create_spotify_artist(
            name="Test Artist 2",
            genres=genres_artist2
        )
        self.track = self.model_fixture_factory.create_spotify_lib_track(
            name="Test Track",
            duration_ms=300000,
            popularity=80,
            spotify_artists=[self.spotify_artist1, self.spotify_artist_2],
            album={ModelFields.NAME: "Test Album"},
            preview_url="https://example.com/preview",
            explicit=True
        )

    def test_retrieve_spotify_lib_track_then_ok(self):
        artists = self.track.spotify_artists.all()
        artist1 = artists[0]
        response = self._retrieve_spotify_lib_track(self.track.spotify_id)
        assert response.status_code == status.HTTP_200_OK
        result = response.json()

        # Test all fields from the model
        assert result[to_camel_case(SerializerFields.SPOTIFY_ID)] == self.track.spotify_id
        assert result[to_camel_case(SerializerFields.NAME)] == self.track.name
        assert result[to_camel_case(SerializerFields.DURATION_MS)] == self.track.duration_ms
        assert result[to_camel_case(SerializerFields.DURATION_STR_IN_HOUR_MIN_SEC)] == self.track.duration_str_in_hour_min_sec
        assert result[to_camel_case(SerializerFields.POPULARITY)] == self.track.popularity
        assert result[to_camel_case(SerializerFields.SPOTIFY_LINK)] == self.track.spotify_link
        assert result[to_camel_case(SerializerFields.ALBUM)] == self.track.album[ModelFields.NAME]
        assert result[to_camel_case(SerializerFields.PREVIEW_URL)] == self.track.preview_url
        assert result[to_camel_case(SerializerFields.EXPLICIT)] == self.track.explicit
        assert result[to_camel_case(SerializerFields.IS_REMOVED)] is False

        # Test spotify_artists field
        spotify_artists = result[to_camel_case(SerializerFields.SPOTIFY_ARTISTS)]
        assert len(spotify_artists) == 2

        # Test first artist
        artist1 = spotify_artists[0]
        assert artist1[to_camel_case(SerializerFields.SPOTIFY_ID)] == self.spotify_artist1.spotify_id
        assert artist1[to_camel_case(SerializerFields.NAME)] == self.spotify_artist1.name
        assert artist1[to_camel_case(SerializerFields.GENRES)] == self.spotify_artist1.genres

        # Test second artist
        artist2 = spotify_artists[1]
        assert artist2[to_camel_case(SerializerFields.SPOTIFY_ID)] == self.spotify_artist_2.spotify_id
        assert artist2[to_camel_case(SerializerFields.NAME)] == self.spotify_artist_2.name
        assert artist2[to_camel_case(SerializerFields.GENRES)] == self.spotify_artist_2.genres

        assert sorted(result[to_camel_case(SerializerFields.GENRES)]) == sorted(["Rock", "Pop", "Jazz", "Blues"])

    def test_retrieve_spotify_lib_track_with_invalid_id_then_404_not_found(self):
        response = self._retrieve_spotify_lib_track(str(uuid4()))
        assert response.status_code == status.HTTP_404_NOT_FOUND
