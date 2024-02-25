#!/usr/bin/env python

from rest_framework import status
from ddf import G
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.serializer.track.input.schema.LibTrackSchemaPutSerializer import \
    FIELDS as PUT_FIELDS
from bodzify_api.test.view.ModelStringAttributePutTestCase import ModelStringAttributePutViewTestCase


class TestCase(ModelStringAttributePutViewTestCase):

    def test_not_provided_then_unchanged(self):
        rap_criteria = G(Criteria, name="Rap")
        lib_track = G(LibraryTrack,
                      user=self.test_user,
                      title="Love",
                      genre=rap_criteria,
                      duration=0)
        response = self.put_lib_track(lib_track.uuid, data_json={})
        assert response.status_code == status.HTTP_200_OK
        updated_lib_track = LibraryTrack.objects.get(uuid=lib_track.uuid)
        assert updated_lib_track.genre == rap_criteria

    def test_ok_when_updating_to_not_none(self):
        rap_criteria = G(Criteria, name="Rap")
        lib_track = G(LibraryTrack,
                      user=self.test_user,
                      title="koko",
                      genre=rap_criteria,
                      duration=0)
        rock_criteria = G(Criteria, name="Rock")
        data = {
            PUT_FIELDS.GENRE_NAME: rock_criteria.name
        }
        response = self.put_lib_track(lib_track_uuid=lib_track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.saved_lib_track.genre == rock_criteria

    def test_empty_then_none(self):
        rap_criteria = G(Criteria, name="Rap")
        lib_track = G(LibraryTrack,
                      user=self.test_user,
                      title="koko",
                      genre=rap_criteria,
                      duration=0)
        data = {
            PUT_FIELDS.GENRE_NAME: ''
        }
        response = self.put_lib_track(lib_track_uuid=lib_track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.saved_lib_track.genre == None
