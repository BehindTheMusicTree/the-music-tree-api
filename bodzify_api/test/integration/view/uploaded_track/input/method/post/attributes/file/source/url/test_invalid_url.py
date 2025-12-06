from rest_framework import status

from bodzify_api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.test.utils.uploaded_track.UploadedTrackDownloadTestUrl import UploadedTrackDownloadTestUrl
from bodzify_api.test.integration.view.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase
from bodzify_api.serializer.model.uploaded_track.input.post.Fields import Fields


class TestCase(UploadedTrackTestCase):

    def test_invalid_url_then_400_bad_request(self):
        response = self._post_uploaded_track_from_url(UploadedTrackDownloadTestUrl.INVALID)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error['field'] == Fields.TRACK_FILE_PUBLIC
        assert error['code'] == FieldValidationErrorCode.URL_NOT_FOUND
