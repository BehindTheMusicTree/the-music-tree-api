from rest_framework import status

from bodzify_api.serializer.schema.model.lib_track.input.extract import Fields as ExtractFields
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase
from bodzify_api.validator.FieldValidationErrorCode import FieldValidationErrorCode


class TestCase(LibTrackTestCase):

    def test(self):
        data = {ExtractFields.URL: "https://wrong-url_OIJOIEFHPOEIHFEPOFIHEOFIH.mp3"}
        response = self._extract(**data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error[ErrorResponseFields.FIELD] == ExtractFields.URL
        assert error['code'] == FieldValidationErrorCode.INVALID_URL
