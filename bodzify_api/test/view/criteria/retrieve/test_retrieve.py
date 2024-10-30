#!/usr/bin/env python


from rest_framework import status

from bodzify_api.serializer.schema.criteria.output.fields import Fields as RetrieveFields
from bodzify_api.test.view.criteria.CriteriaTestCase import CriteriaTestCase
from bodzify_api.utils.utils import to_camel_case


class TestCase(CriteriaTestCase):

    def test_name(self):
        name = 'rock'
        uuid = self.model_fixture_factory.create_genre(name=name).uuid
        response = self._retrieve_genre(uuid=uuid)
        assert response.status_code == status.HTTP_200_OK
        assert self.result[RetrieveFields.NAME] == name

    def test_lib_tracks(self):
        criteria = self.model_fixture_factory.create_genre(name='rock')

        title1 = 'stylax'
        track1_uuid = self.model_fixture_factory.create_lib_track_with_file(title=title1, genre=criteria).uuid

        title2 = 'bien'
        track2_uuid = self.model_fixture_factory.create_lib_track_with_file(title=title2, genre=criteria).uuid

        response = self._retrieve_genre(uuid=criteria.uuid)
        assert response.status_code == status.HTTP_200_OK
        lib_tracks = self.result[to_camel_case(RetrieveFields.LIB_TRACKS)]
        assert len(lib_tracks) == 2
        titles = [track[RetrieveFields.LIB_TRACKS_TITLE] for track in lib_tracks]
        assert title1 in titles
        assert title2 in titles
        uuids = [track[RetrieveFields.UUID] for track in lib_tracks]
        assert track1_uuid in uuids
        assert track2_uuid in uuids
