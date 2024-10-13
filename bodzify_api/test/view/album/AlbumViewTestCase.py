#!/usr/bin/env python

from django.urls import reverse
from rest_framework import status

from bodzify_api.test.AppTestCase import AppTestCase


class AlbumViewTestCase(AppTestCase):

    def _delete(self, album_uuid: str):
        return self.api_client.delete(path=reverse('album-detail', kwargs={'pk': album_uuid}))

    def _get(self):
        response = self.api_client.get(path=reverse('album-list'))
        if response.status_code == status.HTTP_200_OK:
            self._set_results_attributes(response)
        return response

    def _retrieve(self, album_uuid: str):
        response = self.api_client.get(path=reverse('album-detail', kwargs={'pk': album_uuid}))
        return response
