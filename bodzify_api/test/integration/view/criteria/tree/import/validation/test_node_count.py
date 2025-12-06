from rest_framework import status
import pytest

from bodzify_api import settings
from bodzify_api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.model.criteria.children.genre.Genre import Genre
from bodzify_api.serializer.model.criteria.input.tree_import.Fields import Fields
from bodzify_api.test.integration.view.criteria.GenreTestCase import GenreTestCase


class TestNodeCount(GenreTestCase):
    def test_no_data_then_400_bad_request(self):
        response = self._post_genres_tree_import(data={Fields.TREE: None})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert self.bad_request_result_field_errors[0]["field"] == Fields.TREE
        assert self.bad_request_result_field_errors[0]["code"] == FieldValidationErrorCode.REQUIRED

    def test_empty_then_400_bad_request(self):
        response = self._post_genres_tree_import(data={Fields.TREE: []})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert self.bad_request_result_field_errors[0]["field"] == Fields.TREE
        assert self.bad_request_result_field_errors[0]["code"] == FieldValidationErrorCode.REQUIRED

    @pytest.mark.slow
    def test_one_too_large_then_400_bad_request(self):
        root = {Fields.NAME_PUBLIC: "Root1", Fields.CHILDREN: []}
        for i in range(settings.CRITERIA_TREE_IMPORT_MAX_TOTAL_COUNT - 1):
            root[Fields.CHILDREN].append({
                Fields.NAME_PUBLIC: f"Child {i}",
                Fields.CHILDREN: []
            })

        data = [root, {Fields.NAME_PUBLIC: "Root2", Fields.CHILDREN: []}]
        response = self._post_genres_tree_import(data={Fields.TREE: data})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert self.bad_request_result_field_errors[0]["field"] == Fields.TREE
        assert self.bad_request_result_field_errors[0]["code"] == FieldValidationErrorCode.TREE_TOO_LARGE

    @pytest.mark.slow
    def test_multiple_with_one_too_large_then_400_bad_request(self):
        data = [{Fields.NAME_PUBLIC: 'Rock', Fields.CHILDREN: [
            {Fields.NAME_PUBLIC: f'Child {i}', Fields.CHILDREN: []}
            for i in range(settings.CRITERIA_TREE_IMPORT_MAX_TOTAL_COUNT - 1)]}]

        data[0][Fields.CHILDREN].append({Fields.NAME_PUBLIC: 'Extra Child', Fields.CHILDREN: []})

        response = self._post_genres_tree_import(data={Fields.TREE: data})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert self.bad_request_result_field_errors[0]["field"] == Fields.TREE
        assert self.bad_request_result_field_errors[0]["code"] == FieldValidationErrorCode.TREE_TOO_LARGE

    @pytest.mark.slow
    def test_largest_then_ok(self):
        root = {Fields.NAME_PUBLIC: "Root", Fields.CHILDREN: []}
        for i in range(3000):
            root[Fields.CHILDREN].append({
                Fields.NAME_PUBLIC: f"Child {i}",
                Fields.CHILDREN: []
            })

        data = [root]
        response = self._post_genres_tree_import(data={Fields.TREE: data})
        assert response.status_code == status.HTTP_201_CREATED
        genres_count = Genre.objects.filter(user=self.test_user1).count()
        assert genres_count == 3001
