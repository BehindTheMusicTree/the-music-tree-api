from typing import cast
from rest_framework import status

from bodzify_api.model.criteria.children.genre.Genre import Genre
from bodzify_api.serializer.model.criteria.input.tree_import.Fields import Fields
from bodzify_api.test.utils.field.body_data.type.NotNullableListBodyDataTestCase import NotNullableListBodyDataTestCase
from bodzify_api.test.view.criteria.GenreTestCase import GenreTestCase


class TestOverwrite(GenreTestCase, NotNullableListBodyDataTestCase):
    def test_import_new_tree_then_overwrites_existing(self):
        self.model_fixture_factory.create_genre(name="Old Rock")

        tree_data = [{Fields.NAME_PUBLIC: "New Rock", Fields.CHILDREN: []}]
        response = self._post_genres_tree_import(data={Fields.TREE_PUBLIC: tree_data})

        assert response.status_code == status.HTTP_201_CREATED

        genres = Genre.objects.filter(user=self.test_user1)
        assert genres.count() == 1
        assert cast(Genre, genres.first()).name == "New Rock"
