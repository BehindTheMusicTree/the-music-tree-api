from rest_framework import status

from bodzify_api.serializer.model.lib_track.input.post.Fields import Fields
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase
from bodzify_api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode


class TestCase(LibTrackTestCase):

    def test_duplicate_fingerprint_and_must_cancel_if_duplicate_fingerprint_then_bad_request(self):
        data = {Fields.TRACK_FILE_FINGERPRINT_MUST_BE_UNIQUE: True}
        response = self._post_lib_track_with_generic_sample_no_tags(**data)
        response = self._post_lib_track_with_generic_sample_no_tags(**data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error[ErrorResponseFields.FieldErrors.FIELD] == Fields.TRACK_FILE_PUBLIC
        assert error[ErrorResponseFields.FieldErrors.CODE] == FieldValidationErrorCode.DUPLICATE_FINGERPRINT

    def test_not_duplicate_fingerprint_and_must_cancel_if_duplicate_fingerprint_then_ok(self):
        data = {Fields.TRACK_FILE_FINGERPRINT_MUST_BE_UNIQUE: True}
        response = self._post_lib_track_with_generic_sample_no_tags(**data)
        response = self._post_lib_track_with_queenshowmustgoon(**data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_duplicate_fingerprint_and_not_must_cancel_if_duplicate_fingerprint_then_ok(self):
        data = {Fields.TRACK_FILE_FINGERPRINT_MUST_BE_UNIQUE: False}
        response = self._post_lib_track_with_generic_sample_no_tags(**data)
        response = self._post_lib_track_with_generic_sample_no_tags(**data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_duplicate_fingerprint_and_must_cancel_if_duplicate_fingerprint_not_provided_then_ok(self):
        data = {Fields.TRACK_FILE_FINGERPRINT_MUST_BE_UNIQUE: False}
        response = self._post_lib_track_with_generic_sample_no_tags(**data)
        response = self._post_lib_track_with_generic_sample_no_tags(**data)
        assert response.status_code == status.HTTP_201_CREATED
