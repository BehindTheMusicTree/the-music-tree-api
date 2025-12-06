from rest_framework import status

from bodzify_api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.test.integration.view.playlist.children.manual.ManualPlaylistTestCase import ManualPlaylistTestCase


class TestCase(ManualPlaylistTestCase):

    def test_extra_field_then_400_bad_request(self):
        manual_playlist = self.model_fixture_factory.create_manual_playlist(name="teuf")

        non_existing_field = 'nonExistingField'
        response = self._put_manual_playlist(uuid=manual_playlist.uuid, **{non_existing_field: 'value'})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert self.bad_request_result_field_errors[0][
            'code'] == FieldValidationErrorCode.UNKNOWN
        assert self.bad_request_result_field_errors[0]['field'] == non_existing_field
