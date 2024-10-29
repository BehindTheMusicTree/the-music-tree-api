#!/usr/bin/env python

from uuid import UUID
from django.urls import reverse
from rest_framework import status

from bodzify_api.test.ApiTestCase import ApiTestCase


class AlbumTestCase(ApiTestCase):

    def _delete_album(self, album_uuid: UUID):
        return self.api_client.delete(path=reverse('album-detail', kwargs={'pk': album_uuid}))

    def _get_albums(self, **kwargs):
        response = self.api_client.get(path=reverse('album-list'), data=kwargs)
        if response.status_code == status.HTTP_200_OK:
            self._set_results_attributes(response)
        return response

    def _retrieve_album(self, album_uuid: UUID):
        response = self.api_client.get(path=reverse('album-detail', kwargs={'pk': album_uuid}))
        if response.status_code == status.HTTP_200_OK:
            self._set_result(response)
        return response
