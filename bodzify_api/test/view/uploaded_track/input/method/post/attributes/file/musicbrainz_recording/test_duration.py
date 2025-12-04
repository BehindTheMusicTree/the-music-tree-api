import pytest
from rest_framework import status

from bodzify_api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename
from bodzify_api.test.view.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase


@pytest.mark.usefixtures("enable_audio_metadata_analysis")
class TestCase(UploadedTrackTestCase):

    def test_duration_greater_to_one_sec_then_ok(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.RECORDING_QUEEN_DURATION_181_MP3)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.track_file.musicbrainz_recording
        assert self.saved_object.track_file.musicbrainz_recording.duration_in_sec == 181

    def test_musicbrainz_recording_is_missing_duration_then_none(self):
        response = self._post_uploaded_track(
            UploadedTrackTestFilename.RECORDING_CELINEKIN_PARK_NO_MUSICBRAINZ_RECORDING_DURATION_MP3)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.track_file.musicbrainz_recording
        assert not self.saved_object.track_file.musicbrainz_recording.duration_in_sec
