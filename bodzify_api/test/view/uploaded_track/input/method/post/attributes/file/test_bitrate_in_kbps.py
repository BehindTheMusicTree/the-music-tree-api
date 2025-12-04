from typing import cast
from rest_framework import status

from bodzify_api.model.uploaded_track.file.TrackFile import TrackFile
from bodzify_api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename
from bodzify_api.test.view.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase


class TestCase(UploadedTrackTestCase):

    def test_small_wav(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.BITRATE_IN_KBPS_SMALL_1152_WAV)
        assert response.status_code == status.HTTP_201_CREATED
        track_file = cast(TrackFile, self.saved_object.track_file)
        assert track_file.bitrate_in_kbps == 1152

    def test_small_mp3(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.BITRATE_IN_KBPS_SMALL_192_MP3)
        assert response.status_code == status.HTTP_201_CREATED
        track_file = cast(TrackFile, self.saved_object.track_file)
        assert track_file.bitrate_in_kbps == 192

    def test_small_flac(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.BITRATE_IN_KBPS_SMALL_723_FLAC)
        assert response.status_code == status.HTTP_201_CREATED
        track_file = cast(TrackFile, self.saved_object.track_file)
        assert track_file.bitrate_in_kbps == 723

    def test_big_wav(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.BITRATE_IN_KBPS_BIG_1411_WAV)
        assert response.status_code == status.HTTP_201_CREATED
        track_file = cast(TrackFile, self.saved_object.track_file)
        assert track_file.bitrate_in_kbps == 1411

    def test_big_mp3(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.BITRATE_IN_KBPS_BIG_320_MP3)
        assert response.status_code == status.HTTP_201_CREATED
        track_file = cast(TrackFile, self.saved_object.track_file)
        assert track_file.bitrate_in_kbps == 320

    def test_big_flac(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.BITRATE_IN_KBPS_BIG_946_FLAC)
        assert response.status_code == status.HTTP_201_CREATED
        track_file = cast(TrackFile, self.saved_object.track_file)
        assert track_file.bitrate_in_kbps == 922
