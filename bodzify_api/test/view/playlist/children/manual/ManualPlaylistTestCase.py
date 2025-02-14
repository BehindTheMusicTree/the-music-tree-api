from uuid import UUID

from django.urls import reverse

from bodzify_api.model.playlist.children.manual.ManualPlaylist import ManualPlaylist
from bodzify_api.serializer.schema.model.playlist.children.manual.output.detailed import Fields as ManualPlaylistGetFields
from bodzify_api.test.ApiTestCase import ApiTestCase


class ManualPlaylistTestCase(ApiTestCase):
    saved_manual_playlist: ManualPlaylist

    def _set_saved_manual_playlist_attribute(self, response):
        uuid = response.json()[ManualPlaylistGetFields.UUID]
        self.saved_manual_playlist = ManualPlaylist.objects.get(uuid=uuid)

    def _post_manual_playlist(self, **kwargs):
        return self.api_client.post(
            path=reverse('manual-playlist-list'),
            data=kwargs,
            content_type='application/json',
            on_success=self._set_saved_manual_playlist_attribute,
            on_bad_request=self._set_bad_request_result
        )

    def _retrieve_manual_playlist(self, uuid):
        return self.api_client.get(
            path=reverse('manual-playlist-detail', kwargs={'pk': uuid}),
            on_success=self._set_saved_manual_playlist_attribute,
            on_bad_request=self._set_bad_request_result
        )

    def _get_manual_playlists(self, **kwargs):
        return self.api_client.get(
            path=reverse('manual-playlist-list'),
            data=kwargs,
            on_success=self._set_results_attributes,
            on_bad_request=self._set_bad_request_result
        )

    def _put_manual_playlist(self, uuid: UUID, **kwargs):
        return self.api_client.put(
            path=reverse('manual-playlist-detail', kwargs={'pk': uuid}),
            data=kwargs,
            content_type='application/json',
            on_success=self._set_saved_manual_playlist_attribute,
            on_bad_request=self._set_bad_request_result
        )

    def _delete_manual_playlist(self, uuid):
        return self.api_client.delete(path=reverse('manual-playlist-detail', kwargs={'pk': uuid}))
