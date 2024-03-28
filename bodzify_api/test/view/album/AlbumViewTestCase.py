#!/usr/bin/env python

from django.urls import reverse
from bodzify_api.test.ApiTestCase import ApiTestCase
from rest_framework import status


class AlbumViewTestCase(ApiTestCase):

    def delete(self, album_uuid: str):
        return self.api_client.delete(path=reverse('album-detail', kwargs={'pk': album_uuid}))

    def get_albums(self):
        response = self.api_client.get(path=reverse('album-list'))
        if response.status_code == status.HTTP_200_OK:  # type: ignore
            self._set_results_attributes(response)
        return response
