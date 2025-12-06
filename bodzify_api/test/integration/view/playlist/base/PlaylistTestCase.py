from uuid import UUID

from django.urls import reverse

from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.test.utils.AppTestCase import AppTestCase


class PlaylistTestCase(AppTestCase[Playlist]):
    model_class = Playlist
    saved_object: Playlist

    def _post_playlist(self, **kwargs):
        return self.api_client.post(path=reverse('playlist-list'),
                                    data=kwargs,
                                    content_type='application/json',
                                    handle_response=self._set_results)

    def _get_playlists(self, **kwargs):
        return self.api_client.get(path=reverse('playlist-list'), data=kwargs, handle_response=self._set_results)

    def _retrieve_playlist(self, uuid: UUID):
        return self.api_client.get(
            path=reverse('playlist-detail', kwargs={'pk': uuid}), handle_response=self._set_results)

    def _put_playlist(self, uuid: UUID, **kwargs):
        return self.api_client.put(path=reverse('playlist-detail', kwargs={'pk': uuid}),
                                   data=kwargs,
                                   content_type='application/json',
                                   handle_response=self._set_results)

    def _delete_playlist(self, uuid: UUID):
        return self.api_client.delete(path=reverse('playlist-detail', kwargs={'pk': uuid}))
