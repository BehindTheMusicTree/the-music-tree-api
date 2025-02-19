from rest_framework import status

from bodzify_api.serializer.schema.model.playlist.children.manual.input.Fields import Fields
from bodzify_api.test.view.playlist.children.manual.ManualPlaylistTestCase import ManualPlaylistTestCase
from bodzify_api.validator.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.view.error.ErrorResponseFields import ErrorResponseFields


class TestCase(ManualPlaylistTestCase):

    def test_value_then_ok(self):
        response = self._post_manual_playlist(**{Fields.NAME_PUBLIC: "a"})

        assert response.status_code == status.HTTP_201_CREATED

    def test_empty_then_error(self):
        response = self._post_manual_playlist(**{Fields.NAME_PUBLIC: ""})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert self.bad_request_result_field_errors[0][
            ErrorResponseFields.FieldErrors.CODE] == FieldValidationErrorCode.BLANK.value
        assert self.bad_request_result_field_errors[0][ErrorResponseFields.FieldErrors.FIELD] == Fields.NAME_PUBLIC

    def test_not_provided_then_error(self):
        response = self._post_manual_playlist(**{})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert self.bad_request_result_field_errors[0][
            ErrorResponseFields.FieldErrors.CODE] == FieldValidationErrorCode.REQUIRED.value
        assert self.bad_request_result_field_errors[0][ErrorResponseFields.FieldErrors.FIELD] == Fields.NAME_PUBLIC
