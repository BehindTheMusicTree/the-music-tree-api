from urllib.parse import urlencode
from uuid import UUID

from django.urls import reverse
from rest_framework import status

from bodzify_api.test.ApiTestCase import ApiTestCase
from bodzify_api.utils import data_transformer


class ArtistTestCase(ApiTestCase):

    def _post_artist(self, **kwargs):
        response = self.api_client.post(path=reverse('artist-list'),
                                        data=kwargs,
                                        content_type='application/x-www-form-urlencoded')
        if response.status_code == status.HTTP_201_CREATED:
            self._set_result(response)
        return response

    def _get_artists(self, **kwargs):
        response = self.api_client.get(path=reverse('artist-list'), data=kwargs)
        if response.status_code == status.HTTP_200_OK:
            self._set_results_attributes(response)
        return response

    def _retrieve_artist(self, uuid: UUID):
        response = self.api_client.get(path=reverse('artist-detail', kwargs={'pk': uuid}))
        if response.status_code == status.HTTP_200_OK:
            self._set_result(response)
        return response

    def _put_artist(self, uuid: UUID, **kwargs):
        response = self.api_client.put(path=reverse('artist-detail', kwargs={'pk': uuid}),
                                       data=kwargs,
                                       content_type='application/x-www-form-urlencoded')
        if response.status_code == status.HTTP_200_OK:
            self._set_result(response)
        return response

    def _delete_artist(self, uuid: UUID):
        return self.api_client.delete(path=reverse('artist-detail', kwargs={'pk': uuid}))
