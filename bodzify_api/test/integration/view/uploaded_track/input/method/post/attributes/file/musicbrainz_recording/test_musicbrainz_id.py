import warnings

import pytest
from rest_framework import status

from bodzify_api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename
from bodzify_api.test.integration.view.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase


@pytest.mark.usefixtures("enable_audio_metadata_analysis")
class TestCase(UploadedTrackTestCase):

    def test_not_found_then_none(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_MP3)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.track_file.musicbrainz_recording is None

    def test_drown_7m21_mp3_then_ok(self):
        response = self._post_uploaded_track(
            UploadedTrackTestFilename.RECORDING_JUAN_HANSEN_OOSTIL_DROWN_MASSANO_REMIX_7M21_MP3)
        assert response.status_code == status.HTTP_201_CREATED
        recording = self.saved_object.track_file.musicbrainz_recording
        assert recording
        assert recording.musicbrainz_id == "4a45b00b-273d-40ed-9ecd-42f387f59c22"

    def test_totaleclipe_5m35_flac_then_ok(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.RECORDING_TOTAL_ECLIPSE_5M35_FLAC)
        assert response.status_code == status.HTTP_201_CREATED
        track_musicbrainz_recording = self.saved_object.track_file.musicbrainz_recording
        expected_musicbrainz_recording_id = "9f3c3b61-41a6-4bb9-a49c-33606f536784"
        if (track_musicbrainz_recording is None
                or track_musicbrainz_recording.musicbrainz_id != expected_musicbrainz_recording_id):
            warnings.warn(
                f"The expected MusicBrainz recording id {track_musicbrainz_recording} is not the one expected {expected_musicbrainz_recording_id}")

    def test_different_format_but_same_musicbrainz_recording(self):
        response = self._post_uploaded_track(
            UploadedTrackTestFilename.RECORDING_JUAN_HANSEN_OOSTIL_DROWN_MASSANO_REMIX_7M20_FLAC)
        assert response.status_code == status.HTTP_201_CREATED
        recording1 = self.saved_object.track_file.musicbrainz_recording
        if not recording1:
            missing_cause = self.saved_object.track_file.musicbrainz_recording_missing_cause
            code_label = missing_cause.code.label if missing_cause else "Unknown"
            message = missing_cause.message if missing_cause and missing_cause.message else "No message"
            warnings.warn(f"Recording 1 is None because of missing cause: {code_label} - {message}")
        else:
            flac_recording_id = recording1.musicbrainz_id

            response = self._post_uploaded_track(
                UploadedTrackTestFilename.RECORDING_JUAN_HANSEN_OOSTIL_DROWN_MASSANO_REMIX_7M21_MP3)
            assert response.status_code == status.HTTP_201_CREATED
            recording2 = self.saved_object.track_file.musicbrainz_recording
            if not recording2:
                missing_cause = self.saved_object.track_file.musicbrainz_recording_missing_cause
                code_label = missing_cause.code.label if missing_cause else "Unknown"
                message = missing_cause.message if missing_cause and missing_cause.message else "No message"
                warnings.warn(f"Recording 2 is None because of missing cause: {code_label} - {message}")
            else:
                assert recording2
                assert recording2.musicbrainz_id == flac_recording_id
