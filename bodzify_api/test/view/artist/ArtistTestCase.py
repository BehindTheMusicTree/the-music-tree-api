
from uuid import UUID

from django.urls import reverse
from rest_framework import status

from bodzify_api.test.ApiTestCase import ApiTestCase


class ArtistTestCase(ApiTestCase):

    def _delete_artist(self, artistUuid: UUID):
        return self.api_client.delete(path=reverse('artist-detail', kwargs={'pk': artistUuid}))

    def _get_artists(self, **kwargs):
        response = self.api_client.get(path=reverse('artist-list'), data=kwargs)
        if response.status_code == status.HTTP_200_OK:
            self._set_results_attributes(response)
        return response

    def _retrieve(self, artistUuid: UUID):
        return self.api_client.get(path=reverse('artist-detail', kwargs={'pk': artistUuid}))
