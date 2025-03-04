from decimal import Decimal
from typing import cast
from rest_framework import status

from bodzify_api.model.track.file.TrackFile import TrackFile
from bodzify_api.test.utils.lib_track.TestLibTrackFilename import TestLibTrackFilename
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase):

    def test_small_wav(self):
        response = self._post_lib_track(TestLibTrackFilename.SIZE_SMALL_0_08_MO_WAV)
        assert response.status_code == status.HTTP_201_CREATED
        track_file = cast(TrackFile, self.saved_object.track_file)
        assert Decimal(round(track_file.size_in_mo, 2)) == 0.08

    def test_small_mp3(self):
        response = self._post_lib_track(TestLibTrackFilename.SIZE_SMALL_0_01_MO_MP3)
        assert response.status_code == status.HTTP_201_CREATED
        track_file = cast(TrackFile, self.saved_object.track_file)
        assert Decimal(round(track_file.size_in_mo, 2) == round(14/1024, 2))

    def test_small_flac(self):
        response = self._post_lib_track(TestLibTrackFilename.SIZE_SMALL_0_05_MO_FLAC)
        assert response.status_code == status.HTTP_201_CREATED
        track_file = cast(TrackFile, self.saved_object.track_file)
        assert Decimal(round(track_file.size_in_mo, 2) == round(53/1024, 2))

    def test_big_wav(self):
        response = self._post_lib_track(TestLibTrackFilename.SIZE_BIG_79_55_MO_WAV)
        assert response.status_code == status.HTTP_201_CREATED
        track_file = cast(TrackFile, self.saved_object.track_file)
        assert Decimal(round(track_file.size_in_mo, 2) == round(81/1024, 2))

    def test_big_mp3(self):
        response = self._post_lib_track(TestLibTrackFilename.SIZE_BIG_9_98_MO_MP3)
        assert response.status_code == status.HTTP_201_CREATED
        track_file = cast(TrackFile, self.saved_object.track_file)
        assert Decimal(round(track_file.size_in_mo, 2) == round(14/1024, 2))

    def test_big_flac(self):
        response = self._post_lib_track(TestLibTrackFilename.SIZE_BIG_26_6_MO_FLAC)
        assert response.status_code == status.HTTP_201_CREATED
        track_file = cast(TrackFile, self.saved_object.track_file)
        assert Decimal(round(track_file.size_in_mo, 2)) == 26.6
