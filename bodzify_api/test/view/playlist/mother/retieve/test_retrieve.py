#!/usr/bin/env python

import logging
from rest_framework import status
from ddf import G

from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.criteria.CriteriaType import CRITERIA_TYPES_ID
from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.model.playlist.children.SimplePlaylist \
    import SimplePlaylist, SPECIAL_NAMES as SIMPLE_PLAYLIST_SPECIAL_NAMES
from bodzify_api.model.playlist.children.CriteriaPlaylist import SPECIAL_NAMES as CRITERIA_PLAYLIST_SPECIAL_NAMES
from bodzify_api.serializer.playlist.mother.output.PlaylistWithTracksSerializer import FIELDS as RETRIEVE_FIELDS
from bodzify_api.test.ApiTestCase import ApiTestCase
from bodzify_api.test.get_filters.GetFilterWithFreeValuesTestCase import GetFilterWithFreeValuesTestCase

logger = logging.getLogger('bodyzify_api')


class TestCase(ApiTestCase):

    def test_retrieve_simple_then_ok(self):
        simple_playlist_uuid = G(SimplePlaylist, playlist__user=self.test_user,
                                 name='cuisine').playlist.uuid  # type: ignore

        response = self.retrieve_playlist(uuid=simple_playlist_uuid)
        assert response.status_code == status.HTTP_200_OK  # type: ignore
        assert self.result[RETRIEVE_FIELDS.UUID] == simple_playlist_uuid
