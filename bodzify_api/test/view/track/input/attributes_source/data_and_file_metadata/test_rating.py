#!/usr/bin/env python

from rest_framework import status

from bodzify_api.test.view.track.TrackTestCase import TrackTestCase
from bodzify_api.serializer.track.input.endpoint.post import Fields as PostFields


class TestCase(TrackTestCase):

    def test_rating_in_both_then_take_data(self):
        data_rating = 7
        data_dict = {PostFields.RATING: data_rating}
        response = self.post_lib_track_with_generic_sample_1_star(data_dict=data_dict)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.rating == data_rating
