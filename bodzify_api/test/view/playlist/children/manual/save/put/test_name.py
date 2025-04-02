from rest_framework import status

from bodzify_api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.model.playlist.Playlist import Fields as PlayListFields
from bodzify_api.test.view.playlist.children.manual.ManualPlaylistTestCase import ManualPlaylistTestCase


class TestCase(ManualPlaylistTestCase):

    def test_value_then_ok(self):
        simpe_playlist = self.model_fixture_factory.create_manual_playlist(name="teuf")

        manual_playlist_name_new = "teuf2"
        data = {PlayListFields.NAME_PUBLIC: manual_playlist_name_new}
        response = self._put_manual_playlist(uuid=simpe_playlist.uuid, **data)

        assert response.status_code == status.HTTP_200_OK
        assert self.saved_object.name == manual_playlist_name_new

    def test_empty_then_400_bad_request(self):
        uuid = self.model_fixture_factory.create_manual_playlist(name='foero').uuid

        response = self._put_manual_playlist(uuid=uuid, **{PlayListFields.NAME_PUBLIC: ""})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert self.bad_request_result_field_errors[0][
            'code'] == FieldValidationErrorCode.BLANK
        assert self.bad_request_result_field_errors[0][
            'field'] == PlayListFields.NAME_PUBLIC
