from rest_framework import status

from bodzify_api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.serializer.PutSerializer import PutSerializer
from bodzify_api.test.integration.view.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase


class TestCase(UploadedTrackTestCase):

    def test_no_field_specified_then_400_bad_request(self):
        uploaded_track = self.model_fixture_factory.create_uploaded_track_with_file(title="Polo")

        response = self._put_uploaded_track(uuid=uploaded_track.uuid)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        error = self.bad_request_result_field_errors[0]
        assert error['field'] == PutSerializer.REQUEST_FIELD
        assert error['code'] == FieldValidationErrorCode.NO_UPDATES
