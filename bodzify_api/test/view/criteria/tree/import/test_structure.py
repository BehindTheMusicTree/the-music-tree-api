from rest_framework import status

from bodzify_api.model.criteria.children.genre.Genre import Genre
from bodzify_api.test.view.criteria.GenreTestCase import GenreTestCase


class TestStructure(GenreTestCase):
    def test_single_root_then_single_node(self):
        tree_data = [{"name": "Rock", "children": []}]
        response = self._post_genres_tree_import(tree_data)

        assert response.status_code == status.HTTP_201_CREATED

        # Verify database state
        genres = Genre.objects.filter(user=self.test_user1)
        assert genres.count() == 1
        rock = genres.first()
        assert rock is not None
        assert rock.name == "Rock"
        assert rock.parent is None

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

        # Verify database state
        genres = Genre.objects.filter(user=self.test_user1)
        assert genres.count() == 3

        # Verify root
        rock = genres.get(name="Rock")
        assert rock is not None
        assert rock.parent is None

        # Verify children
        punk = genres.get(name="Punk")
        metal = genres.get(name="Metal")
        assert punk is not None
        assert metal is not None
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

        # Verify database state
        genres = Genre.objects.filter(user=self.test_user1)
        assert genres.count() == 4

        # Verify root
        rock = genres.get(name="Rock")
        assert rock is not None
        assert rock.parent is None

        # Verify Punk branch
        punk = genres.get(name="Punk")
        assert punk is not None
        assert punk.parent == rock
        hardcore = genres.get(name="Hardcore")
        assert hardcore is not None
        assert hardcore.parent == punk

        # Verify Metal branch
        metal = genres.get(name="Metal")
        assert metal is not None
        assert metal.parent == rock
