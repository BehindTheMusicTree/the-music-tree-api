from unittest.mock import patch

import pytest
from rest_framework import status

from bodzify_api import settings
from bodzify_api.exception import musicbrainz as musicbrainz_exception
from bodzify_api.model.musicbrainz_resource.children.recording.missing_cause.code.MusicbrainzRecordingMissingCauseCode \
    import MusicbrainzRecordingMissingCauseCode
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


@pytest.mark.usefixtures("enable_audio_metadata_analysis")
class TestCase(LibTrackTestCase):

    def test_ok_then_no_missing_cause(self):
        response = self._post_lib_track_with_queenshowmustgoon()
        assert response.status_code == status.HTTP_201_CREATED
        assert not self.saved_lib_track.track_file.musicbrainz_recording_missing_cause

    def test_no_matching_recording_then_corresponding_missing_cause(self):
        response = self._post_lib_track_with_specific_sample("Tokyo Drift x Temperature - no musicbrainz recording.mp3")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.track_file.musicbrainz_recording_missing_cause
        assert self.saved_lib_track.track_file.musicbrainz_recording_missing_cause.code.code == \
            MusicbrainzRecordingMissingCauseCode.Codes.LOOKUP_FOUND_NO_MATCHING_RECORDING

    def test_duration_below_one_then_corresponding_missing_cause(self):
        response = self._post_lib_track_with_generic_sample_below_1_sec()
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.track_file.musicbrainz_recording_missing_cause
        assert self.saved_lib_track.track_file.musicbrainz_recording_missing_cause.code.code == \
            MusicbrainzRecordingMissingCauseCode.Codes.DURATION_BELOW_1_SEC

    def test_invalid_fingerprint_then_corresponding_missing_cause(self):
        response = self._post_lib_track_with_generic_sample_no_tags()
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.track_file.musicbrainz_recording_missing_cause
        assert self.saved_lib_track.track_file.musicbrainz_recording_missing_cause.code.code == \
            MusicbrainzRecordingMissingCauseCode.Codes.LOOKUP_FAILED_WITH_INVALID_FINGERPRINT_RESPONSE_ERROR_CODE

    def test_long_message_then_truncated(self):
        with patch('bodzify_api.utils.musicbrainz.service._get_musicbrainz_best_recording_dict_from_fingerprint_and_duration') as mock_get_fingerprint:
            exception_message = "a" * (settings.MUSICBRAINZ_RECORDING_MISSING_CAUSE_MESSAGE_LEN_MAX + 1)
            mock_get_fingerprint.side_effect = \
                musicbrainz_exception.UnknownErrorStatusMusicbrainzRecordingLookupException(exception_message)

            response = self._post_lib_track_with_queenshowmustgoon()
            assert response.status_code == status.HTTP_201_CREATED
            assert self.saved_lib_track.track_file.musicbrainz_recording_missing_cause
            assert self.saved_lib_track.track_file.musicbrainz_recording_missing_cause.message == \
                "a" * (settings.MUSICBRAINZ_RECORDING_MISSING_CAUSE_MESSAGE_LEN_MAX - 3) + '...'
