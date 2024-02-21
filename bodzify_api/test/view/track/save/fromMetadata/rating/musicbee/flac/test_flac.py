#!/usr/bin/env python
import pytest
from rest_framework import status
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase


@pytest.mark.django_db
class TestCase(ApiViewTestCase):

    def test_NoneThenNone(self):
        response = self.post_sample_track("no rating.flac")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_track.rating == None

    def test_0Then0(self):
        response = self.post_sample_track("no star.flac")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_track.rating == 0

    def test_0AndHalfThen1(self):
        response = self.post_sample_track("0 5 star.flac")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_track.rating == 1

    def test_1Then2(self):
        response = self.post_sample_track("1 star.flac")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_track.rating == 2

    def test_1AndHalfThen3(self):
        response = self.post_sample_track("1 5 stars.flac")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_track.rating == 3

    def test_2Then4(self):
        response = self.post_sample_track("2 stars.flac")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_track.rating == 4

    def test_2AndHalfThen5(self):
        response = self.post_sample_track("2 5 stars.flac")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_track.rating == 5

    def test_3Then6(self):
        response = self.post_sample_track("3 stars.flac")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_track.rating == 6

    def test_3AndHalfThen7(self):
        response = self.post_sample_track("3 5 stars.flac")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_track.rating == 7

    def test_4Then8(self):
        response = self.post_sample_track("4 stars.flac")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_track.rating == 8

    def test_4AndHalfThen9(self):
        response = self.post_sample_track("4 5 stars.flac")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_track.rating == 9

    def test_5Then10(self):
        response = self.post_sample_track("5 stars.flac")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_track.rating == 10
