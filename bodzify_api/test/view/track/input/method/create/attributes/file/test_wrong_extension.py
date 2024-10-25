#!/usr/bin/env python

import pytest
from rest_framework import status

from bodzify_api.test.view.track.TrackTestCase import TrackTestCase


@pytest.mark.django_db
class TestCase(TrackTestCase):

    def test_jpeg_then_error(self):
        response = self._post_lib_track_with_specific_sample("image.jpeg")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_mp4_then_error(self):
        response = self._post_lib_track_with_specific_sample("bad_extension.mp4")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
