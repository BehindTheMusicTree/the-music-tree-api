from rest_framework import status

from bodzify_api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.serializer.model.playlist.children.manual.input.Fields import Fields
from bodzify_api.test.view.playlist.children.manual.ManualPlaylistTestCase import ManualPlaylistTestCase


class TestCase(ManualPlaylistTestCase):

    def test_value_then_ok(self):
        response = self._post_manual_playlist(**{Fields.NAME_PUBLIC: "a"})

        assert response.status_code == status.HTTP_201_CREATED

    def test_empty_then_400(self):
        response = self._post_manual_playlist(**{Fields.NAME_PUBLIC: ""})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert self.bad_request_result_field_errors[0][
            'code'] == FieldValidationErrorCode.BLANK
        assert self.bad_request_result_field_errors[0]['field'] == Fields.NAME_PUBLIC

    def test_not_provided_then_400(self):
        response = self._post_manual_playlist(**{})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert self.bad_request_result_field_errors[0][
            'code'] == FieldValidationErrorCode.REQUIRED
        assert self.bad_request_result_field_errors[0]['field'] == Fields.NAME_PUBLIC
