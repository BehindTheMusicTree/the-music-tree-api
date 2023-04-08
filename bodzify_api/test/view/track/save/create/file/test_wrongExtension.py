#!/usr/bin/env python
import pytest
from rest_framework import status
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase


@pytest.mark.django_db
class ExtensionTestCase(TrackViewTestCase):

    def test_jpeg(self):
        response = self.postSampleTrack("image.jpeg")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_mp4(self):
        response = self.postSampleTrack("bad_extension.mp4")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
