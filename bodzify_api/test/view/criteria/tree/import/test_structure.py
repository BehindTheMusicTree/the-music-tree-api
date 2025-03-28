from rest_framework import status

from bodzify_api.model.criteria.children.genre.Genre import Genre
from bodzify_api.serializer.model.criteria.output.Fields import Fields as GenreFields
from bodzify_api.test.view.criteria.GenreTestCase import GenreTestCase


class TestStructure(GenreTestCase):
    def test_single_root_then_single_node(self):
        tree_data = [{"name": "Rock", "children": []}]
        response = self._post_genres_tree_import(tree_data)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.results_overall_total == 1
        assert len(self.results) == 1
        assert self.results[0][GenreFields.NAME] == "Rock"
        assert GenreFields.UUID in self.results[0]
        assert GenreFields.PARENT in self.results[0]
        assert self.results[0][GenreFields.PARENT] is None

        # Verify database state
        genres = Genre.objects.filter(user=self.test_user1)
        assert genres.count() == 1
        assert genres.first().name == "Rock"

    def test_root_with_children_then_tree_with_children(self):
        tree_data = [
            {
                "name": "Rock",
                "children": [
                    {"name": "Punk", "children": []},
                    {"name": "Metal", "children": []}
                ]
            }
        ]
        response = self._post_genres_tree_import(tree_data)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.results_overall_total == 3  # Root + 2 children
        assert len(self.results) == 3

        genres = Genre.objects.filter(user=self.test_user1)
        genre_names = [genre.name for genre in genres]
        assert "Rock" in genre_names
        assert "Punk" in genre_names
        assert "Metal" in genre_names

        # Verify parent relationships in DB
        rock = genres.get(name="Rock")
        assert rock.parent is None

        punk = genres.get(name="Punk")
        metal = genres.get(name="Metal")
        assert punk.parent == rock
        assert metal.parent == rock

    def test_deep_tree_then_full_hierarchy(self):
        tree_data = [
            {
                "name": "Rock",
                "children": [
                    {
                        "name": "Punk",
                        "children": [
                            {"name": "Hardcore", "children": []}
                        ]
                    },
                    {"name": "Metal", "children": []}
                ]
            }
        ]
        response = self._post_genres_tree_import(tree_data)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.results_overall_total == 4  # Root + 2 children + 1 grandchild
        assert len(self.results) == 4

        # Verify all genres are returned
        result_names = [result[GenreFields.NAME] for result in self.results]
        assert "Rock" in result_names
        assert "Punk" in result_names
        assert "Hardcore" in result_names
        assert "Metal" in result_names

        # Verify parent relationships
        rock = next(result for result in self.results if result[GenreFields.NAME] == "Rock")
        punk = next(result for result in self.results if result[GenreFields.NAME] == "Punk")
        hardcore = next(result for result in self.results if result[GenreFields.NAME] == "Hardcore")
        metal = next(result for result in self.results if result[GenreFields.NAME] == "Metal")

        assert rock[GenreFields.PARENT] is None
        assert punk[GenreFields.PARENT] == rock[GenreFields.UUID]
        assert hardcore[GenreFields.PARENT] == punk[GenreFields.UUID]
        assert metal[GenreFields.PARENT] == rock[GenreFields.UUID]

        # Verify database state
        genres = Genre.objects.filter(user=self.test_user1)
        assert genres.count() == 4

        # Check root
        root = genres.get(name="Rock")
        assert root.parent is None

        # Check Punk branch
        punk = genres.get(name="Punk")
        assert punk.parent == root
        hardcore = genres.get(name="Hardcore")
        assert hardcore.parent == punk

        # Check Metal branch
        metal = genres.get(name="Metal")
        assert metal.parent == root
