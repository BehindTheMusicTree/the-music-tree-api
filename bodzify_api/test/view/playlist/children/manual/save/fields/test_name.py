from rest_framework import status

from bodzify_api import settings
from bodzify_api.serializer.schema.model.criteria.input.post import Fields
from bodzify_api.test.view.playlist.children.manual.ManualPlaylistTestCase import ManualPlaylistTestCase
from bodzify_api.validator.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.view.error.ErrorResponseFields import ErrorResponseFields


class TestCase(ManualPlaylistTestCase):

    def test_multiple_values_then_error(self):
        response = self._post_manual_playlist(**{Fields.NAME_PUBLIC: ["value", "value2"]})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error[ErrorResponseFields.FIELD] == Fields.NAME_PUBLIC
        assert error[ErrorResponseFields.CODE] == FieldValidationErrorCode.INVALID_FORMAT.value

    def test_longest_then_ok(self):
        response = self._post_manual_playlist(**{Fields.NAME_PUBLIC: "a" * settings.MANUAL_PLAYLIST_NAME_LEN_MAX})
        assert response.status_code == status.HTTP_201_CREATED

    def test_error_when_too_long(self):
        response = self._post_manual_playlist(
            **{Fields.NAME_PUBLIC: "a" * (settings.MANUAL_PLAYLIST_NAME_LEN_MAX + 1)})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error[ErrorResponseFields.FIELD] == Fields.NAME_PUBLIC
        assert error[ErrorResponseFields.CODE] == FieldValidationErrorCode.INVALID_FORMAT.value

    def test_already_exists_then_error(self):
        response = self._post_manual_playlist(**{Fields.NAME_PUBLIC: "value"})
        assert response.status_code == status.HTTP_201_CREATED
        response = self._post_manual_playlist(**{Fields.NAME_PUBLIC: "value"})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error[ErrorResponseFields.FIELD] == Fields.NAME_PUBLIC
        assert error[ErrorResponseFields.CODE] == FieldValidationErrorCode.NAME_DUPLICATE.value
