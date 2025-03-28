from rest_framework import status

from bodzify_api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.model.criteria.children.genre.Genre import Genre
from bodzify_api.test.view.criteria.GenreTestCase import GenreTestCase


class TestErrors(GenreTestCase):
    def test_duplicate_names_then_error(self):
        duplicate_name = "Rock"
        tree_data = [
            {"name": duplicate_name, "children": []},
            {"name": duplicate_name, "children": []}  # Duplicate name
        ]
        response = self._post_genres_tree_import(tree_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert self.bad_request_result_field_errors[0]["field"] == "name"
        assert self.bad_request_result_field_errors[0]["code"] == FieldValidationErrorCode.NAME_DUPLICATE
        assert duplicate_name in self.bad_request_result_field_errors[0]["message"]

    def test_import_overwrites_existing(self):
        # Create initial genre
        self.model_fixture_factory.create_genre(name="Old Rock")

        # Import new tree
        tree_data = [{"name": "New Rock", "children": []}]
        response = self._post_genres_tree_import(tree_data)

        assert response.status_code == status.HTTP_201_CREATED

        # Verify old genre is gone and new one exists
        genres = Genre.objects.filter(user=self.test_user1)
        assert genres.count() == 1
        assert genres.first().name == "New Rock"

    def test_error_during_import_then_rollback(self):
        # Create initial genre
        initial_genre = self.model_fixture_factory.create_genre(name="Initial Rock")
        initial_genre_id = initial_genre.uuid

        # Try to import a tree with a duplicate name that will cause an error
        tree_data = [
            {
                "name": "Rock",
                "children": [
                    {"name": "Punk", "children": []},
                    {"name": "Rock", "children": []}  # This will cause a duplicate name error
                ]
            }
        ]
        response = self._post_genres_tree_import(tree_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert self.bad_request_result_field_errors[0]["field"] == "name"
        assert self.bad_request_result_field_errors[0]["code"] == FieldValidationErrorCode.NAME_DUPLICATE
        assert "already exists for this user" in self.bad_request_result_field_errors[0]["message"]

        # Verify that the initial genre still exists and no new genres were created
        genres = Genre.objects.filter(user=self.test_user1)
        assert genres.count() == 1
        genre = genres.first()
        assert genre.uuid == initial_genre_id
        assert genre.name == "Initial Rock"
