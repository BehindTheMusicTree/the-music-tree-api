#!/usr/bin/env python

from rest_framework import status

from bodzify_api.serializer.track.input.endpoint.post import \
    Fields as PostFields
from bodzify_api.test.view.track.input.attributes_source.data.FieldFromDataTestCase import \
    FieldIntFromDataTestCase


class RatingTestCase(FieldIntFromDataTestCase):
    post_field_key = PostFields.RATING

    def test_value_then_ok(self):
        value = 1
        data = {PostFields.RATING: value}
        response = self.post_lib_track_with_generic_sample_no_tags(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.lib_track_saved.rating == value

    def test_empty_then_none(self):
        data = {PostFields.RATING: ""}
        response = self.post_lib_track_with_generic_sample_1_star(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.lib_track_saved.rating == None
