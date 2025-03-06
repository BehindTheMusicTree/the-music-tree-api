from typing import cast
from rest_framework import status

from bodzify_api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.model.track.file.flac.FlacTrackFile import FlacTrackFile
from bodzify_api.serializer.model.lib_track.input.post.Fields import Fields as LibTrackPostFields
from bodzify_api.test.utils.lib_track.TestLibTrackFilename import TestLibTrackFilename
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase
from bodzify_api.utils import audio_metadata
from bodzify_api.view.error.ErrorResponseFields import ErrorResponseFields


class TestCase(LibTrackTestCase):

    def test_flac_md5_not_valid_and_corrupted_then_400(self):
        response = self._post_lib_track(TestLibTrackFilename.FORMAT_MD5_NOT_VALID_AND_CORRUPTED_FLAC)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error[ErrorResponseFields.FieldErrors.FIELD] == LibTrackPostFields.TRACK_FILE_PUBLIC
        assert error[ErrorResponseFields.FieldErrors.CODE] == FieldValidationErrorCode.AUDIO_FILE_CORRUPTED

    def test_flac_md5_not_valid_not_because_of_id3v2_metadata_then_corrected(self):
        response = self._post_lib_track(TestLibTrackFilename.FORMAT_MD5_NOT_VALID_NOT_BECAUSE_OF_ID3V2_METADATA_FLAC)

        assert response.status_code == status.HTTP_201_CREATED
        track_file = self.saved_object.track_file
        assert isinstance(track_file, FlacTrackFile)
        assert track_file.md5_has_been_corrected
        assert audio_metadata.is_flac_md5_valid(track_file.file)

    def test_flac_md5_not_valid_because_of_id3v2_metadata_then_corrected(self):
        response = self._post_lib_track(TestLibTrackFilename.FORMAT_MD5_NOT_VALID_BECAUSE_OF_ID3V2_METADATA_FLAC)

        assert response.status_code == status.HTTP_201_CREATED
        track_file = cast(FlacTrackFile, self.saved_object.track_file)
        assert track_file
        assert track_file.md5_has_been_corrected

    def test_flac_md5_is_valid(self):
        response = self._post_lib_track(TestLibTrackFilename.RECORDING_DANS_LA_LEGENDE_FLAC)

        assert response.status_code == status.HTTP_201_CREATED
        track_file = cast(FlacTrackFile, self.saved_object.track_file)
        assert track_file
        assert not track_file.md5_has_been_corrected
