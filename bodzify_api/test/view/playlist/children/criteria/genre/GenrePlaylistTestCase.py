from uuid import UUID

from django.urls import reverse

from bodzify_api.model.playlist.children.criteria.genre.GenrePlaylist import GenrePlaylist
from bodzify_api.test.ApiTestCase import ApiTestCase


class GenrePlaylistTestCase(ApiTestCase):
    model_class = GenrePlaylist
    saved_object: GenrePlaylist

    def _post_genre_playlist(self, **kwargs):
        return self.api_client.post(
            path=reverse('genre-playlist-list'),
            data=kwargs,
            content_type='application/x-www-form-urlencoded',
            handle_response=self._set_results
        )

    def _retrieve_genre_playlist(self, uuid):
        return self.api_client.get(
            path=reverse('genre-playlist-detail', kwargs={'pk': uuid}),
            handle_response=self._set_results
        )

    def _get_genre_playlists(self, **kwargs):
        return self.api_client.get(
            path=reverse('genre-playlist-list'),
            data=kwargs,
            handle_response=self._set_results
        )

    def _put_genre_playlist(self, uuid: UUID, **kwargs):
        return self.api_client.put(
            path=reverse('genre-playlist-detail', kwargs={'pk': uuid}),
            data=kwargs,
            content_type='application/x-www-form-urlencoded',
            handle_response=self._set_results
        )

    def _delete_genre_playlist(self, uuid):
        return self.api_client.delete(path=reverse('genre-playlist-detail', kwargs={'pk': uuid}))
