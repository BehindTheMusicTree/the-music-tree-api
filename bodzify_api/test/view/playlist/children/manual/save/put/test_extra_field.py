from rest_framework import status

from bodzify_api.test.view.playlist.children.manual.ManualPlaylistTestCase import ManualPlaylistTestCase
from bodzify_api.validator.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.view.error.ErrorResponseFields import ErrorResponseFields


class TestCase(ManualPlaylistTestCase):

    def test_extra_field_then_error(self):
        manual_playlist = self.model_fixture_factory.create_manual_playlist(name="teuf")
        non_existing_field = 'nonExistingField'
        response = self._put_manual_playlist(uuid=manual_playlist.uuid, **{non_existing_field: 'value'})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert self.bad_request_result_field_errors[0][
            ErrorResponseFields.FieldErrors.CODE] == FieldValidationErrorCode.UNKNOWN_FIELD.value
        assert self.bad_request_result_field_errors[0][ErrorResponseFields.FieldErrors.FIELD] == non_existing_field
