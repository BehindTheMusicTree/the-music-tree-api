#!/usr/bin/env python
import pytest
from rest_framework import status
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase


@pytest.mark.django_db
class TestCase(TrackViewTestCase):

    def test_None(self):
        response = self.postSampleTrack("no rating.flac")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedTrack.rating == None

    def test_1Then2(self):
        response = self.postSampleTrack("1 star.flac")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedTrack.rating == 2
    
    def test_2Then4(self):
        response = self.postSampleTrack("2 stars.flac")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedTrack.rating == 4
    
    def test_3Then6(self):
        response = self.postSampleTrack("3 stars.flac")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedTrack.rating == 6

    def test_4Then8(self):
        response = self.postSampleTrack("4 stars.flac")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedTrack.rating == 8

    def test_5Then10(self):
        response = self.postSampleTrack("5 stars.flac")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedTrack.rating == 10
