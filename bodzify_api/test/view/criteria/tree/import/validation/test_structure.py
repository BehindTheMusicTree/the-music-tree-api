from rest_framework import status

from bodzify_api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.model.criteria.children.genre.Genre import Genre
from bodzify_api.serializer.model.criteria.input.tree_import.Fields import Fields
from bodzify_api.test.utils.field.body_data.type.list.NotNullableListBodyDataTestCase import NotNullableListBodyDataTestCase
from bodzify_api.test.view.criteria.GenreTestCase import GenreTestCase


class TestStructure(GenreTestCase, NotNullableListBodyDataTestCase):
    def test_multiple_with_one_empty_then_400_bad_request(self):
        data = [{Fields.NAME_PUBLIC: "Rock", Fields.CHILDREN: []}, {}]
        response = self._post_genres_tree_import(data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert self.bad_request_result_field_errors[0]["field"] == Fields.TREE
        assert self.bad_request_result_field_errors[0]["code"] == FieldValidationErrorCode.TREE_MALFORMED

    def test_non_array_input_then_400_bad_request(self):
        response = self._post_genres_tree_import(data={Fields.TREE: {Fields.NAME_PUBLIC: "Rock"}})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert self.bad_request_result_field_errors[0]["field"] == Fields.TREE
        assert self.bad_request_result_field_errors[0]["code"] == FieldValidationErrorCode.TREE_MALFORMED

    def test_malformed_array_then_400_bad_request(self):
        response = self._post_genres_tree_import(data={Fields.TREE: {Fields.NAME_PUBLIC: "Rock"}})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert self.bad_request_result_field_errors[0]["field"] == Fields.TREE
        assert self.bad_request_result_field_errors[0]["code"] == FieldValidationErrorCode.TREE_MALFORMED

    def test_invalid_node_structure_then_400_bad_request(self):
        response = self._post_genres_tree_import(data={Fields.TREE: [{"invalid": "Rock"}]})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert self.bad_request_result_field_errors[0]["field"] == Fields.TREE
        assert self.bad_request_result_field_errors[0]["code"] == FieldValidationErrorCode.TREE_MALFORMED

    def test_children_is_str_then_400_bad_request(self):
        response = self._post_genres_tree_import(
            data={Fields.TREE: [{Fields.NAME_PUBLIC: "Rock", Fields.CHILDREN: "invalid"}]})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert self.bad_request_result_field_errors[0]["field"] == Fields.CHILDREN
        assert self.bad_request_result_field_errors[0]["code"] == FieldValidationErrorCode.TREE_MALFORMED

    def test_children_is_none_then_ok(self):
        response = self._post_genres_tree_import(
            data={Fields.TREE: [{Fields.NAME_PUBLIC: "Rock", Fields.CHILDREN: None}]})

        assert response.status_code == status.HTTP_201_CREATED
        genres = Genre.objects.filter(user=self.test_user1)
        assert genres.count() == 1
        genre = genres.first()
        assert genre is not None
        assert genre.name == "Rock"
        assert genre.parent is None

    def test_children_is_empty_list_then_ok(self):
        response = self._post_genres_tree_import(
            data={Fields.TREE: [{Fields.NAME_PUBLIC: "Rock", Fields.CHILDREN: []}]})

        assert response.status_code == status.HTTP_201_CREATED
        genres = Genre.objects.filter(user=self.test_user1)
        assert genres.count() == 1
        genre = genres.first()
        assert genre is not None
        assert genre.name == "Rock"
        assert genre.parent is None

    def test_missing_children_then_ok(self):
        tree_data = [{Fields.NAME_PUBLIC: "Rock"}]  # No children field
        response = self._post_genres_tree_import(data={Fields.TREE: tree_data})
        assert response.status_code == status.HTTP_201_CREATED
        genres = Genre.objects.filter(user=self.test_user1)
        assert genres.count() == 1
        genre = genres.first()
        assert genre is not None
        assert genre.name == "Rock"
        assert genre.parent is None

    def test_null_children_then_ok(self):
        tree_data = [{Fields.NAME_PUBLIC: "Rock", Fields.CHILDREN: None}]  # Null children
        response = self._post_genres_tree_import(data={Fields.TREE: tree_data})
        assert response.status_code == status.HTTP_201_CREATED
        genres = Genre.objects.filter(user=self.test_user1)
        assert genres.count() == 1
        genre = genres.first()
        assert genre is not None
        assert genre.name == "Rock"
        assert genre.parent is None

    def test_mixed_children_styles_then_ok(self):
        tree_data = [
            {Fields.NAME_PUBLIC: "Rock"},  # No children
            {Fields.NAME_PUBLIC: "Jazz", Fields.CHILDREN: None},  # Null children
            {Fields.NAME_PUBLIC: "Metal", Fields.CHILDREN: []},  # Empty list
            {Fields.NAME_PUBLIC: "Punk", Fields.CHILDREN: [{Fields.NAME_PUBLIC: "Hardcore"}]}  # With children
        ]
        response = self._post_genres_tree_import(data={Fields.TREE: tree_data})
        assert response.status_code == status.HTTP_201_CREATED
        genres = Genre.objects.filter(user=self.test_user1)
        assert genres.count() == 5  # 4 roots + 1 child
        assert genres.filter(name="Rock").exists()
        assert genres.filter(name="Jazz").exists()
        assert genres.filter(name="Metal").exists()
        assert genres.filter(name="Punk").exists()
        assert genres.filter(name="Hardcore").exists()
        hardcore = genres.get(name="Hardcore")
        assert hardcore.parent is not None
        assert hardcore.parent.name == "Punk"
