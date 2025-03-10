from django.urls import reverse
from rest_framework import status

from bodzify_api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.serializer.model.criteria.input.Fields import Fields as CriteriaPostFields
from bodzify_api.test.view.criteria.GenreTestCase import GenreTestCase


class TestJsonDuplicateFields(GenreTestCase):

    def test_duplicate_fields_on_json_post_then_400(self):
        raw_json = '{"name": "test", "name": "test2"}'
        response = self.api_client.post(path=reverse(self.list_endpoint),
                                        data=raw_json,
                                        format=None,
                                        content_type='application/json',
                                        handle_response=self._set_results)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        self._set_error_response_result(response)
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error['field'] == CriteriaPostFields.NAME_PUBLIC
        assert error['code'] == FieldValidationErrorCode.DUPLICATE

    def test_duplicate_fields_on_json_put_then_400(self):
        genre = self.model_fixture_factory.create_genre(name="rock")

        raw_json = '{"name": "test", "name": "test2"}'
        response = self.api_client.put(path=reverse(self.detail_endpoint, kwargs={'pk': genre.uuid}),
                                       data=raw_json,
                                       format=None,
                                       content_type='application/json',
                                       handle_response=self._set_results)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        self._set_error_response_result(response)
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error['field'] == CriteriaPostFields.NAME_PUBLIC
        assert error['code'] == FieldValidationErrorCode.DUPLICATE

    def test_duplicate_fields_on_json_patch_then_400(self):
        # PATCH is not supported
        pass
