#!/usr/bin/env python
import pytest
from rest_framework import status

from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase


@pytest.mark.django_db
class TestCase(ApiViewTestCase):

    def test_none(self):
        response = self.post_sample_track("no rating.mp3")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_track.rating == None

    def test_1Then2(self):
        response = self.post_sample_track("1 star.mp3")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_track.rating == 2

    def test_2Then4(self):
        response = self.post_sample_track("2 stars.mp3")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_track.rating == 4

    def test_3Then6(self):
        response = self.post_sample_track("3 stars.mp3")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_track.rating == 6

    def test_4Then8(self):
        response = self.post_sample_track("4 stars.mp3")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_track.rating == 8

    def test_5Then10(self):
        response = self.post_sample_track("5 stars.mp3")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_track.rating == 10
