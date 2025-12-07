from rest_framework import status

from api.test.integration.view.criteria.GenreTestCase import GenreTestCase
from api.serializer.model.criteria.input.tree_import.Fields import Fields


class TestCase(GenreTestCase):

    def test_duplicates_not_in_same_object_then_ok(self):
        tree_data = [
            {
                Fields.NAME_PUBLIC: "Test Criteria 1",
                Fields.CHILDREN: [
                    {
                        Fields.NAME_PUBLIC: "Test Criteria 2",
                        Fields.CHILDREN: []
                    }
                ]
            },
            {
                Fields.NAME_PUBLIC: "Test Criteria 3",
                Fields.CHILDREN: []
            }
        ]

        response = self._post_genres_tree_import(data={Fields.TREE: tree_data})

        assert response.status_code == status.HTTP_201_CREATED
