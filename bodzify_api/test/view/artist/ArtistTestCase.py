from uuid import UUID

from django.urls import reverse
from rest_framework import status

from bodzify_api.test.ApiTestCase import ApiTestCase


class ArtistTestCase(ApiTestCase):

    def _post_artist(self, **kwargs):
        return self.api_client.post(
            path=reverse('artist-list'),
            data=kwargs,
            content_type='application/x-www-form-urlencoded',
            on_success=self._set_result
        )

    def _get_artists(self, **kwargs):
        return self.api_client.get(
            path=reverse('artist-list'),
            data=kwargs,
            on_success=self._set_results_attributes
        )

    def _retrieve_artist(self, uuid: UUID):
        return self.api_client.get(
            path=reverse('artist-detail', kwargs={'pk': uuid}),
            on_success=self._set_result
        )

    def _put_artist(self, uuid: UUID, **kwargs):
        return self.api_client.put(
            path=reverse('artist-detail', kwargs={'pk': uuid}),
            data=kwargs,
            content_type='application/x-www-form-urlencoded',
            on_success=self._set_result
        )

    def _delete_artist(self, uuid: UUID):
        return self.api_client.delete(path=reverse('artist-detail', kwargs={'pk': uuid}))
