from rest_framework import status
from django.http import HttpResponse
from django.urls import reverse

from bodzify_api.test.utils.AppTestCase import AppTestCase
from bodzify_api.model.spotify.children.track.SpotifyLibTrack import SpotifyLibTrack


class SpotifyLibTrackTestCase(AppTestCase[SpotifyLibTrack]):
    def _list_spotify_lib_tracks(self, **kwargs) -> HttpResponse:
        response = self.api_client.get(reverse('spotify-lib-track-list'), kwargs)
        if response.status_code == status.HTTP_200_OK:
            self.results = response.json()['results']
            self.results_overall_total = response.json()['count']
        return response

    def _retrieve_spotify_lib_track(self, spotify_id: str) -> HttpResponse:
        return self.api_client.get(reverse('spotify-lib-track-detail', kwargs={'pk': spotify_id}))
