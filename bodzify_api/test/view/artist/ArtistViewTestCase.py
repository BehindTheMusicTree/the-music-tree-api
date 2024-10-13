#!/usr/bin/env python

from django.urls import reverse
from rest_framework import status

from bodzify_api.test.AppTestCase import AppTestCase


class ArtistViewTestCase(AppTestCase):

    def _delete(self, artistUuid: str):
        return self.api_client.delete(path=reverse('artist-detail', kwargs={'pk': artistUuid}))

    def _get(self):
        response = self.api_client.get(path=reverse('album-list'))
        if response.status_code == status.HTTP_200_OK:
            self._set_results_attributes(response)
        return response

    def _retrieve(self, artistUuid: str):
        return self.api_client.get(path=reverse('artist-detail', kwargs={'pk': artistUuid}))
