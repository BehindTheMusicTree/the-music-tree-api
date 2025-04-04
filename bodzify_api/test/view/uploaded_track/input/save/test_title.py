from rest_framework import status

from bodzify_api import settings
from bodzify_api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.serializer.model.uploaded_track.input.post.Fields import Fields as PostFields
from bodzify_api.test.utils.field.body_data.type.NotNullableCharBodyDataTestCase import NotNullableCharBodyDataTestCase
from bodzify_api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename
from bodzify_api.test.view.uploaded_track.LibTrackTestCase import LibTrackTestCase


class TestCase(NotNullableCharBodyDataTestCase, LibTrackTestCase):

    def test_largest_then_ok(self):
        value = "a" * settings.UPLOADED_TRACK_TITLE_LEN_MAX
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_MP3, **{PostFields.TITLE: value})

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.title == value

    def test_too_large_then_400_bad_request(self):
        value = "a" * (settings.UPLOADED_TRACK_TITLE_LEN_MAX + 1)
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_MP3, **{PostFields.TITLE: value})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error['field'] == PostFields.TITLE
        assert error['code'] == FieldValidationErrorCode.STRING_TOO_LONG

    def test_empty_then_400_bad_request(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_MP3, **{PostFields.TITLE: ""})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error['field'] == PostFields.TITLE
        assert error['code'] == FieldValidationErrorCode.BLANK

    def test_multi_value_then_400_bad_request(self):
        response = self._post_uploaded_track(
            UploadedTrackTestFilename.METADATA_NONE_MP3, **{PostFields.TITLE: ["a", "b"]})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error['field'] == PostFields.TITLE
        assert error['code'] == FieldValidationErrorCode.FORMAT_INVALID
