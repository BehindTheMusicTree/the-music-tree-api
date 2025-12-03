import os

from rest_framework import status

from bodzify_api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.serializer.model.uploaded_track.input.post.Fields import Fields as UploadedTrackPostFields
from bodzify_api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename
from bodzify_api.test.view.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase
from bodzify_api.utils.audio_metadata import is_flac_md5_valid


class TestCase(UploadedTrackTestCase):

    def test_flac_md5_not_valid_and_corrupted_then_400_bad_request(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.FORMAT_MD5_NOT_VALID_AND_CORRUPTED_FLAC)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error['field'] == UploadedTrackPostFields.TRACK_FILE_PUBLIC
        assert error['code'] == FieldValidationErrorCode.TRACK_FILE_TYPE_INVALID

    def test_flac_md5_not_valid_not_because_of_id3v1_metadata_then_corrected(self):
        response = self._post_uploaded_track(
            UploadedTrackTestFilename.FORMAT_MD5_NOT_VALID_NOT_BECAUSE_OF_ID3V1_METADATA_FLAC)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.track_file.md5_has_been_corrected

        self.saved_object.refresh_from_db()
        self.saved_object.track_file.refresh_from_db()
        file_path = getattr(self.saved_object.track_file.file, 'path', None)

        assert file_path and file_path.endswith('.flac'), "File path should be a FLAC file"
        assert is_flac_md5_valid(file_path), f"FLAC MD5 should be valid after correction for file: {file_path}"

    def test_flac_md5_not_valid_because_of_id3v1_metadata_then_corrected(self):
        response = self._post_uploaded_track(
            UploadedTrackTestFilename.FORMAT_MD5_NOT_VALID_BECAUSE_OF_ID3V1_METADATA_FLAC)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.track_file.md5_has_been_corrected

    def test_flac_md5_is_valid(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.RECORDING_DANS_LA_LEGENDE_FLAC)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.track_file
        assert not self.saved_object.track_file.md5_has_been_corrected
