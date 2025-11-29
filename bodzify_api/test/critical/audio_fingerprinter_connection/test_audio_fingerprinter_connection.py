import time
import pytest
from rest_framework import status

from bodzify_api.model.uploaded_track.file.fingerprinting.missing_cause.code.FingerprintMissingCauseCode import FingerprintMissingCauseCode
from bodzify_api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename
from bodzify_api.test.view.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase


@pytest.mark.usefixtures("enable_audio_metadata_analysis")
class TestCase(UploadedTrackTestCase):

    @pytest.mark.critical
    def test_audio_fingerprinter_connection_ok(self):
        max_retries = 3
        retry_delay = 5
        
        for attempt in range(max_retries):
            try:
                print(f"test_audio_fingerprinter_connection_ok (attempt {attempt + 1}/{max_retries})")
                response = self._post_uploaded_track(
                    UploadedTrackTestFilename.RECORDING_JUAN_HANSEN_OOSTIL_DROWN_MASSANO_REMIX_7M21_MP3)
                is_reponse_ok = response.status_code == status.HTTP_201_CREATED
                if not is_reponse_ok:
                    print(self.bad_request_result)
                assert is_reponse_ok
                track_file = self.saved_object.track_file
                assert track_file
                if track_file.fingerprint_missing_cause:
                    print(track_file.fingerprint_missing_cause)
                    if attempt < max_retries - 1:
                        print(f"Retrying in {retry_delay} seconds...")
                        time.sleep(retry_delay)
                        continue
                    error_message = f"Audio Fingerprinter service connection failed: {track_file.fingerprint_missing_cause}"
                    if track_file.fingerprint_missing_cause.code.code == FingerprintMissingCauseCode.Codes.SERVICE_NOT_FOUND:
                        error_message += " The Audio Fingerprinter service is not available. Please ensure the service is running."
                    assert False, error_message

                if track_file.musicbrainz_recording_missing_cause:
                    print(track_file.musicbrainz_recording_missing_cause)
                    if attempt < max_retries - 1:
                        print(f"Retrying in {retry_delay} seconds...")
                        time.sleep(retry_delay)
                        continue
                    assert False, f"MusicBrainz recording lookup failed: {track_file.musicbrainz_recording_missing_cause}"
                else:
                    print("No musicbrainz_recording_missing_cause")

                assert track_file.musicbrainz_recording
                assert track_file.musicbrainz_recording.musicbrainz_id == "4a45b00b-273d-40ed-9ecd-42f387f59c22"
                return
            except AssertionError:
                if attempt < max_retries - 1:
                    print(f"Test failed, retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                    continue
                raise
