#!/usr/bin/env python

from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.criteria.CriteriaType import CRITERIA_TYPES_ID
from bodzify_api.serializer.track.input.endpoint.LibTrackPostSerializer import FIELDS as POST_FIELDS
from rest_framework import status
from ddf import G

from bodzify_api.test.view.track.input.source.data.FieldFromDataTestCase import NullableUuidFieldFromDataTestCase


class GenreUuidTestCase(NullableUuidFieldFromDataTestCase):
    post_field_key = POST_FIELDS.GENRE_NAME

    def test_non_existing_uuid_then_error(self):
        data = {POST_FIELDS.GENRE_UUID: 'a' * 22}
        response = self.post_lib_track_with_generic_sample_no_tags(data_dict=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST  # type: ignore

    def test_value_then_ok(self):
        genre_name = "Rock"
        genre_uuid = G(Criteria, user=self.test_user, type=CRITERIA_TYPES_ID.GENRE,
                       name=genre_name).uuid  # type: ignore
        data = {POST_FIELDS.GENRE_UUID: genre_uuid}
        response = self.post_lib_track_with_generic_sample_no_tags(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED  # type: ignore
        assert self.saved_lib_track.genre.name == genre_name  # type: ignore

    def test_empty_then_none(self):
        data = {POST_FIELDS.GENRE_UUID: ''}
        response = self.post_lib_track_with_generic_sample_no_tags(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED  # type: ignore
        assert self.saved_lib_track.genre == None
