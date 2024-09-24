#!/usr/bin/env python

from rest_framework import status
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.criteria.CriteriaType import CriteriaTypesId
from bodzify_api.test.view.track.TrackTestCase import TrackTestCase
from bodzify_api.serializer.track.input.endpoint.post import Fields as POST_FIELDS


class TestCase(TrackTestCase):

    def test_genre_name_in_both_then_take_data(self):
        data_genre_name = "Rock"
        data_dict = {POST_FIELDS.GENRE_NAME: data_genre_name}
        response = self.post_lib_track_with_generic_sample_tags_max_length_of_a(data_dict=data_dict)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.genre is not None
        assert self.saved_lib_track.genre.name == data_genre_name

    def test_genre_uuid_in_data_and_genre_name_in_matadata_then_take_data(self):
        data_genre_name = "Rock"
        genre_uuid = self.model_fixture_factory.create_genre(name=data_genre_name).uuid
        data_dict = {POST_FIELDS.GENRE_UUID: genre_uuid}
        response = self.post_lib_track_with_generic_sample_tags_max_length_of_a(data_dict=data_dict)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.genre is not None
        assert self.saved_lib_track.genre.name == data_genre_name
