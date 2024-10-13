#!/usr/bin/env python

from rest_framework import status

from bodzify_api.test.view.track.TrackTestCase import TrackTestCase


class TestCase(TrackTestCase):

    def test_wav(self):
        response = self.extract_default_mine_track(extension='wav')
        assert response.status_code == status.HTTP_201_CREATED

    def test_mp3(self):
        response = self.extract_default_mine_track(extension='mp3')
        assert response.status_code == status.HTTP_201_CREATED
