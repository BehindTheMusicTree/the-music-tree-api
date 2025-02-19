from rest_framework import status

from bodzify_api.test.view.playlist.children.manual.ManualPlaylistTestCase import ManualPlaylistTestCase
from bodzify_api.validator.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.view.error.ErrorResponseFields import ErrorResponseFields
from bodzify_api.serializer.schema.model.playlist.children.manual.input.Fields import Fields as PlaylistFields


class TestCase(ManualPlaylistTestCase):

    def test_no_field_specified_then_error(self):
        manual_playlist = self.model_fixture_factory.create_manual_playlist(name="Kitchen")

        response = self._put_manual_playlist(uuid=manual_playlist.uuid)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert self.bad_request_result_field_errors[0][
            ErrorResponseFields.FieldErrors.CODE] == FieldValidationErrorCode.REQUIRED.value
        assert self.bad_request_result_field_errors[0][
            ErrorResponseFields.FieldErrors.FIELD] == PlaylistFields.NAME_PUBLIC
        assert self.bad_request_result_field_errors[0][
            ErrorResponseFields.FieldErrors.CODE] == FieldValidationErrorCode.NO_UPDATES.value
