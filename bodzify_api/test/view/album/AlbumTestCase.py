from uuid import UUID
from django.urls import reverse
from rest_framework import status

from bodzify_api.test.ApiTestCase import ApiTestCase


class AlbumTestCase(ApiTestCase):

    def _post_album(self, **kwargs):
        return self.api_client.post(
            path=reverse('album-list'),
            data=kwargs,
            content_type='application/x-www-form-urlencoded',
            on_success=self._set_result,
            on_bad_request=self._set_bad_request_result
        )

    def _get_albums(self, **kwargs):
        return self.api_client.get(
            path=reverse('album-list'),
            data=kwargs,
            on_success=self._set_results_attributes,
            on_bad_request=self._set_bad_request_result
        )

    def _retrieve_album(self, uuid: UUID):
        return self.api_client.get(
            path=reverse('album-detail', kwargs={'pk': uuid}),
            on_success=self._set_result,
            on_bad_request=self._set_bad_request_result
        )

    def _put_album(self, uuid: UUID, **kwargs):
        return self.api_client.put(
            path=reverse('album-detail', kwargs={'pk': uuid}),
            data=kwargs,
            content_type='application/x-www-form-urlencoded',
            on_success=self._set_result,
            on_bad_request=self._set_bad_request_result
        )

    def _delete_album(self, uuid: UUID):
        return self.api_client.delete(path=reverse('album-detail', kwargs={'pk': uuid}))
