import pytest
from rest_framework import status

from bodzify_api.test.view.track.input.attributes_source.file_metadata.rating.RatingNotNoneTestCase import (
    RatingNotNoneTestCase
)


@pytest.mark.django_db
class TestCase(RatingNotNoneTestCase):

    def test_1_then_2(self):
        response = self._post_lib_track_with_specific_sample("1 star.mp3")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.rating == 2

    def test_2_then_4(self):
        response = self._post_lib_track_with_specific_sample("2 stars.mp3")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.rating == 4

    def test_3_then_6(self):
        response = self._post_lib_track_with_specific_sample("3 stars.mp3")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.rating == 6

    def test_4_then_8(self):
        response = self._post_lib_track_with_specific_sample("4 stars.mp3")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.rating == 8

    def test_5_then_10(self):
        response = self._post_lib_track_with_specific_sample("5 stars.mp3")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.rating == 10
