
import uuid

import pytest
from rest_framework import status

from bodzify_api.test.view.track.TrackTestCase import LibTrackTestCase


@pytest.mark.usefixtures("enable_audio_metadata_analysis")
class TestCase(LibTrackTestCase):

    @pytest.mark.critical
    def test_audio_fingerprinter_connection_ok(self):
        print("test_audio_fingerprinter_connection_ok")
        response = self._post_lib_track_with_specific_sample("oostil - drown (massano remix) - 7m21.mp3")
        is_reponse_ok = response.status_code == status.HTTP_201_CREATED
        if not is_reponse_ok:
            print(response.data)  # type: ignore
        assert is_reponse_ok
        track_file = self.saved_lib_track.track_file
        assert track_file
        if track_file.fingerprint_missing_cause:
            print(track_file.fingerprint_missing_cause)
            assert False

        if track_file.musicbrainz_recording_missing_cause:
            print(track_file.musicbrainz_recording_missing_cause)
            assert False
        else:
            print("No musicbrainz_recording_missing_cause")

        assert track_file.musicbrainz_recording
        assert track_file.musicbrainz_recording.musicbrainz_id == "4a45b00b-273d-40ed-9ecd-42f387f59c22"
