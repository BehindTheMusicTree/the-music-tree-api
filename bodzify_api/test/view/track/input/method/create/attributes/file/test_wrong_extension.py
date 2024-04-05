#!/usr/bin/env python

import pytest
from rest_framework import status
from bodzify_api.test.view.track.TrackTestCase import TrackTestCase


@pytest.mark.django_db
class ExtensionTestCase(TrackTestCase):

    def test_jpeg(self):
        response = self.post_lib_track_with_specific_sample("image.jpeg")
        assert response.status_code == status.HTTP_400_BAD_REQUEST  # type: ignore

    def test_mp4(self):
        response = self.post_lib_track_with_specific_sample("bad_extension.mp4")
        assert response.status_code == status.HTTP_400_BAD_REQUEST  # type: ignore
