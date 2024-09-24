#!/usr/bin/env python

from rest_framework import status
from bodzify_api.test.view.track.TrackTestCase import TrackTestCase
from bodzify_api.serializer.track.input.endpoint.post import Fields as POST_FIELDS


class TestCase(TrackTestCase):

    def test_artist_in_both_then_take_data(self):
        data_artist_name = "Rock"
        data_dict = {POST_FIELDS.ARTIST_NAME: data_artist_name}
        response = self.post_lib_track_with_generic_sample_tags_max_length_of_a(data_dict=data_dict)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.artist is not None
        assert self.saved_lib_track.artist.name == data_artist_name
