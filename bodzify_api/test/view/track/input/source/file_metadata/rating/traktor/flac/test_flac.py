#!/usr/bin/env python

import pytest
from rest_framework import status

from bodzify_api.test.view.track.input.source.file_metadata.rating.LibraryTrackFromFileMetadataRatingFieldTestCase \
    import LibTrackFromFileMetadataRatingFieldTestCase


@pytest.mark.django_db
class TestCase(LibTrackFromFileMetadataRatingFieldTestCase):

    def test_51_then_2(self):
        response = self.post_lib_track_with_specific_sample("1 star.flac")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.rating == 2

    def test_102_then_4(self):
        response = self.post_lib_track_with_specific_sample("2 stars.flac")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.rating == 4

    def test_153_then_6(self):
        response = self.post_lib_track_with_specific_sample("3 stars.flac")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.rating == 6

    def test_204_then_8(self):
        response = self.post_lib_track_with_specific_sample("4 stars.flac")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.rating == 8

    def test_255_then_10(self):
        response = self.post_lib_track_with_specific_sample("5 stars.flac")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.rating == 10
