#!/usr/bin/env python

from rest_framework import status
from bodzify_api.test.view.track.TrackTestCase import TrackTestCase


class TestCase(TrackTestCase):

    def test_not_povided_then_none(self):
        response = self.post_lib_track_with_generic_sample_no_tags()
        assert response.status_code == status.HTTP_201_CREATED
        assert self.lib_track_saved.language == None
