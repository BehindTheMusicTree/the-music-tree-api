#!/usr/bin/env python

import logging
from typing import Optional
from django.urls import get_resolver

from django.urls import reverse
from rest_framework import status

import bodzify_api.audiometadata as audiometadata
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.playlist.children.SimplePlaylist import SimplePlaylist
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.test.AppTestCase import AppTestCase
from bodzify_api.view.viewset.model.AppModelViewSet import PAGINATED_RESPONSE_FIELDS
from bodzify_api.serializer.track.input.endpoint.LibTrackExtractSerializer import FIELDS as LIB_TRACK_EXTRACT_FIELDS
from bodzify_api.serializer.track.input.endpoint.LibTrackPostSerializer import FIELDS as LIB_TRACK_POST_FIELDS
from bodzify_api.serializer.track.output.LibTrackDetailedSerializer import FIELDS as LIB_TRACK_GET_FIELDS
from bodzify_api.serializer.playlist.children.simple.output.SimplePlaylistWithTracksSerializer \
    import FIELDS as SIMPLE_PLAYLIST_GET_FIELDS


class SearchTestCase(AppTestCase):

    def search(self, query):
        response = self.api_client.get(path=reverse('search-list'), data={'query': query})
        if response.status_code == status.HTTP_200_OK:
            self._set_results_attributes(response)
        return response
