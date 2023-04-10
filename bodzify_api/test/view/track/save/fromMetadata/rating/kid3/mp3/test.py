#!/usr/bin/env python
import pytest
from rest_framework import status
from bodzify_api.test.view.track.ApiViewTestCase import ApiViewTestCase


@pytest.mark.django_db
class TestCase(ApiViewTestCase):

    def test_None(self):
        response = self.postSampleTrack("no rating.mp3")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedTrack.rating == None

    def test_1Then2(self):
        response = self.postSampleTrack("1 star.mp3")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedTrack.rating == 2

    def test_2Then4(self):
        response = self.postSampleTrack("2 stars.mp3")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedTrack.rating == 4

    def test_3Then6(self):
        response = self.postSampleTrack("3 stars.mp3")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedTrack.rating == 6

    def test_4Then8(self):
        response = self.postSampleTrack("4 stars.mp3")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedTrack.rating == 8

    def test_5Then10(self):
        response = self.postSampleTrack("5 stars.mp3")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedTrack.rating == 10
