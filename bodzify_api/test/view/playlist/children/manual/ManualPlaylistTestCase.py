
from urllib.parse import urlencode
from uuid import UUID

from django.urls import reverse
from rest_framework import status

from bodzify_api.model.playlist.children.manual.ManualPlaylist import ManualPlaylist
from bodzify_api.serializer.schema.playlist.children.simple.output.detailed import Fields as ManualPlaylistGetFields
from bodzify_api.test.ApiTestCase import ApiTestCase


class ManualPlaylistTestCase(ApiTestCase):
    saved_manual_playlist: ManualPlaylist

    def _set_saved_manual_playlist_attribute(self, response):
        uuid = response.json()[ManualPlaylistGetFields.UUID]
        self.saved_manual_playlist = ManualPlaylist.objects.get(uuid=uuid)

    def _post_manual_playlist(self, data_dict):
        data_url_encoded = urlencode(self._replace_none_values_by_empty_string(data_dict), doseq=True)
        response = self.api_client.post(path=reverse('manual-playlist-list'),
                                        data=data_url_encoded,
                                        content_type='application/x-www-form-urlencoded')
        if response.status_code == status.HTTP_201_CREATED:
            self._set_saved_manual_playlist_attribute(response)
        return response

    def _put_manual_playlist(self, manual_playlist_uuid: UUID, data_dict):
        data_url_encoded = urlencode(query=self._replace_none_values_by_empty_string(data_dict), doseq=True)
        response = self.api_client.put(path=reverse('manual-playlist-detail', kwargs={'pk': manual_playlist_uuid}),
                                       data=data_url_encoded,
                                       content_type='application/x-www-form-urlencoded')
        if response.status_code == status.HTTP_200_OK:
            self._set_saved_manual_playlist_attribute(response)
        return response
