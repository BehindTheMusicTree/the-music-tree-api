from rest_framework import status

from bodzify_api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.test.view.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase


class TestCase(UploadedTrackTestCase):

    def test_filter_not_existing_then_400_bad_request(self):
        invalid_filter_name = 'invalidFilter'
        response = self._list_uploaded_tracks(**{invalid_filter_name: 'invalidFilter'})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error['field'] == invalid_filter_name
        assert error['code'] == FieldValidationErrorCode.INVALID_FILTER
