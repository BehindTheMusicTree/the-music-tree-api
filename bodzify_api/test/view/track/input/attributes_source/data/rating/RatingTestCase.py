#!/usr/bin/env python

import pytest
from bodzify_api.test import conftest
from bodzify_api.serializer.track.input.endpoint.post import FIELDS as POST_FIELDS
from rest_framework import status

from bodzify_api.test.view.track.TrackTestCase import TrackTestCase
from bodzify_api.test.view.track.input.attributes_source.data.FieldFromDataTestCase import FieldIntFromDataTestCase


class RatingTestCase(FieldIntFromDataTestCase):
    post_field_key = POST_FIELDS.RATING

    def test_value_then_ok(self):
        value = 1
        data = {POST_FIELDS.RATING: value}
        response = self.post_lib_track_with_generic_sample_no_tags(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.rating == value

    def test_empty_then_none(self):
        data = {POST_FIELDS.RATING: ""}
        response = self.post_lib_track_with_generic_sample_1_star(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.rating == None
