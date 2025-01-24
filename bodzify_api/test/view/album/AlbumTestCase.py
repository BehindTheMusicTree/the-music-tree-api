from uuid import UUID
from django.urls import reverse
from rest_framework import status

from bodzify_api.test.ApiTestCase import ApiTestCase


class AlbumTestCase(ApiTestCase):

    def _post_album(self, **kwargs):
        response = self.api_client.post(path=reverse('album-list'),
                                        data=kwargs,
                                        content_type='application/x-www-form-urlencoded')
        if response.status_code == status.HTTP_201_CREATED:
            self._set_result(response)
        return response

    def _get_albums(self, **kwargs):
        response = self.api_client.get(path=reverse('album-list'), data=kwargs)
        if response.status_code == status.HTTP_200_OK:
            self._set_results_attributes(response)
        return response

    def _retrieve_album(self, uuid: UUID):
        response = self.api_client.get(path=reverse('album-detail', kwargs={'pk': uuid}))
        if response.status_code == status.HTTP_200_OK:
            self._set_result(response)
        return response

    def _put_album(self, uuid: UUID, **kwargs):
        response = self.api_client.put(path=reverse('album-detail', kwargs={'pk': uuid}),
                                       data=kwargs,
                                       content_type='application/x-www-form-urlencoded')
        if response.status_code == status.HTTP_200_OK:
            self._set_result(response)
        return response

    def _delete_album(self, uuid: UUID):
        return self.api_client.delete(path=reverse('album-detail', kwargs={'pk': uuid}))
