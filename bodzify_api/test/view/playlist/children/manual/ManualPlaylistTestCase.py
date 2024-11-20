from urllib.parse import urlencode
from uuid import UUID

from django.urls import reverse
from rest_framework import status

from bodzify_api.model.playlist.children.manual.ManualPlaylist import ManualPlaylist
from bodzify_api.serializer.schema.model.playlist.children.manual.output.detailed import Fields as ManualPlaylistGetFields
from bodzify_api.test.ApiTestCase import ApiTestCase


class ManualPlaylistTestCase(ApiTestCase):
    saved_manual_playlist: ManualPlaylist

    def _set_saved_manual_playlist_attribute(self, response):
        uuid = response.json()[ManualPlaylistGetFields.UUID]
        self.saved_manual_playlist = ManualPlaylist.objects.get(uuid=uuid)

    def _post_manual_playlist(self, **kwargs):
        data_url_encoded = urlencode(replace_none_values_by_empty_string(**kwargs), doseq=True)
        response = self.api_client.post(path=reverse('manual-playlist-list'),
                                        data=data_url_encoded,
                                        content_type='application/x-www-form-urlencoded')
        if response.status_code == status.HTTP_201_CREATED:
            self._set_saved_manual_playlist_attribute(response)
        return response

    def _retrieve_manual_playlist(self, uuid):
        response = self.api_client.get(path=reverse('manual-playlist-detail', kwargs={'pk': uuid}))
        if response.status_code == status.HTTP_200_OK:
            self._set_saved_manual_playlist_attribute(response)
        return response

    def _get_manual_playlists(self, **kwargs):
        response = self.api_client.get(path=reverse('manual-playlist-list'), data=kwargs)
        if response.status_code == status.HTTP_200_OK:
            self._set_results_attributes(response)
        return response

    def _put_manual_playlist(self, uuid: UUID, **kwargs):
        data_url_encoded = urlencode(query=replace_none_values_by_empty_string(**kwargs), doseq=True)
        response = self.api_client.put(path=reverse('manual-playlist-detail', kwargs={'pk': uuid}),
                                       data=data_url_encoded,
                                       content_type='application/x-www-form-urlencoded')
        if response.status_code == status.HTTP_200_OK:
            self._set_saved_manual_playlist_attribute(response)
        return response

    def _delete_manual_playlist(self, uuid):
        return self.api_client.delete(path=reverse('manual-playlist-detail', kwargs={'pk': uuid}))
