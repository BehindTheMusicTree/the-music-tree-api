from rest_framework import status

from bodzify_api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.serializer.PutSerializer import PutSerializer
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase
from bodzify_api.view.error.ErrorResponseFields import ErrorResponseFields


class TestCase(LibTrackTestCase):

    def test_no_field_specified_then_400(self):
        lib_track = self.model_fixture_factory.create_lib_track_with_file(title="Polo")

        response = self._put_lib_track(uuid=lib_track.uuid)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        error = self.bad_request_result_field_errors[0]
        assert error[ErrorResponseFields.FieldErrors.FIELD] == PutSerializer.REQUEST_FIELD
        assert error['code'] == FieldValidationErrorCode.NO_UPDATES
