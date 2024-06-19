#!/usr/bin/env python

from urllib.parse import urlencode

from django.urls import reverse
from rest_framework import status

from bodzify_api.model.playlist.children.SimplePlaylist import SimplePlaylist
from bodzify_api.test.AppTestCase import AppTestCase
from bodzify_api.serializer.playlist.children.simple.output.with_tracks \
    import FIELDS as SIMPLE_PLAYLIST_GET_FIELDS


class SimplePlaylistTestCase(AppTestCase):
    saved_simple_playlist: SimplePlaylist

    def _set_saved_simple_playlist_attribute(self, response):
        uuid = response.json()[SIMPLE_PLAYLIST_GET_FIELDS.UUID]
        self.saved_simple_playlist = SimplePlaylist.objects.get(base_playlist__uuid=uuid)

    def post_simple_playlist(self, data_dict):
        data_url_encoded = urlencode(self._replace_none_values_by_empty_string(data_dict), doseq=True)
        response = self.api_client.post(path=reverse('simple-playlist-list'),
                                        data=data_url_encoded,
                                        content_type='application/x-www-form-urlencoded')
        if response.status_code == status.HTTP_201_CREATED:
            self._set_saved_simple_playlist_attribute(response)
        return response

    def put_simple_playlist(self, simple_playlist_uuid: str, data_dict):
        data_url_encoded = urlencode(query=self._replace_none_values_by_empty_string(data_dict), doseq=True)
        response = self.api_client.put(path=reverse('simple-playlist-detail', kwargs={'pk': simple_playlist_uuid}),
                                       data=data_url_encoded,
                                       content_type='application/x-www-form-urlencoded')
        if response.status_code == status.HTTP_200_OK:
            self._set_saved_simple_playlist_attribute(response)
        return response
