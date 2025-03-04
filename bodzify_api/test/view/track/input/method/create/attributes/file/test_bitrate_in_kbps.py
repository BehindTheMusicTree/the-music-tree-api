from typing import cast
from rest_framework import status

from bodzify_api.model.track.file.TrackFile import TrackFile
from bodzify_api.test.utils.lib_track.TestLibTrackFilename import TestLibTrackFilename
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase):

    def test_small_wav(self):
        response = self._post_lib_track(TestLibTrackFilename.BITRATE_IN_KPBPS_SMALL_1152_WAV)
        assert response.status_code == status.HTTP_201_CREATED
        track_file = cast(TrackFile, self.saved_object.track_file)
        assert track_file.bitrate_in_kbps == 1152

    def test_small_mp3(self):
        response = self._post_lib_track(TestLibTrackFilename.BITRATE_IN_KPBPS_SMALL_192_MP3)
        assert response.status_code == status.HTTP_201_CREATED
        track_file = cast(TrackFile, self.saved_object.track_file)
        assert track_file.bitrate_in_kbps == 192

    def test_small_flac(self):
        response = self._post_lib_track(TestLibTrackFilename.BITRATE_IN_KPBPS_SMALL_1152_FLAC)
        assert response.status_code == status.HTTP_201_CREATED
        track_file = cast(TrackFile, self.saved_object.track_file)
        assert track_file.bitrate_in_kbps == 1152

    def test_big_wav(self):
        response = self._post_lib_track(TestLibTrackFilename.BITRATE_IN_KPBPS_BIG_1411_WAV)
        assert response.status_code == status.HTTP_201_CREATED
        track_file = cast(TrackFile, self.saved_object.track_file)
        assert track_file.bitrate_in_kbps == 1411

    def test_big_mp3(self):
        response = self._post_lib_track(TestLibTrackFilename.BITRATE_IN_KPBPS_BIG_320_MP3)
        assert response.status_code == status.HTTP_201_CREATED
        track_file = cast(TrackFile, self.saved_object.track_file)
        assert track_file.bitrate_in_kbps == 320

    def test_big_flac(self):
        response = self._post_lib_track(TestLibTrackFilename.BITRATE_IN_KPBPS_BIG_946_FLAC)
        assert response.status_code == status.HTTP_201_CREATED
        track_file = cast(TrackFile, self.saved_object.track_file)
        assert track_file.bitrate_in_kbps == 946
