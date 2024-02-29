#!/usr/bin/env python

import pytest
from rest_framework import status

from bodzify_api.test.view.track.input.source.file_metadata.rating.LibraryTrackFromFileMetadataRatingWithHalfFieldTestCase \
    import LibraryTrackFromFileMetadataRatingWithHalfFieldTestCase


@pytest.mark.django_db
class TestCase(LibraryTrackFromFileMetadataRatingWithHalfFieldTestCase):

    def test_0_and_half_then_1(self):
        response = self.post_lib_track_with_specific_sample("0 5 star.wav")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.rating == 1

    def test_1_then_2(self):
        response = self.post_lib_track_with_specific_sample("1 star.wav")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.rating == 2

    def test_1_and_half_then_3(self):
        response = self.post_lib_track_with_specific_sample("1 5 stars.wav")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.rating == 3

    def test_2_then_4(self):
        response = self.post_lib_track_with_specific_sample("2 stars.wav")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.rating == 4

    def test_2_and_half_then_5(self):
        response = self.post_lib_track_with_specific_sample("2 5 stars.wav")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.rating == 5

    def test_3_then_6(self):
        response = self.post_lib_track_with_specific_sample("3 stars.wav")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.rating == 6

    def test_3_and_half_then_7(self):
        response = self.post_lib_track_with_specific_sample("3 5 stars.wav")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.rating == 7

    def test_4_then_8(self):
        response = self.post_lib_track_with_specific_sample("4 stars.wav")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.rating == 8

    def test_4_and_half_then_9(self):
        response = self.post_lib_track_with_specific_sample("4 5 stars.wav")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.rating == 9

    def test_5_then_10(self):
        response = self.post_lib_track_with_specific_sample("5 stars.wav")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.rating == 10
