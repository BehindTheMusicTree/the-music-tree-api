import pytest
from rest_framework import status

from bodzify_api.test.utils.lib_track.LibTrackTestFilename import LibTrackTestFilename
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


@pytest.mark.usefixtures("enable_audio_metadata_analysis")
class TestCase(LibTrackTestCase):

    def test_duration_greater_to_one_sec_then_ok(self):
        response = self._post_lib_track(LibTrackTestFilename.RECORDING_QUEEN_DURATION_181_MP3)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.track_file.musicbrainz_recording
        assert self.saved_object.track_file.musicbrainz_recording.duration_in_sec == 182

    def test_musicbrainz_recording_is_missing_duration_then_none(self):
        response = self._post_lib_track(
            LibTrackTestFilename.RECORDING_CELINEKIN_PARK_NO_MUSICBRAINZ_RECORDING_DURATION_MP3)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.track_file.musicbrainz_recording
        assert not self.saved_object.track_file.musicbrainz_recording.duration_in_sec
