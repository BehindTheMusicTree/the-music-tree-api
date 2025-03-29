from rest_framework import status

from bodzify_api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.test.view.criteria.GenreTestCase import GenreTestCase


class TestValidation(GenreTestCase):
    def test_no_data_then_400_bad_request(self):
        response = self._post_genres_tree_import()
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert self.bad_request_result_field_errors[0]["field"] == "data"
        assert self.bad_request_result_field_errors[0]["code"] == FieldValidationErrorCode.REQUIRED

    def test_empty_array_then_400_bad_request(self):
        data = []
        response = self._post_genres_tree_import(data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert self.bad_request_result_field_errors[0]["field"] == "data"
        assert self.bad_request_result_field_errors[0]["code"] == FieldValidationErrorCode.REQUIRED

    def test_empty_name_then_400_bad_request(self):
        tree_data = [{"name": "", "children": []}]
        response = self._post_genres_tree_import(tree_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert self.bad_request_result_field_errors[0]["field"] == "name"
        assert self.bad_request_result_field_errors[0]["code"] == FieldValidationErrorCode.NAME_EMPTY
        assert "Name cannot be empty" in self.bad_request_result_field_errors[0]["message"]

    def test_missing_name_then_400_bad_request(self):
        tree_data = [{"children": []}]  # Missing name field
        response = self._post_genres_tree_import(tree_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert self.bad_request_result_field_errors[0]["field"] == "data"
        assert self.bad_request_result_field_errors[0]["code"] == FieldValidationErrorCode.FORMAT_INVALID
        assert "must have a 'name' field" in self.bad_request_result_field_errors[0]["message"]

    def test_non_array_input_then_400_bad_request(self):
        response = self._post_genres_tree_import({"name": "Rock"})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert self.bad_request_result_field_errors[0]["field"] == "data"
        assert self.bad_request_result_field_errors[0]["code"] == FieldValidationErrorCode.FORMAT_INVALID
        assert "Input must be an array" in self.bad_request_result_field_errors[0]["message"]

    def test_invalid_node_structure_then_400_bad_request(self):
        response = self._post_genres_tree_import([{"invalid": "Rock"}])
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert self.bad_request_result_field_errors[0]["field"] == "data"
        assert self.bad_request_result_field_errors[0]["code"] == FieldValidationErrorCode.FORMAT_INVALID
        assert "must have a 'name' field" in self.bad_request_result_field_errors[0]["message"]

    def test_invalid_children_structure_then_400_bad_request(self):
        response = self._post_genres_tree_import([{"name": "Rock", "children": "invalid"}])
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert self.bad_request_result_field_errors[0]["field"] == "data"
        assert self.bad_request_result_field_errors[0]["code"] == FieldValidationErrorCode.FORMAT_INVALID
        assert "Children must be an array" in self.bad_request_result_field_errors[0]["message"]
