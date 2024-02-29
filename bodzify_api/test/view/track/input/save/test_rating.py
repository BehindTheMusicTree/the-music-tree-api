#!/usr/bin/env python

from rest_framework import status
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase
from bodzify_api.serializer.track.input.schema.LibTrackPostSchemaSerializer import FIELDS as POST_FIELDS


class TestCase(ApiViewTestCase):

    def test_empty_then_none(self):
        data = {
            POST_FIELDS.RATING: ''
        }
        response = self.post_lib_track_with_generic_sample_no_tags(data_json=data)
        assert response.status_code == status.HTTP_201_CREATED  # type: ignore
        assert self.saved_lib_track.rating == None

    def test_zero(self):
        rating = 0
        data = {
            POST_FIELDS.RATING: rating
        }
        response = self.post_lib_track_with_generic_sample_no_tags(data_json=data)
        assert response.status_code == status.HTTP_201_CREATED  # type: ignore
        assert self.saved_lib_track.rating == rating

    def test_four(self):
        rating = 4
        data = {
            POST_FIELDS.RATING: rating
        }
        response = self.post_lib_track_with_generic_sample_no_tags(data_json=data)
        assert response.status_code == status.HTTP_201_CREATED  # type: ignore
        assert self.saved_lib_track.rating == rating

    def test_ten(self):
        rating = 10
        data = {
            POST_FIELDS.RATING: rating
        }
        response = self.post_lib_track_with_generic_sample_no_tags(data_json=data)
        assert response.status_code == status.HTTP_201_CREATED  # type: ignore
        assert self.saved_lib_track.rating == rating

    def test_error_when_above_maximum(self):
        data = {
            POST_FIELDS.RATING: 11,
        }
        response = self.post_lib_track_with_generic_sample_no_tags(data_json=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST  # type: ignore

    def test_error_when_below_minimum(self):
        data = {
            POST_FIELDS.RATING: -1,
        }
        response = self.post_lib_track_with_generic_sample_no_tags(data_json=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST  # type: ignore

    def test_error_when_not_integer(self):
        data = {
            POST_FIELDS.RATING: 5.5,
        }
        response = self.post_lib_track_with_generic_sample_no_tags(data_json=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST  # type: ignore
