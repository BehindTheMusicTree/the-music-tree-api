from uuid import UUID

from django.urls import reverse

from bodzify_api.model.playlist.children.manual.ManualPlaylist import ManualPlaylist
from bodzify_api.test.ApiTestCase import ApiTestCase


class ManualPlaylistTestCase(ApiTestCase):
    saved_object: ManualPlaylist
    model_class = ManualPlaylist

    def _post_manual_playlist(self, **kwargs):
        return self.api_client.post(
            path=reverse('manual-playlist-list'),
            data=kwargs,
            content_type='application/json',
            handle_response=self._set_results
        )

    def _retrieve_manual_playlist(self, uuid):
        return self.api_client.get(
            path=reverse('manual-playlist-detail', kwargs={'pk': uuid}),
            handle_response=self._set_results
        )

    def _get_manual_playlists(self, **kwargs):
        return self.api_client.get(
            path=reverse('manual-playlist-list'),
            data=kwargs,
            handle_response=self._set_results
        )

    def _put_manual_playlist(self, uuid: UUID, **kwargs):
        return self.api_client.put(
            path=reverse('manual-playlist-detail', kwargs={'pk': uuid}),
            data=kwargs,
            content_type='application/json',
            handle_response=self._set_results
        )

    def _delete_manual_playlist(self, uuid):
        return self.api_client.delete(path=reverse('manual-playlist-detail', kwargs={'pk': uuid}))
