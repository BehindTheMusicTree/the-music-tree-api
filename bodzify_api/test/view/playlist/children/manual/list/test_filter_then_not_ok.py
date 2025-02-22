from rest_framework import status

from bodzify_api.test.view.artist.ArtistTestCase import ArtistTestCase
from bodzify_api.test.view.playlist.children.manual.ManualPlaylistTestCase import ManualPlaylistTestCase
from bodzify_api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.view.error.ErrorResponseFields import ErrorResponseFields


class TestCase(ManualPlaylistTestCase):

    def test_filter_not_existing_then_error(self):
        invalid_filter = 'invalidfilter'
        response = self._get_manual_playlists(**{invalid_filter: 'a'})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert self.bad_request_result_field_errors[0][ErrorResponseFields.FieldErrors.FIELD] == invalid_filter
        assert self.bad_request_result_field_errors[0][
            ErrorResponseFields.FieldErrors.CODE] == FieldValidationErrorCode.INVALID_FILTER.value
