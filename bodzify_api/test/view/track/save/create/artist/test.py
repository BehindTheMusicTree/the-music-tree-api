#!/usr/bin/env python
from rest_framework import status
from ddf import G
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase


class TestCase(ApiViewTestCase):

    def test_not_provided_then_none(self):
        response = self.post_sample_track(sample_filename="notProvided.mp3", data_json={})
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_track.artist == None
