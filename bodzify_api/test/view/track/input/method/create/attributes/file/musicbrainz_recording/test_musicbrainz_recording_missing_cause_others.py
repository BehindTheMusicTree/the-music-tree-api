
from unittest.mock import patch

import pytest
from rest_framework import status

from bodzify_api import settings
from bodzify_api.exception import musicbrainz as musicbrainz_exception
from bodzify_api.model.musicbrainz_resource.children.recording.missing_cause.code.MbRecordingMissingCauseCode import (
    MbRecordingMissingCauseCode
)
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


@pytest.mark.usefixtures("enable_audio_metadata_analysis")
class TestCase(LibTrackTestCase):

    def test_ok_then_no_missing_cause(self):
        response = self._post_lib_track_with_queenshowmustgoon()

        assert response.status_code == status.HTTP_201_CREATED
        assert not self.saved_object.track_file.musicbrainz_recording_missing_cause

    def test_no_matching_recording_then_corresponding_missing_cause(self):
        response = self._post_lib_track_with_specific_sample("Tokyo Drift x Temperature - no musicbrainz recording.mp3")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.track_file.musicbrainz_recording_missing_cause
        assert (self.saved_object.track_file.musicbrainz_recording_missing_cause.code.code ==
                MbRecordingMissingCauseCode.Codes.LOOKUP_FOUND_NO_MATCHING_RECORDING)

    def test_duration_below_or_equals_one_second_then_corresponding_missing_cause(self):
        response = self._post_lib_track_with_generic_sample_1_sec()

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.track_file.musicbrainz_recording_missing_cause
        assert (self.saved_object.track_file.musicbrainz_recording_missing_cause.code.code ==
                MbRecordingMissingCauseCode.Codes.DURATION_BELOW_OR_EQUAL_1_SEC)

    def test_invalid_fingerprint_then_corresponding_missing_cause(self):
        with patch('acoustid.lookup') as mock_lookup:
            error_code = 3  # MusicBrainz error code for invalid fingerprint.
            error_message = "Invalid fingerprint sent"
            mock_lookup.return_value = {
                'status': 'error',
                'error': {
                    'code': error_code,
                    'message': error_message
                }
            }
            response = self._post_lib_track_with_queenshowmustgoon()

            assert response.status_code == status.HTTP_201_CREATED
            assert self.saved_object.track_file.musicbrainz_recording_missing_cause
            assert (self.saved_object.track_file.musicbrainz_recording_missing_cause.code.code ==
                    MbRecordingMissingCauseCode.Codes.LOOKUP_FAILED_DUE_TO_INVALID_FINGERPRINT)

    def test_long_message_then_truncated(self):
        with patch('bodzify_api.utils.musicbrainz.service._get_musicbrainz_best_recording_dict_from_fingerprint_and_duration'
                   ) as mock_get_fingerprint:
            exception_message = "a" * (settings.MB_RECORDING_MISSING_CAUSE_MESSAGE_LEN_MAX + 1)
            mock_get_fingerprint.side_effect = (
                musicbrainz_exception.UnknownErrorCodeMusicbrainzRecordingLookupException(exception_message))

            response = self._post_lib_track_with_queenshowmustgoon()

            assert response.status_code == status.HTTP_201_CREATED
            assert self.saved_object.track_file.musicbrainz_recording_missing_cause
            assert (self.saved_object.track_file.musicbrainz_recording_missing_cause.message ==
                    "a" * (settings.MB_RECORDING_MISSING_CAUSE_MESSAGE_LEN_MAX - 3) + '...')

    def test_dns_resolution_error_then_corresponding_missing_cause(self):
        with patch('bodzify_api.utils.musicbrainz.service._get_musicbrainz_best_recording_dict_from_fingerprint_and_duration') as mock_get_fingerprint:
            error_message = "Failed to resolve 'api.acoustid.org' ([Errno 8] nodename nor servname provided, or not known)"
            mock_get_fingerprint.side_effect = (
                musicbrainz_exception.DNSResolutionErrorMusicbrainzRecordingLookupException(error_message))

            response = self._post_lib_track_with_queenshowmustgoon()

            assert response.status_code == status.HTTP_201_CREATED
            assert self.saved_object.track_file.musicbrainz_recording_missing_cause
            assert (self.saved_object.track_file.musicbrainz_recording_missing_cause.code.code ==
                    MbRecordingMissingCauseCode.Codes.LOOKUP_FAILED_DNS_RESOLUTION_ERROR)
            assert self.saved_object.track_file.musicbrainz_recording_missing_cause.message is not None
            assert "Failed to resolve 'api.acoustid.org'" in self.saved_object.track_file.musicbrainz_recording_missing_cause.message

    def test_internal_error_then_corresponding_missing_cause(self):
        with patch('bodzify_api.utils.musicbrainz.service._get_musicbrainz_best_recording_dict_from_fingerprint_and_duration') as mock_get_fingerprint:
            error_message = "Internal server error occurred"
            mock_get_fingerprint.side_effect = (
                musicbrainz_exception.InternalErrorMusicbrainzRecordingLookupException(error_message))

            response = self._post_lib_track_with_queenshowmustgoon()

            assert response.status_code == status.HTTP_201_CREATED
            assert self.saved_object.track_file.musicbrainz_recording_missing_cause
            assert (self.saved_object.track_file.musicbrainz_recording_missing_cause.code.code ==
                    MbRecordingMissingCauseCode.Codes.LOOKUP_FAILED_WITH_INTERNAL_ERROR)
            assert self.saved_object.track_file.musicbrainz_recording_missing_cause.message is not None

    def test_unknown_error_code_then_corresponding_missing_cause(self):
        with patch('acoustid.lookup') as mock_lookup:
            error_code = 7  # Using error code 7 (not 3 or 5)
            error_message = "Some other error"
            mock_lookup.return_value = {
                'status': 'error',
                'error': {
                    'code': error_code,
                    'message': error_message
                }
            }

            response = self._post_lib_track_with_queenshowmustgoon()

            assert response.status_code == status.HTTP_201_CREATED
            assert self.saved_object.track_file.musicbrainz_recording_missing_cause
            assert (self.saved_object.track_file.musicbrainz_recording_missing_cause.code.code ==
                    MbRecordingMissingCauseCode.Codes.LOOKUP_FAILED_WITH_UNKNOWN_RESPONSE_ERROR_CODE)
            assert self.saved_object.track_file.musicbrainz_recording_missing_cause.message is not None

    def test_unknown_status_code_then_corresponding_missing_cause(self):
        with patch('bodzify_api.utils.musicbrainz.service._get_musicbrainz_best_recording_dict_from_fingerprint_and_duration') as mock_get_fingerprint:
            mock_get_fingerprint.side_effect = (
                musicbrainz_exception.UnknownStatusMusicbrainzRecordingLookupException("unknown_status"))

            response = self._post_lib_track_with_queenshowmustgoon()

            assert response.status_code == status.HTTP_201_CREATED
            assert self.saved_object.track_file.musicbrainz_recording_missing_cause
            assert (self.saved_object.track_file.musicbrainz_recording_missing_cause.code.code ==
                    MbRecordingMissingCauseCode.Codes.LOOKUP_FAILED_WITH_UNKNOWN_RESPONSE_STATUS_CODE)
            assert self.saved_object.track_file.musicbrainz_recording_missing_cause.message is not None
