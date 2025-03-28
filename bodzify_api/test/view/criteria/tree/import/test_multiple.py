from rest_framework import status

from bodzify_api.model.criteria.children.genre.Genre import Genre
from bodzify_api.serializer.model.criteria.output.Fields import Fields as GenreFields
from bodzify_api.test.view.criteria.GenreTestCase import GenreTestCase


class TestMultiple(GenreTestCase):
    def test_multiple_roots_then_multiple_trees(self):
        tree_data = [
            {
                "name": "Rock",
                "children": [
                    {"name": "Punk", "children": []}
                ]
            },
            {
                "name": "Jazz",
                "children": [
                    {"name": "Blues", "children": []}
                ]
            }
        ]
        response = self._post_genres_tree_import(tree_data)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.results_overall_total == 4  # 2 roots + 2 children
        assert len(self.results) == 4

        # Verify all genres are returned
        result_names = [result[GenreFields.NAME] for result in self.results]
        assert "Rock" in result_names
        assert "Punk" in result_names
        assert "Jazz" in result_names
        assert "Blues" in result_names

        # Verify parent relationships
        rock = next(result for result in self.results if result[GenreFields.NAME] == "Rock")
        punk = next(result for result in self.results if result[GenreFields.NAME] == "Punk")
        jazz = next(result for result in self.results if result[GenreFields.NAME] == "Jazz")
        blues = next(result for result in self.results if result[GenreFields.NAME] == "Blues")

        assert rock[GenreFields.PARENT] is None
        assert punk[GenreFields.PARENT] == rock[GenreFields.UUID]
        assert jazz[GenreFields.PARENT] is None
        assert blues[GenreFields.PARENT] == jazz[GenreFields.UUID]

        # Verify database state
        genres = Genre.objects.filter(user=self.test_user1)
        assert genres.count() == 4

        # Check Rock tree
        rock = genres.get(name="Rock")
        assert rock.parent is None
        punk = genres.get(name="Punk")
        assert punk.parent == rock

        # Check Jazz tree
        jazz = genres.get(name="Jazz")
        assert jazz.parent is None
        blues = genres.get(name="Blues")
        assert blues.parent == jazz

    def test_pagination(self):
        # Create a tree with 15 nodes (5 roots with 2 children each)
        tree_data = []
        for i in range(5):
            tree_data.append({
                "name": f"Root {i}",
                "children": [
                    {"name": f"Child {i}-1", "children": []},
                    {"name": f"Child {i}-2", "children": []}
                ]
            })

        response = self._post_genres_tree_import(tree_data)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.results_overall_total == 15  # 5 roots + 10 children

        # Test first page (default page size)
        assert len(self.results) == 10  # Default page size

        # Test second page
        response = self._post_genres_tree_import(tree_data, page=2)
        assert len(self.results) == 5  # Remaining items

        # Test custom page size
        response = self._post_genres_tree_import(tree_data, page_size=5)
        assert len(self.results) == 5
        assert self.results_overall_total == 15
