from uuid import UUID
from django.urls import reverse
from rest_framework import status

from bodzify_api.test.ApiTestCase import ApiTestCase


class GenrePlaylistTestCase(ApiTestCase):

    def _post_genre_playlist(self, **kwargs):
        return self.api_client.post(
            path=reverse('genre-playlist-list'),
            data=kwargs,
            content_type='application/x-www-form-urlencoded',
            on_success=self._set_result,
            on_bad_request=self._set_bad_request_result
        )

    def _retrieve_genre_playlist(self, uuid):
        return self.api_client.get(
            path=reverse('genre-playlist-detail', kwargs={'pk': uuid}),
            on_success=self._set_result,
            on_bad_request=self._set_bad_request_result
        )

    def _get_genre_playlists(self, **kwargs):
        return self.api_client.get(
            path=reverse('genre-playlist-list'),
            data=kwargs,
            on_success=self._set_results_attributes,
            on_bad_request=self._set_bad_request_result
        )

    def _put_genre_playlist(self, uuid: UUID, **kwargs):
        return self.api_client.put(
            path=reverse('genre-playlist-detail', kwargs={'pk': uuid}),
            data=kwargs,
            content_type='application/x-www-form-urlencoded',
            on_success=self._set_result,
            on_bad_request=self._set_bad_request_result
        )

    def _delete_genre_playlist(self, uuid):
        return self.api_client.delete(path=reverse('genre-playlist-detail', kwargs={'pk': uuid}))
