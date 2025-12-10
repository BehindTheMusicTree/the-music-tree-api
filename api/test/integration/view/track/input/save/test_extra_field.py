from rest_framework import status

from api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from api.serializer.model.track.input.Fields import Fields as PostFields
from api.test.integration.view.track.TrackTestCase import TrackTestCase


class TestCase(TrackTestCase):

    def test_extra_field_then_400_bad_request(self):
        extraField = "extraField"
        data = {PostFields.TITLE: "Rock", extraField: "extra_value"}
        response = self._post_track(**data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error['field'] == extraField
        assert error['code'] == FieldValidationErrorCode.UNKNOWN
