
from django.urls import reverse
from rest_framework import status

from bodzify_api.serializer.schema.model.criteria.input.Fields import Fields as CriteriaPostFields
from bodzify_api.test.view.criteria.GenreTestCase import GenreTestCase
from bodzify_api.validator.FieldValidationErrorCode import FieldValidationErrorCode


class TestCase(GenreTestCase):

    def test_duplicate_fields_on_content_type_json_then_400(self):
        json_str = '{"name": "test", "name": "test2"}'
        response = self.client.post(
            reverse(self.list_endpoint),
            json_str.encode('utf-8'),
            content_type='application/json',
            HTTP_ACCEPT='application/json'
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        self._set_bad_request_result(response)
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error[ErrorResponseFields.FIELD] == CriteriaPostFields.NAME_PUBLIC
        assert error[ErrorResponseFields.CODE] == FieldValidationErrorCode.FIELD_DUPLICATE.value
