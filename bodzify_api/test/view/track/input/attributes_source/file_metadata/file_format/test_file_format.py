#!/usr/bin/env python

import pytest
from rest_framework import status

from bodzify_api.test.view.track.TrackTestCase import TrackTestCase


@pytest.mark.django_db
class TestCase(TrackTestCase):

    def test_flac(self):
        response = self._post_lib_track_with_specific_sample("sample.flac")
        assert response.status_code == status.HTTP_201_CREATED

    def test_mp3(self):
        response = self._post_lib_track_with_specific_sample("sample.mp3")
        assert response.status_code == status.HTTP_201_CREATED

    def test_wav(self):
        response = self._post_lib_track_with_specific_sample("sample.wav")
        assert response.status_code == status.HTTP_201_CREATED
