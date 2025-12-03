import logging
import subprocess

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
        self.saved_object.track_file.refresh_from_db()
        file_path = self.saved_object.track_file.file.path if hasattr(
            self.saved_object.track_file.file, 'path') else None

        logger = logging.getLogger(__name__)
        logger.info(f"Test checking file: {file_path}")

        if file_path and file_path.endswith('.flac'):
            result = subprocess.run(['flac', '-t', file_path], capture_output=True, text=True)
            logger.info(
                f"FLAC tool result: returncode={result.returncode}, stderr={result.stderr[:200] if result.stderr else None}")
            assert result.returncode == 0, f"FLAC tool validation failed: {result.stderr}"

        logger.info(f"Checking with is_flac_md5_valid: {is_flac_md5_valid(self.saved_object.track_file.file)}")
        assert is_flac_md5_valid(self.saved_object.track_file.file)

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
