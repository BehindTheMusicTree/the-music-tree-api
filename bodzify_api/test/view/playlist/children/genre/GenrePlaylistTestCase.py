#!/usr/bin/env python

import logging
from typing import Optional
from django.urls import get_resolver

from django.urls import reverse
from rest_framework import status

import bodzify_api.utils.audio_metadata as audio_metadata
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.playlist.children.SimplePlaylist import SimplePlaylist
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.test.AppTestCase import AppTestCase
from bodzify_api.test.AppTestCase import AppTestCase
from bodzify_api.view.viewset.model.AppModelViewSet import PaginatedResponseFields
from bodzify_api.serializer.track.output.detailed import Fields as LibTrackGetFields
from bodzify_api.serializer.playlist.children.simple.output.with_tracks \
    import Fields as SimplePlaylistGetFields


class GenrePlaylistTestCase(AppTestCase):

    def retrieve_genre_playlist(self, playlist_uuid):
        return self.api_client.get(path=reverse('genre-playlist-detail', kwargs={'pk': playlist_uuid}))

    def get_genre_playlists(self, data_dict=None):
        response = self.api_client.get(
            path=reverse('genre-playlist-list'),
            data=self._replace_none_values_by_empty_string(data_dict))
        if response.status_code == status.HTTP_200_OK:
            self._set_results_attributes(response)
        return response
