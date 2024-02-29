#!/usr/bin/env python

from rest_framework import status
from ddf import G
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.serializer.track.input.schema.LibTrackPutSchemaSerializer import FIELDS as PUT_FIELDS
from bodzify_api.test.view.track.input.method.put.FieldTestCase import FieldTestCase
from bodzify_api.model.criteria.CriteriaType import CRITERIA_TYPES_ID


class TestCase(FieldTestCase):

    def test_not_provided_then_unchanged(self):
        rap_criteria = G(Criteria, user=self.test_user, type=CRITERIA_TYPES_ID.GENRE, name="Rap")
        lib_track = G(LibraryTrack,
                      user=self.test_user,
                      title="Love",
                      genre=rap_criteria,
                      duration=0)
        response = self.put_lib_track(lib_track.uuid, data_json={})  # type: ignore
        assert response.status_code == status.HTTP_200_OK  # type: ignore
        updated_lib_track = LibraryTrack.objects.get(uuid=lib_track.uuid)  # type: ignore
        assert updated_lib_track.genre == rap_criteria

    def test_ok_when_updating_to_not_none(self):
        rap_criteria = G(Criteria, user=self.test_user, type=CRITERIA_TYPES_ID.GENRE, name="Rap")
        lib_track = G(LibraryTrack,
                      user=self.test_user,
                      title="koko",
                      genre=rap_criteria,
                      duration=0)
        rock_criteria = G(Criteria, user=self.test_user, type=CRITERIA_TYPES_ID.GENRE, name="Rock")
        data = {
            PUT_FIELDS.GENRE_NAME: rock_criteria.name  # type: ignore
        }
        response = self.put_lib_track(lib_track_uuid=lib_track.uuid, data_json=data)  # type: ignore
        assert response.status_code == status.HTTP_200_OK  # type: ignore
        assert self.saved_lib_track.genre == rock_criteria

    def test_empty_then_none(self):
        rap_criteria = G(Criteria, user=self.test_user, type=CRITERIA_TYPES_ID.GENRE, name="Rap")
        lib_track = G(LibraryTrack,
                      user=self.test_user,
                      title="koko",
                      genre=rap_criteria,
                      duration=0)
        data = {
            PUT_FIELDS.GENRE_NAME: ''
        }
        response = self.put_lib_track(lib_track_uuid=lib_track.uuid, data_json=data)  # type: ignore
        assert response.status_code == status.HTTP_200_OK  # type: ignore
        assert self.saved_lib_track.genre == None

    def test_not_none_then_update(self):
        genre_name = "rap"
        lib_track = G(LibraryTrack,
                      user=self.test_user,
                      title='lolo',
                      duration=0)
        data = {
            PUT_FIELDS.GENRE_NAME: genre_name
        }
        response = self.put_lib_track(lib_track.uuid, data_json=data)  # type: ignore
        assert response.status_code == status.HTTP_200_OK  # type: ignore
        assert self.saved_lib_track.genre.name == genre_name  # type: ignore
