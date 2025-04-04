from rest_framework import status

from bodzify_api.test.utils.uploaded_track.LibTrackTestFilename import LibTrackTestFilename
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase):

    def test_0_then_0(self):
        response = self._post_uploaded_track(LibTrackTestFilename.RATING_ID3V2_0_STAR_MP3)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.rating == 0

    def test_0_and_half_then_1(self):
        response = self._post_uploaded_track(LibTrackTestFilename.RATING_ID3V2_0_5_STAR_MP3)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.rating == 1

    def test_1_then_2(self):
        response = self._post_uploaded_track(LibTrackTestFilename.RATING_ID3V2_1_STAR_MP3)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.rating == 2

    def test_1_and_half_then_3(self):
        response = self._post_uploaded_track(LibTrackTestFilename.RATING_ID3V2_1_5_STAR_MP3)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.rating == 3

    def test_2_then_4(self):
        response = self._post_uploaded_track(LibTrackTestFilename.RATING_ID3V2_2_STAR_MP3)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.rating == 4

    def test_2_and_half_then_5(self):
        response = self._post_uploaded_track(LibTrackTestFilename.RATING_ID3V2_2_5_STAR_MP3)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.rating == 5

    def test_3_then_6(self):
        response = self._post_uploaded_track(LibTrackTestFilename.RATING_ID3V2_3_STAR_MP3)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.rating == 6

    def test_3_and_half_then_7(self):
        response = self._post_uploaded_track(LibTrackTestFilename.RATING_ID3V2_3_5_STAR_MP3)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.rating == 7

    def test_4_then_8(self):
        response = self._post_uploaded_track(LibTrackTestFilename.RATING_ID3V2_4_STAR_MP3)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.rating == 8

    def test_4_and_half_then_9(self):
        response = self._post_uploaded_track(LibTrackTestFilename.RATING_ID3V2_4_5_STAR_MP3)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.rating == 9

    def test_5_then_10(self):
        response = self._post_uploaded_track(LibTrackTestFilename.RATING_ID3V2_5_STAR_MP3)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.rating == 10
