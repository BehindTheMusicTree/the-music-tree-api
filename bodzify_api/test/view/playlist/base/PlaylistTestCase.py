from uuid import UUID

from django.urls import reverse

from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.test.ApiTestCase import ApiTestCase


class PlaylistTestCase(ApiTestCase[Playlist]):
    def _post_playlist(self, **kwargs):
        return self.api_client.post(
            path=reverse('playlist-list'),
            data=kwargs,
            content_type='application/x-www-form-urlencoded',
            handle_response=self._set_results
        )

    def _get_playlists(self, **kwargs):
        return self.api_client.get(
            path=reverse('playlist-list'),
            data=kwargs,
            handle_response=self._set_results
        )

    def _retrieve_playlist(self, uuid: UUID):
        return self.api_client.get(
            path=reverse('playlist-detail', kwargs={'pk': uuid}),
            handle_response=self._set_results
        )

    def _put_playlist(self, uuid: UUID, **kwargs):
        return self.api_client.put(
            path=reverse('playlist-detail', kwargs={'pk': uuid}),
            data=kwargs,
            content_type='application/x-www-form-urlencoded',
            handle_response=self._set_results
        )

    def _delete_playlist(self, uuid: UUID):
        return self.api_client.delete(path=reverse('playlist-detail', kwargs={'pk': uuid}))
