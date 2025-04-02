from typing import cast
from rest_framework import status

from bodzify_api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.model.criteria.children.genre.Genre import Genre
from bodzify_api.serializer.model.criteria.input.tree_import.Fields import Fields
from bodzify_api.test.view.criteria.GenreTestCase import GenreTestCase


class TestRollback(GenreTestCase):
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
        response = self._post_genres_tree_import(data={Fields.TREE: tree_data})

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
