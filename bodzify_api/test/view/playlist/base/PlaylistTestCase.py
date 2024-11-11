from urllib.parse import urlencode
from uuid import UUID

from django.urls import reverse
from rest_framework import status

from bodzify_api.test.ApiTestCase import ApiTestCase


class PlaylistTestCase(ApiTestCase):

    def _post_playlist(self, **kwargs):
        data_url_encoded = urlencode(self._replace_none_values_by_empty_string(kwargs), doseq=True)
        response = self.api_client.post(path=reverse('playlist-list'),
                                        data=data_url_encoded,
                                        content_type='application/x-www-form-urlencoded')
        if response.status_code == status.HTTP_201_CREATED:
            self._set_result(response)
        return response

    def _get_playlists(self, **kwargs):
        response = self.api_client.get(path=reverse('playlist-list'),
                                       data=self._replace_none_values_by_empty_string(kwargs))
        if response.status_code == status.HTTP_200_OK:
            self._set_results_attributes(response)
        return response

    def _retrieve_playlist(self, uuid: UUID):
        response = self.api_client.get(path=reverse('playlist-detail', kwargs={'pk': uuid}))
        if response.status_code == status.HTTP_200_OK:
            self._set_result(response=response)
        return response

    def _put_playlist(self, uuid: UUID, **kwargs):
        data_url_encoded = urlencode(self._replace_none_values_by_empty_string(kwargs), doseq=True)
        response = self.api_client.put(path=reverse('playlist-detail', kwargs={'pk': uuid}),
                                       data=data_url_encoded,
                                       content_type='application/x-www-form-urlencoded')
        if response.status_code == status.HTTP_200_OK:
            self._set_result(response)
        return response

    def _delete_playlist(self, uuid: UUID):
        return self.api_client.delete(path=reverse('playlist-detail', kwargs={'pk': uuid}))
