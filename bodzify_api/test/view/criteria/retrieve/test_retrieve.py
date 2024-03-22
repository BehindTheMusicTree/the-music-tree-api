#!/usr/bin/env python

import logging
from rest_framework import status
from ddf import G

from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.criteria.CriteriaType import CRITERIA_TYPES_ID
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.serializer.criteria.output.CriteriaDetailedSerializer import FIELDS as RETRIEVE_FIELDS
from bodzify_api.test.ApiTestCase import ApiTestCase
from bodzify_api.utils import to_camel_case

logger = logging.getLogger('bodyzify_api')


class TestCase(ApiTestCase):

    def test_name(self):
        name = 'rock'
        uuid = G(Criteria, user=self.test_user, name=name, type=CRITERIA_TYPES_ID.GENRE).uuid  # type: ignore
        response = self.retrieve_genre(uuid=uuid)
        assert response.status_code == status.HTTP_200_OK  # type: ignore
        assert self.result[RETRIEVE_FIELDS.NAME] == name

    def test_lib_tracks(self):
        criteriaUuid = G(Criteria, user=self.test_user, name='rock', type=CRITERIA_TYPES_ID.GENRE).uuid  # type: ignore

        title1 = 'stylax'
        track1Uuid = G(LibraryTrack, user=self.test_user, title=title1, genre=criteriaUuid).uuid  # type: ignore

        title2 = 'bien'
        track2Uuid = G(LibraryTrack, user=self.test_user, title=title2, genre=criteriaUuid).uuid  # type: ignore

        response = self.retrieve_genre(uuid=criteriaUuid)
        assert response.status_code == status.HTTP_200_OK  # type: ignore
        print(self.result)
        lib_tracks = self.result[to_camel_case(RETRIEVE_FIELDS.LIB_TRACKS)]
        assert len(lib_tracks) == 2
        titles = [track[RETRIEVE_FIELDS.LIB_TRACKS_TITLE] for track in lib_tracks]
        assert title1 in titles
        assert title2 in titles
        uuids = [track[RETRIEVE_FIELDS.UUID] for track in lib_tracks]
        assert track1Uuid in uuids
        assert track2Uuid in uuids
