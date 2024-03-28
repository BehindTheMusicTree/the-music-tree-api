#!/usr/bin/env python

import logging
from rest_framework import status
from ddf import G

from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.criteria.CriteriaType import CRITERIA_TYPES_ID
from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.model.playlist.children.SimplePlaylist \
    import SimplePlaylist, SPECIAL_NAMES as SIMPLE_PLAYLIST_SPECIAL_NAMES
from bodzify_api.model.playlist.children.CriteriaPlaylist import SPECIAL_NAMES as CRITERIA_PLAYLIST_SPECIAL_NAMES, CriteriaPlaylist
from bodzify_api.serializer.playlist.mother.output.PlaylistWithTracksSerializer import FIELDS as RETRIEVE_FIELDS
from bodzify_api.test.ApiTestCase import ApiTestCase
from bodzify_api.test.get_filters.GetFilterWithFreeValuesTestCase import GetFilterWithFreeValuesTestCase

logger = logging.getLogger('bodyzify_api')


class TestCase(ApiTestCase):

    def test_retrieve_simple_then_ok(self):
        name = 'cuisine'
        playlist_uuid = G(SimplePlaylist, playlist__user=self.test_user, name=name).playlist.uuid  # type: ignore

        response = self.retrieve_playlist(uuid=playlist_uuid)
        assert response.status_code == status.HTTP_200_OK  # type: ignore
        assert self.result[RETRIEVE_FIELDS.NAME] == name

    def test_retrieve_genre_then_ok(self):
        name = 'rock'
        genre = G(Criteria, user=self.test_user, name=name, type=CRITERIA_TYPES_ID.GENRE)
        playlist_uuid = Playlist.objects.get(user=self.test_user,
                                             criteria_playlist__criteria=genre,
                                             criteria_playlist__type=CRITERIA_TYPES_ID.GENRE).uuid  # type: ignore

        response = self.retrieve_playlist(uuid=playlist_uuid)
        assert response.status_code == status.HTTP_200_OK  # type: ignore
        assert self.result[RETRIEVE_FIELDS.NAME] == name

    def test_retrieve_tag_then_ok(self):
        name = 'fr'
        genre = G(Criteria, user=self.test_user, name=name, type=CRITERIA_TYPES_ID.TAG)
        playlist_uuid = Playlist.objects.get(user=self.test_user,
                                             criteria_playlist__criteria=genre,
                                             criteria_playlist__type=CRITERIA_TYPES_ID.TAG).uuid  # type: ignore

        response = self.retrieve_playlist(uuid=playlist_uuid)
        assert response.status_code == status.HTTP_200_OK  # type: ignore
        assert self.result[RETRIEVE_FIELDS.NAME] == name
