from rest_framework import status

from bodzify_api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.serializer.model.criteria.input.tree_import.Fields import Fields
from bodzify_api.test.utils.field.body_data.type.NotNullableListBodyDataTestCase import NotNullableListBodyDataTestCase
from bodzify_api.test.view.criteria.GenreTestCase import GenreTestCase


class TestName(GenreTestCase, NotNullableListBodyDataTestCase):
    def test_empty_name_then_400_bad_request(self):
        tree_data = [{Fields.NAME_PUBLIC: "", Fields.CHILDREN: []}]
        response = self._post_genres_tree_import(data={Fields.TREE_PUBLIC: tree_data})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert self.bad_request_result_field_errors[0]["field"] == Fields.NAME_PUBLIC
        assert self.bad_request_result_field_errors[0]["code"] == FieldValidationErrorCode.NAME_EMPTY

    def test_missing_name_then_400_bad_request(self):
        tree_data = [{Fields.CHILDREN: []}]  # Missing name field
        response = self._post_genres_tree_import(data={Fields.TREE_PUBLIC: tree_data})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert self.bad_request_result_field_errors[0]["field"] == Fields.NAME_PUBLIC
        assert self.bad_request_result_field_errors[0]["code"] == FieldValidationErrorCode.FORMAT_INVALID

    def test_duplicate_values_then_400_bad_request(self):
        data = [{Fields.NAME_PUBLIC: "Rock", Fields.CHILDREN: []},
                {Fields.NAME_PUBLIC: "Rock", Fields.CHILDREN: []}]

        response = self._post_genres_tree_import(data={Fields.TREE_PUBLIC: data})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert self.bad_request_result_field_errors[0]["field"] == Fields.TREE_PUBLIC
        assert self.bad_request_result_field_errors[0]["code"] == FieldValidationErrorCode.TREE_VALUE_DUPLICATE
