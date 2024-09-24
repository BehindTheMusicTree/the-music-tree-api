#!/usr/bin/env python

import logging
from rest_framework import status

from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.criteria.CriteriaType import CriteriaTypesId
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.serializer.criteria.output.detailed import Fields as RETRIEVE_FIELDS
from bodzify_api.test.view.criteria.CriteriaTestCase import CriteriaTestCase
from bodzify_api.utils.utils import to_camel_case


class TestCase(CriteriaTestCase):

    def test_name(self):
        name = 'rock'
        uuid = self.model_fixture_factory.create_genre(name=name).uuid
        response = self.retrieve_genre(uuid=uuid)
        assert response.status_code == status.HTTP_200_OK
        assert self.result[RETRIEVE_FIELDS.NAME] == name

    def test_lib_tracks(self):
        criteria = self.model_fixture_factory.create_genre(name='rock')

        title1 = 'stylax'
        track1_uuid = self.model_fixture_factory.create_lib_track(title=title1, genre=criteria).uuid

        title2 = 'bien'
        track2_uuid = self.model_fixture_factory.create_lib_track(title=title2, genre=criteria).uuid

        response = self.retrieve_genre(uuid=criteria.uuid)
        assert response.status_code == status.HTTP_200_OK
        lib_tracks = self.result[to_camel_case(RETRIEVE_FIELDS.LIB_TRACKS)]
        assert len(lib_tracks) == 2
        titles = [track[RETRIEVE_FIELDS.LIB_TRACKS_TITLE] for track in lib_tracks]
        assert title1 in titles
        assert title2 in titles
        uuids = [track[RETRIEVE_FIELDS.UUID] for track in lib_tracks]
        assert track1_uuid in uuids
        assert track2_uuid in uuids
