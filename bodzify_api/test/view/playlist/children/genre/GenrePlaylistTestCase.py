#!/usr/bin/env python

import logging
from typing import Optional
from django.urls import get_resolver

from django.urls import reverse
from rest_framework import status

from bodzify_api import AudioMetadataManager
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.playlist.children.SimplePlaylist import SimplePlaylist
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.test.ApiTestCase import ApiTestCase
from bodzify_api.test.AppTestCase import AppTestCase
from bodzify_api.view.viewset.model.AppModelViewSet import PAGINATED_RESPONSE_FIELDS
from bodzify_api.serializer.track.output.LibTrackDetailedSerializer import FIELDS as LIB_TRACK_GET_FIELDS
from bodzify_api.serializer.playlist.children.simple.output.SimplePlaylistWithTracksSerializer \
    import FIELDS as SIMPLE_PLAYLIST_GET_FIELDS


logger = logging.getLogger('bodzify_api')


class GenrePlaylistTestCase(ApiTestCase):

    def retrieve_genre_playlist(self, playlist_uuid):
        return self.api_client.get(path=reverse('genre-playlist-detail', kwargs={'pk': playlist_uuid}))

    def get_genre_playlists(self, data_dict=None):
        response = self.api_client.get(
            path=reverse('genre-playlist-list'),
            data=self._replace_none_values_by_empty_string(data_dict))
        if response.status_code == status.HTTP_200_OK:  # type: ignore
            self._set_results_attributes(response)
        return response
