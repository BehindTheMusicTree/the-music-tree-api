import pytest
from rest_framework import status

from bodzify_api.test.utils.lib_track.TestLibTrackFilename import TestLibTrackFilename
from bodzify_api.test.view.track.input.attributes_source.file_metadata.rating.RatingNotNoneWithHalfValuesAndZeroTestCase import (
    RatingNotNoneWithHalfValuesAndZeroTestCase)


@pytest.mark.django_db
class TestCase(RatingNotNoneWithHalfValuesAndZeroTestCase):

    def test_1_then_2(self):
        response = self._post_lib_track(TestLibTrackFilename.RATING_RIFF_BASE_100_1_STAR_MP3)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.rating == 2

    def test_2_then_4(self):
        response = self._post_lib_track(TestLibTrackFilename.RATING_RIFF_BASE_100_2_STAR_MP3)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.rating == 4

    def test_3_then_6(self):
        response = self._post_lib_track(TestLibTrackFilename.RATING_RIFF_BASE_100_3_STAR_MP3)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.rating == 6

    def test_4_then_8(self):
        response = self._post_lib_track(TestLibTrackFilename.RATING_RIFF_BASE_100_4_STAR_MP3)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.rating == 8

    def test_5_then_10(self):
        response = self._post_lib_track(TestLibTrackFilename.RATING_RIFF_BASE_100_5_STAR_MP3)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.rating == 10
