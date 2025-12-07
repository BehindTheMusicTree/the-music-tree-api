from django.urls import reverse

from api.model.spotify_resource.children.artist.SpotifyArtist import SpotifyArtist
from api.test.utils.AppTestCase import AppTestCase


class SpotifyArtistTestCase(AppTestCase[SpotifyArtist]):
    model_class = SpotifyArtist
    saved_object: SpotifyArtist

    def _set_single_result(self, response):
        self.result = response.json()

    def _list_spotify_artists(self, **params):
        return self.api_client.get(
            path=reverse('spotify-artist-list'),
            data=params,
            handle_response=self._set_results
        )

    def _retrieve_spotify_artist(self, spotify_id: str):
        return self.api_client.get(
            path=reverse('spotify-artist-detail', kwargs={'pk': spotify_id}),
            handle_response=self._set_single_result
        )
