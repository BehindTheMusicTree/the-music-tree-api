from decimal import Decimal
from typing import cast
from rest_framework import status

from bodzify_api.model.track.file.TrackFile import TrackFile
from bodzify_api.test.utils.lib_track.TestLibTrackFilename import TestLibTrackFilename
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase):

    def test_wav(self):
        response = self._post_lib_track(TestLibTrackFilename.METADATA_NONE_WAV)
        assert response.status_code == status.HTTP_201_CREATED
        track_file = cast(TrackFile, self.saved_object.track_file)
        assert Decimal(round(track_file.size_in_mo, 2) == round(81/1024, 2))

    def test_mp3(self):
        response = self._post_lib_track(TestLibTrackFilename.METADATA_NONE_MP3)
        assert response.status_code == status.HTTP_201_CREATED
        track_file = cast(TrackFile, self.saved_object.track_file)
        assert Decimal(round(track_file.size_in_mo, 2) == round(14/1024, 2))

    def test_flac(self):
        response = self._post_lib_track(TestLibTrackFilename.METADATA_NONE_FLAC)
        assert response.status_code == status.HTTP_201_CREATED
        track_file = cast(TrackFile, self.saved_object.track_file)
        assert Decimal(round(track_file.size_in_mo, 2) == round(53/1024, 2))
