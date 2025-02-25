import pytest
from rest_framework import status

from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


@pytest.mark.django_db
class TestCase(LibTrackTestCase):

    def test_wav(self):
        response = self._post_lib_track_with_generic_sample_no_tags(extension='wav')
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.track_file.bitrate_in_kbps == 1190

    def test_mp3(self):
        response = self._post_lib_track_with_generic_sample_no_tags(extension='mp3')
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.track_file.bitrate_in_kbps == 192

    def test_flac_without_corrected_md5(self):
        response = self._post_lib_track_with_queenshowmustgoon(extension='flac')
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.track_file.bitrate_in_kbps == 723

    def test_flac_with_corrected_md5(self):
        response = self._post_lib_track_with_californiagurls_flac_with_id3v2_tags()
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.track_file.bitrate_in_kbps == 723
