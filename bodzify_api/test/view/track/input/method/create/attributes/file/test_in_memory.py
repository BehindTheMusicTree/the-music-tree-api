#!/usr/bin/env python

from rest_framework import status
from bodzify_api.test.view.track.TrackTestCase import TrackTestCase


"""
Small files are handled differently by Django. They are stored in memory instead of being written to disk.
Thus the python file object is not available. This test case is to ensure that the API handles this case.
"""


class TestCase(TrackTestCase):

    def test_in_memory(self):
        response = self.post_lib_track_with_specific_sample("in_memory.flac")
        assert response.status_code == status.HTTP_201_CREATED  # type: ignore
