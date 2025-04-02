from rest_framework import status

from bodzify_api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.test.utils.lib_track.LibTrackTestUrl import LibTracTestkUrl
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase
from bodzify_api.serializer.model.lib_track.input.post.Fields import Fields


class TestCase(LibTrackTestCase):

    def test_invalid_url_then_400_bad_request(self):
        response = self._post_lib_track_from_url(LibTracTestkUrl.INVALID)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error['field'] == Fields.TRACK_FILE_PUBLIC
        assert error['code'] == FieldValidationErrorCode.URL_NOT_FOUND
