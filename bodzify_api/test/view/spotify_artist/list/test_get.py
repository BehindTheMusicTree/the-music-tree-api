from rest_framework import status

from bodzify_api.model.spotify.children.artist.Fields import Fields
from bodzify_api.test.view.spotify_artist.SpotifyArtistTestCase import SpotifyArtistTestCase


class TestGet(SpotifyArtistTestCase):
    def setUp(self):
        super().setUp()
        self.artist1 = self.model_fixture_factory.create_spotify_artist(
            name='Artist 1',
            popularity=90,
            genres=[Fields.GENRES],
            images=[{'url': 'https://example.com/image1.jpg', 'height': 640, 'width': 640}]
        )
        self.artist2 = self.model_fixture_factory.create_spotify_artist(
            name='Artist 2',
            popularity=80,
            genres=[Fields.GENRES],
            images=[{'url': 'https://example.com/image2.jpg', 'height': 640, 'width': 640}]
        )

    def test_list_spotify_artists_then_ok(self):
        response = self._list_spotify_artists()
        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 2

        # Test first artist
        artist1_result = self.results[0]
        assert artist1_result[Fields.NAME] == self.artist1.name
        assert artist1_result[Fields.POPULARITY] == self.artist1.popularity
        assert artist1_result[Fields.SPOTIFY_LINK] == self.artist1.spotify_link
        assert Fields.GENRES in artist1_result
        assert artist1_result[Fields.GENRES] == self.artist1.genres
        assert artist1_result[Fields.IMAGES] == self.artist1.images
        assert artist1_result[Fields.CREATED_ON] is not None
        assert artist1_result[Fields.UPDATED_ON] is not None

        # Test second artist
        artist2_result = self.results[1]
        assert artist2_result[Fields.NAME] == self.artist2.name
        assert artist2_result[Fields.POPULARITY] == self.artist2.popularity
        assert artist2_result[Fields.SPOTIFY_LINK] == self.artist2.spotify_link
        assert Fields.GENRES in artist2_result
        assert artist2_result[Fields.GENRES] == self.artist2.genres
        assert artist2_result[Fields.IMAGES] == self.artist2.images
        assert artist2_result[Fields.CREATED_ON] is not None
        assert artist2_result[Fields.UPDATED_ON] is not None
