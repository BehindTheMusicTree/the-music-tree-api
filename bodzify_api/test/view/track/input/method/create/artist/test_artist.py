#!/usr/bin/env python
from rest_framework import status
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase


class TestCase(ApiViewTestCase):

    def test_not_provided_then_none(self):
        response = self.post_lib_track_with_specific_sample(specific_sample_filename="notProvided.mp3", data_json={})
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.artist == None
