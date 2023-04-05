#!/usr/bin/env python
import pytest
from rest_framework import status
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase


@pytest.mark.django_db
class NoneTestCase(TrackViewTestCase):

    def test_flac(self):
        response = self.postSampleTrack("sample.flac")
        assert response.status_code == status.HTTP_201_CREATED

    def test_mp3(self):
        response = self.postSampleTrack("sample.mp3")
        assert response.status_code == status.HTTP_201_CREATED

    def test_wav(self):
        response = self.postSampleTrack("sample.wav")
        assert response.status_code == status.HTTP_201_CREATED
