#!/usr/bin/env python
from rest_framework import status
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase


class TestCase(ApiViewTestCase):

    def test_not_povided_then_none(self):
        response = self.post_lib_track_with_specific_sample(specific_sample_filename="not_provided.mp3", data_json={})
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.language == None
