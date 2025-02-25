from rest_framework import status

from bodzify_api.exception.validation.FieldValidationErrorCode import \
    FieldValidationErrorCode
from bodzify_api.model.playlist.Playlist import Fields as PlaylistFields
from bodzify_api.test.view.playlist.children.manual.ManualPlaylistTestCase import \
    ManualPlaylistTestCase
from bodzify_api.view.error.ErrorResponseFields import ErrorResponseFields


class TestCase(ManualPlaylistTestCase):

    def test_value_then_ok(self):
        simpe_playlist = self.model_fixture_factory.create_manual_playlist(name="teuf")

        manual_playlist_name_new = "teuf2"
        data = {PlaylistFields.NAME_PUBLIC: manual_playlist_name_new}
        response = self._put_manual_playlist(uuid=simpe_playlist.uuid, **data)

        assert response.status_code == status.HTTP_200_OK
        assert self.saved_object.name == manual_playlist_name_new

    def test_empty_then_error(self):
        uuid = self.model_fixture_factory.create_manual_playlist(name='foero').uuid

        response = self._put_manual_playlist(uuid=uuid, **{PlaylistFields.NAME_PUBLIC: ""})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert self.bad_request_result_field_errors[0][
            ErrorResponseFields.FieldErrors.CODE] == FieldValidationErrorCode.BLANK.value
        assert self.bad_request_result_field_errors[0][
            ErrorResponseFields.FieldErrors.FIELD] == PlaylistFields.NAME_PUBLIC
