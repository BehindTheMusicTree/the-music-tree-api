import pytest
from rest_framework import status

from bodzify_api.test.utils.lib_track.LibTrackTestFilename import LibTrackTestFilename
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


@pytest.mark.usefixtures("enable_audio_metadata_analysis")
class TestCase(LibTrackTestCase):

    def test_totaleclipse_with_three_scores_then_highest(self):
        response = self._post_lib_track(LibTrackTestFilename.RECORDING_TOTAL_ECLIPSE_3_SCORES_FLAC)

        assert response.status_code == status.HTTP_201_CREATED
        musicbrainz_recording = self.saved_object.track_file.musicbrainz_recording
        assert musicbrainz_recording
        assert float(musicbrainz_recording.score) > 0.98
