#!/usr/bin/env python
import pytest
from rest_framework import status

from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase


@pytest.mark.django_db
class TestCase(ApiViewTestCase):

    def test_none_then_none(self):
        response = self.post_sample_track("no rating.mp3")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_track.rating == None

    def test_0Then0(self):
        response = self.post_sample_track("no star.mp3")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_track.rating == 0

    def test_0AndHalfThen1(self):
        response = self.post_sample_track("0 5 star.mp3")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_track.rating == 1

    def test_1_then_2(self):
        response = self.post_sample_track("1 star.mp3")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_track.rating == 2

    def test_1AndHalfThen3(self):
        response = self.post_sample_track("1 5 stars.mp3")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_track.rating == 3

    def test_2_then_4(self):
        response = self.post_sample_track("2 stars.mp3")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_track.rating == 4

    def test_2AndHalfThen5(self):
        response = self.post_sample_track("2 5 stars.mp3")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_track.rating == 5

    def test_3_then_6(self):
        response = self.post_sample_track("3 stars.mp3")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_track.rating == 6

    def test_3AndHalfThen7(self):
        response = self.post_sample_track("3 5 stars.mp3")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_track.rating == 7

    def test_4_then_8(self):
        response = self.post_sample_track("4 stars.mp3")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_track.rating == 8

    def test_4AndHalfThen9(self):
        response = self.post_sample_track("4 5 stars.mp3")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_track.rating == 9

    def test_5_then_10(self):
        response = self.post_sample_track("5 stars.mp3")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_track.rating == 10
