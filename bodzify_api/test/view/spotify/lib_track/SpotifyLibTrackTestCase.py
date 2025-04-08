from django.http import HttpResponse
from django.urls import reverse

from bodzify_api.test.utils.AppTestCase import AppTestCase
from bodzify_api.model.spotify.children.track.SpotifyLibTrack import SpotifyLibTrack


class SpotifyLibTrackTestCase(AppTestCase[SpotifyLibTrack]):
    def _list_spotify_lib_tracks(self, **kwargs) -> HttpResponse:
        return self.api_client.get(reverse('spotify-lib-track-list'), data=kwargs, handle_response=self._set_results)

    def _retrieve_spotify_lib_track(self, spotify_id: str) -> HttpResponse:
        return self.api_client.get(
            reverse('spotify-lib-track-detail', kwargs={'pk': spotify_id}),
            handle_response=self._set_results)
