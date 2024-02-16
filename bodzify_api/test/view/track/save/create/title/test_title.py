#!/usr/bin/env python
from rest_framework import status
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase


class TestCase(ApiViewTestCase):

    def test_not_povided_then_set_from_filename(self):
        filename_without_extension = "notTooLongFilename"
        response = self.post_sample_track(
            sample_filename=filename_without_extension + ".mp3", data_json={})
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_track.title == filename_without_extension
