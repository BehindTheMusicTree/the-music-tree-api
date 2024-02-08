#!/usr/bin/env python
from rest_framework import status
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase


class TestCase(ApiViewTestCase):

    def test_notProvidedThenNone(self):
        response = self.post_sample_track(sample_filename="notProvided.mp3", data_json={})
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedTrack.genre == None
