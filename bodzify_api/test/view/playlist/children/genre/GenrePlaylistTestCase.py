#!/usr/bin/env python


from django.urls import reverse
from rest_framework import status

from bodzify_api.test.ApiTestCase import ApiTestCase


class GenrePlaylistTestCase(ApiTestCase):

    def retrieve_genre_playlist(self, playlist_uuid):
        return self.api_client.get(path=reverse('genre-playlist-detail', kwargs={'pk': playlist_uuid}))

    def get_genre_playlists(self, data_dict=None):
        response = self.api_client.get(
            path=reverse('genre-playlist-list'),
            data=self._replace_none_values_by_empty_string(data_dict))
        if response.status_code == status.HTTP_200_OK:
            self._set_results_attributes(response)
        return response
