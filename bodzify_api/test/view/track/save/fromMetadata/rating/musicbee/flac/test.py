#!/usr/bin/env python
import pytest
from rest_framework import status
from bodzify_api.test.view.track.ApiViewTestCase import ApiViewTestCase


@pytest.mark.django_db
class TestCase(ApiViewTestCase):

    def test_NoneThenNone(self):
        response = self.postSampleTrack("no rating.flac")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedTrack.rating == None

    def test_0Then0(self):
        response = self.postSampleTrack("no star.flac")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedTrack.rating == 0

    def test_0AndHalfThen1(self):
        response = self.postSampleTrack("0 5 star.flac")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedTrack.rating == 1

    def test_1Then2(self):
        response = self.postSampleTrack("1 star.flac")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedTrack.rating == 2

    def test_1AndHalfThen3(self):
        response = self.postSampleTrack("1 5 stars.flac")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedTrack.rating == 3

    def test_2Then4(self):
        response = self.postSampleTrack("2 stars.flac")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedTrack.rating == 4

    def test_2AndHalfThen5(self):
        response = self.postSampleTrack("2 5 stars.flac")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedTrack.rating == 5

    def test_3Then6(self):
        response = self.postSampleTrack("3 stars.flac")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedTrack.rating == 6

    def test_3AndHalfThen7(self):
        response = self.postSampleTrack("3 5 stars.flac")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedTrack.rating == 7

    def test_4Then8(self):
        response = self.postSampleTrack("4 stars.flac")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedTrack.rating == 8

    def test_4AndHalfThen9(self):
        response = self.postSampleTrack("4 5 stars.flac")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedTrack.rating == 9

    def test_5Then10(self):
        response = self.postSampleTrack("5 stars.flac")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.savedTrack.rating == 10
