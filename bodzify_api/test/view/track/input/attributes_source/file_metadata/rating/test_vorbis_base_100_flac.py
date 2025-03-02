import pytest
from rest_framework import status

from bodzify_api.test.utils.lib_track.TestLibTrackFilename import TestLibTrackFilename
from bodzify_api.test.view.track.input.attributes_source.file_metadata.rating.RatingNotNoneWithHalfValuesAndZeroTestCase import (
    RatingNotNoneWithHalfValuesAndZeroTestCase)


@pytest.mark.django_db
class TestCase(RatingNotNoneWithHalfValuesAndZeroTestCase):

    def test_0_then_0(self):
        response = self._post_lib_track(TestLibTrackFilename.RATING_VORBIS_0_STAR_FLAC)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.rating == 0

    def test_0_and_half_then_1(self):
        response = self._post_lib_track(TestLibTrackFilename.RATING_VORBIS_0_5_STAR_FLAC)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.rating == 1

    def test_1_then_2(self):
        response = self._post_lib_track(TestLibTrackFilename.RATING_VORBIS_1_STAR_FLAC)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.rating == 2

    def test_1_and_half_then_3(self):
        response = self._post_lib_track(TestLibTrackFilename.RATING_VORBIS_1_5_STAR_FLAC)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.rating == 3

    def test_2_then_4(self):
        response = self._post_lib_track(TestLibTrackFilename.RATING_VORBIS_2_STAR_FLAC)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.rating == 4

    def test_2_and_half_then_5(self):
        response = self._post_lib_track(TestLibTrackFilename.RATING_VORBIS_2_5_STAR_FLAC)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.rating == 5

    def test_3_then_6(self):
        response = self._post_lib_track(TestLibTrackFilename.RATING_VORBIS_3_STAR_FLAC)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.rating == 6

    def test_3_and_half_then_7(self):
        response = self._post_lib_track(TestLibTrackFilename.RATING_VORBIS_3_5_STAR_FLAC)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.rating == 7

    def test_4_then_8(self):
        response = self._post_lib_track(TestLibTrackFilename.RATING_VORBIS_4_STAR_FLAC)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.rating == 8

    def test_4_and_half_then_9(self):
        response = self._post_lib_track(TestLibTrackFilename.RATING_VORBIS_4_5_STAR_FLAC)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.rating == 9

    def test_5_then_10(self):
        response = self._post_lib_track(TestLibTrackFilename.RATING_VORBIS_5_STAR_FLAC)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.rating == 10
