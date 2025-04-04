import pytest
from rest_framework import status

from bodzify_api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename
from bodzify_api.test.view.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase


@pytest.mark.usefixtures("enable_audio_metadata_analysis")
class TestCase(UploadedTrackTestCase):

    def test_totaleclipse_with_three_scores_then_highest(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.RECORDING_TOTAL_ECLIPSE_3_SCORES_FLAC)

        assert response.status_code == status.HTTP_201_CREATED
        musicbrainz_recording = self.saved_object.track_file.musicbrainz_recording
        assert musicbrainz_recording
        assert float(musicbrainz_recording.score) > 0.98
