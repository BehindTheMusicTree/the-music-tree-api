from rest_framework import status

from bodzify_api.test.view.criteria.GenreTestCase import GenreTestCase


class TestCase(GenreTestCase):

    def test_duplicates_not_in_same_object_then_ok(self):
        json_data = [
            {
                "name": "Test Criteria 1",
                "children": [
                    {
                        "name": "Test Criteria 2",
                        "children": []
                    }
                ]
            },
            {
                "name": "Test Criteria 3",
                "children": []
            }
        ]

        response = self._post_genres_tree_import(json_data)

        assert response.status_code == status.HTTP_201_CREATED
