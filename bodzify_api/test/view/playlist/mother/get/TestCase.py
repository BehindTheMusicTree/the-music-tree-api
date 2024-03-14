#!/usr/bin/env python

import logging
from rest_framework import status
from ddf import G

from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.criteria.CriteriaType import CRITERIA_TYPES_ID
from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.model.playlist.children.CriteriaPlaylist import TYPES_LABEL as CRITERIA_PLAYLIST_TYPES_LABEL, \
    SPECIAL_NAMES as CRITERIA_PLAYLIST_SPECIAL_NAMES
from bodzify_api.model.playlist.children.SimplePlaylist \
    import SimplePlaylist, SPECIAL_NAMES as SIMPLE_PLAYLIST_SPECIAL_NAMES
from bodzify_api.serializer.playlist.mother.input.PlaylistQueryParamSerializer import FIELDS as GET_QUERY_FIELDS
from bodzify_api.serializer.playlist.mother.output.PlaylistWithTracksSerializer import FIELDS as GET_RESULT_FIELDS
from bodzify_api.test.view.GetFilterTestCase import GetFilterTestCase

logger = logging.getLogger('bodyzify_api')


class TestCase(GetFilterTestCase):
    filter_field = GET_QUERY_FIELDS.NAME

    def test_filter_is_empty_then_results(self):
        rock_criteria_name = "Rock"
        G(Criteria, user=self.test_user, name=rock_criteria_name, type=CRITERIA_TYPES_ID.GENRE)

        simple_playlist_name = "Teuf"
        G(SimplePlaylist, playlist__user=self.test_user, name=simple_playlist_name)

        data_dict = {
            self.filter_field: ''
        }
        response = self.get_playlists(data_dict=data_dict)
        assert response.status_code == status.HTTP_200_OK  # type: ignore
        assert len(self.results) == 0

    def test_filter_is_not_provided_then_results(self):
        rock_criteria_name = "Rock"
        G(Criteria, user=self.test_user, name=rock_criteria_name, type=CRITERIA_TYPES_ID.GENRE)

        simple_playlist_name = "Teuf"
        G(SimplePlaylist, playlist__user=self.test_user, name=simple_playlist_name)

        response = self.get_playlists()
        assert response.status_code == status.HTTP_200_OK  # type: ignore
        assert len(self.results) == Playlist.objects.filter(user=self.test_user).count()
