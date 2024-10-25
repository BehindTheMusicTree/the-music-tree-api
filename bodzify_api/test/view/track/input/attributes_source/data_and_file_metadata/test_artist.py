#!/usr/bin/env python

from rest_framework import status

from bodzify_api.model.Artist import Artist
from bodzify_api.serializer.schema.track.input.endpoint.post import Fields as PostFields
from bodzify_api.test.view.track.TrackTestCase import TrackTestCase


class TestCase(TrackTestCase):

    def test_artist_in_both_then_take_data(self):
        data_artist_name = "Rock"
        data_dict = {PostFields.ARTISTS_NAMES: data_artist_name}
        response = self._post_lib_track_with_generic_sample_tags_max_length_of_a(data_dict=data_dict)
        assert response.status_code == status.HTTP_201_CREATED
        artists_list: list[Artist] = list(self.saved_lib_track.artists.all())
        assert len(artists_list) > 0
        assert artists_list[0].name == data_artist_name
