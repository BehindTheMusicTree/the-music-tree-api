#!/usr/bin/env python

from rest_framework import status
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.serializer.track.input.endpoint.put import Fields as PutFields
from bodzify_api.test.view.track.input.method.put.NullableFieldTestCase import NullableFieldTestCase
from bodzify_api.model.criteria.CriteriaType import CriteriaTypesId


class TestCase(NullableFieldTestCase):

    def test_not_provided_then_unchanged(self):
        rap_criteria = self.model_fixture_factory.create_genre(name="Rap")
        lib_track = self.model_fixture_factory.create_lib_track(title="Love", genre=rap_criteria)
        response = self.put_lib_track(lib_track.uuid, data_dict={})
        assert response.status_code == status.HTTP_200_OK
        updated_lib_track = LibraryTrack.objects.get(uuid=lib_track.uuid)
        assert updated_lib_track.genre == rap_criteria

    def test_ok_when_updating_to_not_none(self):
        rap_criteria = self.model_fixture_factory.create_genre(name="Rap")
        lib_track = self.model_fixture_factory.create_lib_track(title="koko", genre=rap_criteria)
        rock_criteria = self.model_fixture_factory.create_genre(name="Rock")
        data = {PutFields.GENRE_NAME: rock_criteria.name}
        response = self.put_lib_track(lib_track_uuid=lib_track.uuid, data_dict=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.saved_lib_track.genre == rock_criteria

    def test_empty_then_none(self):
        rap_criteria = self.model_fixture_factory.create_genre(name="Rap")
        lib_track = self.model_fixture_factory.create_lib_track(title="koko", genre=rap_criteria)
        data = {PutFields.GENRE_NAME: ''}
        response = self.put_lib_track(lib_track_uuid=lib_track.uuid, data_dict=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.saved_lib_track.genre == None

    def test_not_none_then_update(self):
        genre_name = "rap"
        lib_track = self.model_fixture_factory.create_lib_track(title='lolo')
        data = {PutFields.GENRE_NAME: genre_name}
        response = self.put_lib_track(lib_track.uuid, data_dict=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.saved_lib_track.genre is not None
        assert self.saved_lib_track.genre.name == genre_name
