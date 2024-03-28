#!/usr/bin/env python

import logging
from django.urls import get_resolver

from django.urls import reverse
from rest_framework import status

from bodzify_api.model.playlist.children.SimplePlaylist import SimplePlaylist
from bodzify_api.test.ApiTestCase import ApiTestCase
from bodzify_api.serializer.playlist.children.simple.output.SimplePlaylistWithTracksSerializer \
    import FIELDS as SIMPLE_PLAYLIST_GET_FIELDS


logger = logging.getLogger('bodzify_api')


class SimplePlaylistTestCase(ApiTestCase):
    saved_simple_playlist: SimplePlaylist

    def _set_saved_simple_playlist_attribute(self, response):
        uuid = response.json()[SIMPLE_PLAYLIST_GET_FIELDS.UUID]
        self.saved_simple_playlist = SimplePlaylist.objects.get(playlist__uuid=uuid)

    def post_simple_playlist(self, data_dict):
        response = self.api_client.post(path=reverse('simple-playlist-list'),
                                        data=self._replace_none_values_by_empty_string(data_dict),
                                        format='json')
        if response.status_code == status.HTTP_201_CREATED:  # type: ignore
            self._set_saved_simple_playlist_attribute(response)
        return response

    def put_simple_playlist(self, simple_playlist_uuid: str, data_dict):
        response = self.api_client.put(
            path=reverse('simple-playlist-detail', kwargs={'pk': simple_playlist_uuid}),
            data=self._replace_none_values_by_empty_string(data_dict),
            format='json')
        if response.status_code == status.HTTP_200_OK:  # type: ignore
            self._set_saved_simple_playlist_attribute(response)
        return response
