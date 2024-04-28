#!/usr/bin/env python


from django.urls import reverse
from rest_framework import status

from bodzify_api.test.AppTestCase import AppTestCase


class PlaylistTestCase(AppTestCase):

    def retrieve_playlist(self, uuid: str):
        response = self.api_client.get(path=reverse('playlist-detail', kwargs={'pk': uuid}))
        if response.status_code == status.HTTP_200_OK:
            self._set_result(response=response)
        return response

    def get_playlists(self, data_dict=None):
        response = self.api_client.get(path=reverse('playlist-list'),
                                       data=self._replace_none_values_by_empty_string(data_dict))
        if response.status_code == status.HTTP_200_OK:
            self._set_results_attributes(response)
        return response
