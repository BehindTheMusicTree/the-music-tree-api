from rest_framework import status

from bodzify_api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.serializer.AppInputSerializer import AppInputSerializer
from bodzify_api.test.integration.view.playlist.children.manual.ManualPlaylistTestCase import ManualPlaylistTestCase


class TestCase(ManualPlaylistTestCase):

    def test_no_field_specified_then_400_bad_request(self):
        manual_playlist = self.model_fixture_factory.create_manual_playlist(name="Kitchen")

        response = self._put_manual_playlist(uuid=manual_playlist.uuid)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert self.bad_request_result_field_errors[0][
            'code'] == FieldValidationErrorCode.NO_UPDATES
        assert self.bad_request_result_field_errors[0][
            'field'] == AppInputSerializer.REQUEST_FIELD
