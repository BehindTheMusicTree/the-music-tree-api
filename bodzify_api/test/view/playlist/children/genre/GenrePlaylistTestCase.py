from uuid import UUID
from django.urls import reverse
from rest_framework import status

from bodzify_api.test.ApiTestCase import ApiTestCase


class GenrePlaylistTestCase(ApiTestCase):

    def _post_genre_playlist(self, **kwargs):
        response = self.api_client.post(path=reverse('genre-playlist-list'),
                                        data=kwargs,
                                        content_type='application/x-www-form-urlencoded')
        if response.status_code == status.HTTP_201_CREATED:
            self._set_result(response)
        return response

    def _retrieve_genre_playlist(self, uuid):
        return self.api_client.get(path=reverse('genre-playlist-detail', kwargs={'pk': uuid}))

    def _get_genre_playlists(self, **kwargs):
        response = self.api_client.get(path=reverse('genre-playlist-list'), data=kwargs)
        if response.status_code == status.HTTP_200_OK:
            self._set_results_attributes(response)
        return response

    def _put_genre_playlist(self, manual_playlist_uuid: UUID, **kwargs):
        response = self.api_client.put(path=reverse('genre-playlist-detail', kwargs={'pk': manual_playlist_uuid}),
                                       data=kwargs,
                                       content_type='application/x-www-form-urlencoded')
        return response

    def _delete_genre_playlist(self, uuid):
        return self.api_client.delete(path=reverse('genre-playlist-detail', kwargs={'pk': uuid}))
