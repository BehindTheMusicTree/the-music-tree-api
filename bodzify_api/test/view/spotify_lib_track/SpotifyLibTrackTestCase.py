
from django.urls import reverse

from bodzify_api.model.spotify.children.track.SpotifyLibTrack import SpotifyLibTrack
from bodzify_api.test.utils.AppTestCase import AppTestCase


class SpotifyLibTrackTestCase(AppTestCase[SpotifyLibTrack]):
    saved_object: SpotifyLibTrack
    model_class = SpotifyLibTrack

    def _list_spotify_lib_tracks(self, **kwargs):
        return self.api_client.get(
            path=reverse('spotify-lib-track-list'),
            data=kwargs)

    def _retrieve_spotify_lib_track(self, spotify_id: str):
        return self.api_client.get(
            path=reverse('spotify-lib-track-detail', kwargs={'pk': spotify_id}))
