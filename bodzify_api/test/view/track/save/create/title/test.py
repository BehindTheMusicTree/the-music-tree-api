#!/usr/bin/env python
from rest_framework import status
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase


class TestCase(ApiViewTestCase):

    def test_notProvidedThenSetFromFilename(self):
        filenameWithoutExtension = "notTooLongFilename"
        response = self.post_sample_track(
            sample_filename=filenameWithoutExtension + ".mp3", data_json={})
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedTrack.title == filenameWithoutExtension
