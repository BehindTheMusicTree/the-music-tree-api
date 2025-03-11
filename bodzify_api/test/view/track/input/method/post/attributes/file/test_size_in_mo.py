from typing import cast
from rest_framework import status

from bodzify_api.model.track.file.TrackFile import TrackFile
from bodzify_api.test.utils.lib_track.LibTrackTestFilename import LibTrackTestFilename
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase):

    def test_small_wav(self):
        response = self._post_lib_track(LibTrackTestFilename.SIZE_SMALL_0_08_MO_WAV)
        assert response.status_code == status.HTTP_201_CREATED
        track_file = cast(TrackFile, self.saved_object.track_file)
        assert str(round(track_file.size_in_mo, 2)) == '0.08'

    def test_small_mp3(self):
        response = self._post_lib_track(LibTrackTestFilename.SIZE_SMALL_0_01_MO_MP3)
        assert response.status_code == status.HTTP_201_CREATED
        track_file = cast(TrackFile, self.saved_object.track_file)
        assert str(round(track_file.size_in_mo, 2)) == '0.01'

    def test_small_flac(self):
        response = self._post_lib_track(LibTrackTestFilename.SIZE_SMALL_0_05_MO_FLAC)
        assert response.status_code == status.HTTP_201_CREATED
        track_file = cast(TrackFile, self.saved_object.track_file)
        assert str(round(track_file.size_in_mo, 2)) == '0.05'

    def test_big_wav(self):
        response = self._post_lib_track(LibTrackTestFilename.SIZE_BIG_79_55_MO_WAV)
        assert response.status_code == status.HTTP_201_CREATED
        track_file = cast(TrackFile, self.saved_object.track_file)
        assert str(round(track_file.size_in_mo, 2)) == '79.55'

    def test_big_mp3(self):
        response = self._post_lib_track(LibTrackTestFilename.SIZE_BIG_9_98_MO_MP3)
        assert response.status_code == status.HTTP_201_CREATED
        track_file = cast(TrackFile, self.saved_object.track_file)
        assert str(round(track_file.size_in_mo, 2)) == '9.98'

    def test_big_flac(self):
        response = self._post_lib_track(LibTrackTestFilename.SIZE_BIG_26_6_MO_FLAC)
        assert response.status_code == status.HTTP_201_CREATED
        track_file = cast(TrackFile, self.saved_object.track_file)
        assert str(round(track_file.size_in_mo, 2)) == '25.91'
