import pytest
from rest_framework import status

from bodzify_api.test.utils.lib_track.LibTrackTestFilename import LibTrackTestFilename
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


@pytest.mark.usefixtures("enable_audio_metadata_analysis")
class TestCase(LibTrackTestCase):

    def test_drown_7m21_mp3_then_ok(self):
        response = self._post_lib_track(LibTrackTestFilename.RECORDING_JUAN_HANSEN_OOSTIL_DROWN_MASSANO_REMIX_7M21_MP3)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.track_file.musicbrainz_recording
        assert self.saved_object.track_file.musicbrainz_recording.title == "Drown (Massano remix)"

    def test_totaleclipe_5m35_flac_then_ok(self):
        response = self._post_lib_track(LibTrackTestFilename.RECORDING_TOTAL_ECLIPSE_5M35_FLAC)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.track_file.musicbrainz_recording
        assert self.saved_object.track_file.musicbrainz_recording.title == "Total Eclipse of the Heart"
