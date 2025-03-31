from typing import cast
from rest_framework import status
import pytest

from bodzify_api import settings
from bodzify_api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.model.criteria.children.genre.Genre import Genre
from bodzify_api.serializer.model.criteria.input.tree_import.Fields import Fields
from bodzify_api.test.utils.field.body_data.type.NotNullableListBodyDataTestCase import NotNullableListBodyDataTestCase
from bodzify_api.test.view.criteria.GenreTestCase import GenreTestCase


class TestValidation(GenreTestCase, NotNullableListBodyDataTestCase):
    def test_no_data_then_400_bad_request(self):
        response = self._post_genres_tree_import()
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert self.bad_request_result_field_errors[0]["field"] == Fields.TREE_INTERNAL
        assert self.bad_request_result_field_errors[0]["code"] == FieldValidationErrorCode.REQUIRED

    def test_empty_then_400_bad_request(self):
        data = []
        response = self._post_genres_tree_import(data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert self.bad_request_result_field_errors[0]["field"] == Fields.TREE_INTERNAL
        assert self.bad_request_result_field_errors[0]["code"] == FieldValidationErrorCode.REQUIRED

    def test_one_too_large_then_400_bad_request(self):
        root = {Fields.NAME_PUBLIC: "Root1", Fields.CHILDREN: []}
        for i in range(settings.CRITERIA_TREE_IMPORT_MAX_TOTAL_COUNT - 1):
            root[Fields.CHILDREN].append({
                Fields.NAME_PUBLIC: f"Child {i}",
                Fields.CHILDREN: []
            })

        data = [root, {Fields.NAME_PUBLIC: "Root2", Fields.CHILDREN: []}]
        response = self._post_genres_tree_import(data={Fields.TREE_PUBLIC: data})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert self.bad_request_result_field_errors[0]["field"] == Fields.TREE_PUBLIC
        assert self.bad_request_result_field_errors[0]["code"] == FieldValidationErrorCode.TREE_TOO_LARGE

    @pytest.mark.slow
    def test_multiple_with_one_too_large_then_400_bad_request(self):
        # Create a tree with max_count - 1 children for the first root
        data = [{Fields.NAME_PUBLIC: 'Rock', Fields.CHILDREN: [{Fields.NAME_PUBLIC: f'Child {i}', Fields.CHILDREN: []}
                                                               for i in range(settings.CRITERIA_TREE_IMPORT_MAX_TOTAL_COUNT - 1)]}]

        # Add an "Extra Child" to exceed the limit
        data[0][Fields.CHILDREN].append({Fields.NAME_PUBLIC: 'Extra Child', Fields.CHILDREN: []})

        response = self._post_genres_tree_import(data={Fields.TREE_INTERNAL: data})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert self.bad_request_result_field_errors[0]["field"] == Fields.TREE_INTERNAL
        assert self.bad_request_result_field_errors[0]["code"] == FieldValidationErrorCode.TREE_TOO_LARGE

    @pytest.mark.slow
    def test_largest_then_ok(self):
        # Create a wide tree structure instead of a deep one
        root = {Fields.NAME_PUBLIC: "Root", Fields.CHILDREN: []}
        for i in range(settings.CRITERIA_TREE_IMPORT_MAX_TOTAL_COUNT - 1):
            root[Fields.CHILDREN].append({
                Fields.NAME_PUBLIC: f"Child {i}",
                Fields.CHILDREN: []
            })

        data = [root]
        response = self._post_genres_tree_import(data={Fields.TREE_INTERNAL: data})
        assert response.status_code == status.HTTP_201_CREATED
        genres_count = Genre.objects.filter(user=self.test_user1).count()
        assert genres_count == settings.CRITERIA_TREE_IMPORT_MAX_TOTAL_COUNT

    def test_multiple_with_one_empty_then_400_bad_request(self):
        data = [{Fields.NAME_PUBLIC: "Rock", Fields.CHILDREN: []},
                {}]
        response = self._post_genres_tree_import(data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert self.bad_request_result_field_errors[0]["field"] == Fields.TREE_INTERNAL
        assert self.bad_request_result_field_errors[0]["code"] == FieldValidationErrorCode.TREE_MALFORMED

    def test_empty_name_then_400_bad_request(self):
        tree_data = [{Fields.NAME_PUBLIC: "", Fields.CHILDREN: []}]
        response = self._post_genres_tree_import(data={Fields.TREE_INTERNAL: tree_data})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert self.bad_request_result_field_errors[0]["field"] == Fields.NAME_PUBLIC
        assert self.bad_request_result_field_errors[0]["code"] == FieldValidationErrorCode.NAME_EMPTY

    def test_missing_name_then_400_bad_request(self):
        tree_data = [{Fields.CHILDREN: []}]  # Missing name field
        response = self._post_genres_tree_import(data={Fields.TREE_INTERNAL: tree_data})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert self.bad_request_result_field_errors[0]["field"] == Fields.NAME_PUBLIC
        assert self.bad_request_result_field_errors[0]["code"] == FieldValidationErrorCode.FORMAT_INVALID

    def test_non_array_input_then_400_bad_request(self):
        response = self._post_genres_tree_import(data={Fields.TREE_INTERNAL: {Fields.NAME_PUBLIC: "Rock"}})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert self.bad_request_result_field_errors[0]["field"] == Fields.TREE_INTERNAL
        assert self.bad_request_result_field_errors[0]["code"] == FieldValidationErrorCode.TREE_MALFORMED

    def test_malformed_array_then_400_bad_request(self):
        response = self._post_genres_tree_import(data={Fields.TREE_INTERNAL: {Fields.NAME_PUBLIC: "Rock"}})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert self.bad_request_result_field_errors[0]["field"] == Fields.TREE_INTERNAL
        assert self.bad_request_result_field_errors[0]["code"] == FieldValidationErrorCode.TREE_MALFORMED

    def test_invalid_node_structure_then_400_bad_request(self):
        response = self._post_genres_tree_import(data={Fields.TREE_INTERNAL: [{"invalid": "Rock"}]})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert self.bad_request_result_field_errors[0]["field"] == Fields.TREE_INTERNAL
        assert self.bad_request_result_field_errors[0]["code"] == FieldValidationErrorCode.TREE_MALFORMED

    def test_invalid_children_structure_then_400_bad_request(self):
        response = self._post_genres_tree_import(
            data={Fields.TREE_INTERNAL: [{Fields.NAME_PUBLIC: "Rock", Fields.CHILDREN: "invalid"}]})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert self.bad_request_result_field_errors[0]["field"] == Fields.CHILDREN
        assert self.bad_request_result_field_errors[0]["code"] == FieldValidationErrorCode.TREE_MALFORMED

    def test_duplicate_values_then_400_bad_request(self):
        data = [{Fields.NAME_PUBLIC: "Rock", Fields.CHILDREN: []},
                {Fields.NAME_PUBLIC: "Rock", Fields.CHILDREN: []}]

        response = self._post_genres_tree_import(data={Fields.TREE_INTERNAL: data})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert self.bad_request_result_field_errors[0]["field"] == Fields.TREE_INTERNAL
        assert self.bad_request_result_field_errors[0]["code"] == FieldValidationErrorCode.TREE_VALUE_DUPLICATE

    def test_import_new_tree_then_overwrites_existing(self):
        self.model_fixture_factory.create_genre(name="Old Rock")

        tree_data = [{Fields.NAME_PUBLIC: "New Rock", Fields.CHILDREN: []}]
        response = self._post_genres_tree_import(data={Fields.TREE_INTERNAL: tree_data})

        assert response.status_code == status.HTTP_201_CREATED

        genres = Genre.objects.filter(user=self.test_user1)
        assert genres.count() == 1
        assert cast(Genre, genres.first()).name == "New Rock"

    def test_error_during_import_then_rollback(self):
        initial_genre = self.model_fixture_factory.create_genre(name="Initial Rock")
        initial_genre_id = initial_genre.uuid

        tree_data = [
            {
                Fields.NAME_PUBLIC: "Rock",
                Fields.CHILDREN: [
                    {Fields.NAME_PUBLIC: "Punk", Fields.CHILDREN: []},
                    {Fields.NAME_PUBLIC: "Rock", Fields.CHILDREN: []}  # This will cause a duplicate name error
                ]
            }
        ]
        response = self._post_genres_tree_import(data={Fields.TREE_INTERNAL: tree_data})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert self.bad_request_result_field_errors[0]["field"] == Fields.NAME_PUBLIC
        assert self.bad_request_result_field_errors[0]["code"] == FieldValidationErrorCode.NAME_DUPLICATE
        assert Fields.NAME_PUBLIC in self.bad_request_result_field_errors[0]["message"]

        # Verify that the initial genre still exists and no new genres were created
        genres = Genre.objects.filter(user=self.test_user1)
        assert genres.count() == 1
        genre = cast(Genre, genres.first())
        assert genre.uuid == initial_genre_id
        assert genre.name == "Initial Rock"

    def test_missing_children_then_ok(self):
        tree_data = [{Fields.NAME_PUBLIC: "Rock"}]  # No children field
        response = self._post_genres_tree_import(data={Fields.TREE_INTERNAL: tree_data})
        assert response.status_code == status.HTTP_201_CREATED
        genres = Genre.objects.filter(user=self.test_user1)
        assert genres.count() == 1
        genre = genres.first()
        assert genre is not None
        assert genre.name == "Rock"
        assert genre.parent is None

    def test_null_children_then_ok(self):
        tree_data = [{Fields.NAME_PUBLIC: "Rock", Fields.CHILDREN: None}]  # Null children
        response = self._post_genres_tree_import(data={Fields.TREE_INTERNAL: tree_data})
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
        response = self._post_genres_tree_import(data={Fields.TREE_INTERNAL: tree_data})
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
