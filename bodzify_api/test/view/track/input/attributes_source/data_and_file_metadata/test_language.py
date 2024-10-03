#!/usr/bin/env python

from rest_framework import status
from bodzify_api.test.view.track.TrackTestCase import TrackTestCase
from bodzify_api.serializer.track.input.endpoint.post import Fields as PostFields


class TestCase(TrackTestCase):

    def test_title_in_both_then_take_data(self):
        data_language = "fr"
        data_dict = {PostFields.LANGUAGE: data_language}
        response = self.post_lib_track_with_generic_sample_tags_max_length_of_a(data_dict=data_dict)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.lib_track_saved.language == data_language
