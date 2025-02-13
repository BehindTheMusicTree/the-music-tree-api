from rest_framework import status

from bodzify_api.serializer.schema.model.criteria.input.post import Fields as PostFields
from bodzify_api.test.view.playlist.children.manual.ManualPlaylistTestCase import ManualPlaylistTestCase
from bodzify_api.view.error.FieldValidationErrorCode import FieldValidationErrorCode


class TestCase(ManualPlaylistTestCase):

    def test_extra_field_then_error(self):
        response = self._post_manual_playlist(**{PostFields.NAME_PUBLIC: "Rock", "extra_field": "extra_value"})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error['field'] == 'extra_field'
        assert error['code'] == FieldValidationErrorCode.UNKNOWN
