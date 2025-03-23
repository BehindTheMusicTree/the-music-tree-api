from rest_framework import status

from bodzify_api.test.utils.lib_track.LibTrackTestFilename import LibTrackTestFilename
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase):

    def test_1_then_2(self):
        response = self._post_lib_track(LibTrackTestFilename.RATING_VORBIS_TRAKTOR_1_STAR_FLAC)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.rating == 2

    def test_2_then_4(self):
        response = self._post_lib_track(LibTrackTestFilename.RATING_VORBIS_TRAKTOR_2_STAR_FLAC)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.rating == 4

    def test_3_then_6(self):
        response = self._post_lib_track(LibTrackTestFilename.RATING_VORBIS_TRAKTOR_3_STAR_FLAC)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.rating == 6

    def test_4_then_8(self):
        response = self._post_lib_track(LibTrackTestFilename.RATING_VORBIS_TRAKTOR_4_STAR_FLAC)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.rating == 8

    def test_5_then_10(self):
        response = self._post_lib_track(LibTrackTestFilename.RATING_VORBIS_TRAKTOR_5_STAR_FLAC)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.rating == 10
