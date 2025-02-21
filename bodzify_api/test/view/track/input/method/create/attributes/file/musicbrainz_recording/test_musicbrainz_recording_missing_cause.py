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
        assert not self.saved_object.track_file.musicbrainz_recording_missing_cause

    def test_no_matching_recording_then_corresponding_missing_cause(self):
        response = self._post_lib_track_with_specific_sample("Tokyo Drift x Temperature - no musicbrainz recording.mp3")
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.track_file.musicbrainz_recording_missing_cause
        assert self.saved_object.track_file.musicbrainz_recording_missing_cause.code.code == \
            MusicbrainzRecordingMissingCauseCode.Codes.LOOKUP_FOUND_NO_MATCHING_RECORDING

    def test_duration_below_one_then_corresponding_missing_cause(self):
        response = self._post_lib_track_with_generic_sample_below_1_sec()
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.track_file.musicbrainz_recording_missing_cause
        assert self.saved_object.track_file.musicbrainz_recording_missing_cause.code.code == \
            MusicbrainzRecordingMissingCauseCode.Codes.DURATION_BELOW_1_SEC

    def test_invalid_fingerprint_then_corresponding_missing_cause(self):
        response = self._post_lib_track_with_generic_sample_no_tags()
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.track_file.musicbrainz_recording_missing_cause
        assert self.saved_object.track_file.musicbrainz_recording_missing_cause.code.code == \
            MusicbrainzRecordingMissingCauseCode.Codes.LOOKUP_FAILED_WITH_INVALID_FINGERPRINT_RESPONSE_ERROR_CODE

    def test_long_message_then_truncated(self):
        with patch('bodzify_api.utils.musicbrainz.service._get_musicbrainz_best_recording_dict_from_fingerprint_and_duration') as mock_get_fingerprint:
            exception_message = "a" * (settings.MUSICBRAINZ_RECORDING_MISSING_CAUSE_MESSAGE_LEN_MAX + 1)
            mock_get_fingerprint.side_effect = \
                musicbrainz_exception.UnknownErrorStatusMusicbrainzRecordingLookupException(exception_message)

            response = self._post_lib_track_with_queenshowmustgoon()
            assert response.status_code == status.HTTP_201_CREATED
            assert self.saved_object.track_file.musicbrainz_recording_missing_cause
            assert self.saved_object.track_file.musicbrainz_recording_missing_cause.message == \
                "a" * (settings.MUSICBRAINZ_RECORDING_MISSING_CAUSE_MESSAGE_LEN_MAX - 3) + '...'

    def test_dns_resolution_error_then_corresponding_missing_cause(self):
        with patch('bodzify_api.utils.musicbrainz.service._get_musicbrainz_best_recording_dict_from_fingerprint_and_duration') as mock_get_fingerprint:
            error_message = "Failed to resolve 'api.acoustid.org' ([Errno 8] nodename nor servname provided, or not known)"
            mock_get_fingerprint.side_effect = \
                musicbrainz_exception.DNSResolutionErrorMusicbrainzRecordingLookupException(error_message)

            response = self._post_lib_track_with_queenshowmustgoon()
            assert response.status_code == status.HTTP_201_CREATED
            assert self.saved_object.track_file.musicbrainz_recording_missing_cause
            assert self.saved_object.track_file.musicbrainz_recording_missing_cause.code.code == \
                MusicbrainzRecordingMissingCauseCode.Codes.LOOKUP_FAILED_DNS_RESOLUTION_ERROR
            assert self.saved_object.track_file.musicbrainz_recording_missing_cause.message is not None
            assert "Failed to resolve 'api.acoustid.org'" in self.saved_object.track_file.musicbrainz_recording_missing_cause.message

    def test_internal_error_then_corresponding_missing_cause(self):
        with patch('bodzify_api.utils.musicbrainz.service._get_musicbrainz_best_recording_dict_from_fingerprint_and_duration') as mock_get_fingerprint:
            error_message = "Internal server error occurred"
            mock_get_fingerprint.side_effect = \
                musicbrainz_exception.InternalErrorStatusErrorMusicbrainzRecordingLookupException(error_message)

            response = self._post_lib_track_with_queenshowmustgoon()
            assert response.status_code == status.HTTP_201_CREATED
            assert self.saved_object.track_file.musicbrainz_recording_missing_cause
            assert self.saved_object.track_file.musicbrainz_recording_missing_cause.code.code == \
                MusicbrainzRecordingMissingCauseCode.Codes.LOOKUP_FAILED_WITH_INTERNAL_ERROR_RESPONSE_ERROR_CODE
            assert self.saved_object.track_file.musicbrainz_recording_missing_cause.message is not None

    def test_unknown_response_error_then_corresponding_missing_cause(self):
        with patch('bodzify_api.utils.musicbrainz.service._get_musicbrainz_best_recording_dict_from_fingerprint_and_duration') as mock_get_fingerprint:
            error_message = "Unknown response error"
            mock_get_fingerprint.side_effect = \
                musicbrainz_exception.UnknownErrorStatusMusicbrainzRecordingLookupException(error_message)

            response = self._post_lib_track_with_queenshowmustgoon()
            assert response.status_code == status.HTTP_201_CREATED
            assert self.saved_object.track_file.musicbrainz_recording_missing_cause
            assert self.saved_object.track_file.musicbrainz_recording_missing_cause.code.code == \
                MusicbrainzRecordingMissingCauseCode.Codes.LOOKUP_FAILED_WITH_UNKNOWN_RESPONSE_ERROR_CODE
            assert self.saved_object.track_file.musicbrainz_recording_missing_cause.message is not None

    def test_unknown_status_code_then_corresponding_missing_cause(self):
        with patch('bodzify_api.utils.musicbrainz.service._get_musicbrainz_best_recording_dict_from_fingerprint_and_duration') as mock_get_fingerprint:
            mock_get_fingerprint.side_effect = \
                musicbrainz_exception.UnknownStatusCodeMusicbrainzRecordingLookupException("unknown_status")

            response = self._post_lib_track_with_queenshowmustgoon()
            assert response.status_code == status.HTTP_201_CREATED
            assert self.saved_object.track_file.musicbrainz_recording_missing_cause
            assert self.saved_object.track_file.musicbrainz_recording_missing_cause.code.code == \
                MusicbrainzRecordingMissingCauseCode.Codes.LOOKUP_FAILED_WITH_RESPONSE_UNKNOWN_STATUS_CODE
            assert self.saved_object.track_file.musicbrainz_recording_missing_cause.message is not None

    def test_unknown_reason_then_corresponding_missing_cause(self):
        with patch('bodzify_api.utils.musicbrainz.service._get_musicbrainz_best_recording_dict_from_fingerprint_and_duration') as mock_get_fingerprint:
            mock_get_fingerprint.side_effect = Exception("Unknown error occurred")

            response = self._post_lib_track_with_queenshowmustgoon()
            assert response.status_code == status.HTTP_201_CREATED
            assert self.saved_object.track_file.musicbrainz_recording_missing_cause
            assert self.saved_object.track_file.musicbrainz_recording_missing_cause.code.code == \
                MusicbrainzRecordingMissingCauseCode.Codes.LOOKUP_FAILED_FOR_UNKNOWN_REASON
            assert self.saved_object.track_file.musicbrainz_recording_missing_cause.message is not None

    @pytest.mark.usefixtures("disable_audio_metadata_analysis")
    def test_audio_meta_analysis_disabled_then_corresponding_missing_cause(self):
        response = self._post_lib_track_with_queenshowmustgoon()
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.track_file.musicbrainz_recording_missing_cause
        assert self.saved_object.track_file.musicbrainz_recording_missing_cause.code.code == \
            MusicbrainzRecordingMissingCauseCode.Codes.AUDIO_META_AMALYSIS_DISABLED

    def test_track_file_missing_then_corresponding_missing_cause(self):
        with patch('bodzify_api.utils.audio_fingerprinter.get_fingerprinting_result') as mock_get_fingerprint:
            mock_get_fingerprint.return_value = FingerprintingResult(
                is_success=False,
                missing_cause=FingerprintMissingCause.objects.create(
                    user=self.user,
                    code=MusicbrainzRecordingMissingCauseCode.Codes.TRACK_FILE_MISSING
                )
            )
            response = self._post_lib_track_with_queenshowmustgoon()
            assert response.status_code == status.HTTP_201_CREATED
            assert self.saved_object.track_file.musicbrainz_recording_missing_cause
            assert self.saved_object.track_file.musicbrainz_recording_missing_cause.code.code == \
                MusicbrainzRecordingMissingCauseCode.Codes.TRACK_FILE_MISSING
