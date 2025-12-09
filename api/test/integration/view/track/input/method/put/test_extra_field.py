from rest_framework import status

from api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from api.test.integration.view.track.TrackTestCase import TrackTestCase


class TestCase(TrackTestCase):

    def test_extra_field_then_400_bad_request(self):
        extra_field = "extraField"
        track = self.model_fixture_factory.create_track_with_file(title="Foire")

        response = self._put_track(uuid=track.uuid, **{extra_field: "value"})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error['field'] == extra_field
        assert error['code'] == FieldValidationErrorCode.UNKNOWN
