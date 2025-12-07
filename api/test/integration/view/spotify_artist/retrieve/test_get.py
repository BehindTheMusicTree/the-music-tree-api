from uuid import uuid4
from rest_framework import status

from api.model.spotify_resource.children.artist.Fields import Fields
from api.test.integration.view.spotify_artist.SpotifyArtistTestCase import SpotifyArtistTestCase
from api.utils.data_transformer import to_camel_case


class TestGet(SpotifyArtistTestCase):
    def setUp(self):
        super().setUp()
        self.artist = self.model_fixture_factory.create_spotify_artist(
            name='Test Artist',
            popularity=90,
            genres=[Fields.GENRES],
            images=[{'url': 'https://example.com/image.jpg', 'height': 640, 'width': 640}]
        )

    def test_retrieve_spotify_artist_then_ok(self):
        response = self._retrieve_spotify_artist(self.artist.spotify_id)
        assert response.status_code == status.HTTP_200_OK
        result = self.result
        assert result[Fields.NAME] == self.artist.name
        assert result[Fields.POPULARITY] == self.artist.popularity
        assert result[to_camel_case(Fields.SPOTIFY_LINK)] == self.artist.spotify_link
        assert Fields.GENRES in result
        assert result[Fields.GENRES] == self.artist.genres
        assert result[Fields.IMAGES] == self.artist.images

    def test_retrieve_spotify_artist_with_invalid_id_then_404_not_found(self):
        response = self._retrieve_spotify_artist(str(uuid4()))
        assert response.status_code == status.HTTP_404_NOT_FOUND
