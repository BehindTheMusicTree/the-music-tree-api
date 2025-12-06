from rest_framework import status

from bodzify_api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.test.integration.view.playlist.children.manual.ManualPlaylistTestCase import ManualPlaylistTestCase


class TestCase(ManualPlaylistTestCase):

    def test_filter_not_existing_then_400_bad_request(self):
        invalid_filter = 'invalidfilter'
        response = self._get_manual_playlists(**{invalid_filter: 'a'})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert self.bad_request_result_field_errors[0]['field'] == invalid_filter
        assert self.bad_request_result_field_errors[0][
            'code'] == FieldValidationErrorCode.INVALID_FILTER
