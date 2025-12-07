import pytest
from rest_framework import status

from api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from api.serializer.model.uploaded_track.input.post.Fields import Fields
from api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename
from api.test.integration.view.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase


@pytest.mark.usefixtures("enable_audio_metadata_analysis")
class TestCase(UploadedTrackTestCase):

    def test_duplicate_fingerprint_and_must_cancel_if_duplicate_fingerprint_then_bad_request(self):
        data = {Fields.TRACK_FILE_FINGERPRINT_MUST_BE_UNIQUE: True}
        response = self._post_uploaded_track(UploadedTrackTestFilename.RECORDING_KEMAR_FRANCE_MP3, **data)

        assert response.status_code == status.HTTP_201_CREATED

        response = self._post_uploaded_track(UploadedTrackTestFilename.RECORDING_KEMAR_FRANCE_MP3, **data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error['field'] == Fields.TRACK_FILE_PUBLIC
        assert error['code'] == FieldValidationErrorCode.TRACK_FILE_FINGERPRINT_DUPLICATE

    def test_not_duplicate_fingerprint_and_must_cancel_if_duplicate_fingerprint_then_ok(self):
        data = {Fields.TRACK_FILE_FINGERPRINT_MUST_BE_UNIQUE: True}
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_MP3, **data)

        assert response.status_code == status.HTTP_201_CREATED

        response = self._post_uploaded_track(UploadedTrackTestFilename.RECORDING_SHOWMUSTGOON_MP3, **data)

        assert response.status_code == status.HTTP_201_CREATED

    def test_duplicate_fingerprint_and_not_must_cancel_if_duplicate_fingerprint_then_ok(self):
        data = {Fields.TRACK_FILE_FINGERPRINT_MUST_BE_UNIQUE: False}
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_MP3, **data)

        assert response.status_code == status.HTTP_201_CREATED

        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_MP3, **data)

        assert response.status_code == status.HTTP_201_CREATED

    def test_duplicate_fingerprint_and_must_cancel_if_duplicate_fingerprint_not_provided_then_ok(self):
        data = {Fields.TRACK_FILE_FINGERPRINT_MUST_BE_UNIQUE: False}
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_MP3, **data)

        assert response.status_code == status.HTTP_201_CREATED

        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_MP3, **data)

        assert response.status_code == status.HTTP_201_CREATED
