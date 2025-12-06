from rest_framework import status

from bodzify_api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.test.integration.view.playlist.children.manual.ManualPlaylistTestCase import ManualPlaylistTestCase


class TestCase(ManualPlaylistTestCase):

    def test_extra_field_then_400_bad_request(self):
        invalid_field = 'nonExistingField'
        response = self._post_manual_playlist(**{invalid_field: 'oifjqoif'})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert self.bad_request_result_field_errors[0]['field'] == invalid_field
        assert self.bad_request_result_field_errors[0][
            'code'] == FieldValidationErrorCode.UNKNOWN
