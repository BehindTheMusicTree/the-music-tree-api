from rest_framework import status

from bodzify_api.test.view.criteria.GenreTestCase import GenreTestCase


class TestCase(GenreTestCase):

    def test_empty_then_empty_tree(self):
        response = self._list_genres(tree=True)

        assert response.status_code == status.HTTP_200_OK
        assert self.results == []

    def test_single_root_then_single_node(self):
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")

        response = self._list_genres(tree=True)

        assert response.status_code == status.HTTP_200_OK
        assert len(self.results) == 1
        assert self.results[0]["name"] == genre_rock.name
        assert self.results[0]["children"] == []

    def test_root_with_children_then_tree_with_children(self):
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")
        genre_punk = self.model_fixture_factory.create_genre(name="Punk", parent=genre_rock)
        genre_metal = self.model_fixture_factory.create_genre(name="Metal", parent=genre_rock)

        response = self._list_genres(tree=True)

        assert response.status_code == status.HTTP_200_OK
        assert len(self.results) == 1
        assert self.results[0]["name"] == genre_rock.name
        assert len(self.results[0]["children"]) == 2
        child_names = [child["name"] for child in self.results[0]["children"]]
        assert genre_punk.name in child_names
        assert genre_metal.name in child_names
        assert all(child["children"] == [] for child in self.results[0]["children"])

    def test_deep_tree_then_full_hierarchy(self):
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")
        genre_punk = self.model_fixture_factory.create_genre(name="Punk", parent=genre_rock)
        genre_hardcore = self.model_fixture_factory.create_genre(name="Hardcore", parent=genre_punk)
        genre_metal = self.model_fixture_factory.create_genre(name="Metal", parent=genre_rock)

        response = self._list_genres(tree=True)

        assert response.status_code == status.HTTP_200_OK
        assert len(self.results) == 1
        assert self.results[0]["name"] == genre_rock.name
        assert len(self.results[0]["children"]) == 2

        # Check Punk branch
        punk_node = next(child for child in self.results[0]["children"] if child["name"] == genre_punk.name)
        assert len(punk_node["children"]) == 1
        assert punk_node["children"][0]["name"] == genre_hardcore.name
        assert punk_node["children"][0]["children"] == []

        # Check Metal branch
        metal_node = next(child for child in self.results[0]["children"] if child["name"] == genre_metal.name)
        assert metal_node["children"] == []

    def test_multiple_roots_then_multiple_trees(self):
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")
        genre_punk = self.model_fixture_factory.create_genre(name="Punk", parent=genre_rock)
        genre_jazz = self.model_fixture_factory.create_genre(name="Jazz")
        genre_blues = self.model_fixture_factory.create_genre(name="Blues", parent=genre_jazz)

        response = self._list_genres(tree=True)

        assert response.status_code == status.HTTP_200_OK
        assert len(self.results) == 2

        # Check Rock tree
        rock_tree = next(tree for tree in self.results if tree["name"] == genre_rock.name)
        assert len(rock_tree["children"]) == 1
        assert rock_tree["children"][0]["name"] == genre_punk.name
        assert rock_tree["children"][0]["children"] == []

        # Check Jazz tree
        jazz_tree = next(tree for tree in self.results if tree["name"] == genre_jazz.name)
        assert len(jazz_tree["children"]) == 1
        assert jazz_tree["children"][0]["name"] == genre_blues.name
        assert jazz_tree["children"][0]["children"] == []

    def test_with_query_param_not_related_to_pagination_then_400(self):
        response = self._list_genres(tree=True, limit=100)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_with_query_param_related_to_pagination_then_results_are_paginated_by_roots(self):
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")
        genre_punk = self.model_fixture_factory.create_genre(name="Punk", parent=genre_rock)
        genre_metal = self.model_fixture_factory.create_genre(name="Metal", parent=genre_rock)
        genre_jazz = self.model_fixture_factory.create_genre(name="Jazz")
        genre_blues = self.model_fixture_factory.create_genre(name="Blues", parent=genre_jazz)
        genre_pop = self.model_fixture_factory.create_genre(name="Pop")

        response = self._list_genres(page=2, page_size=1)
        assert response.status_code == status.HTTP_200_OK
        assert len(self.results) == 1
        assert self.results[0]["name"] == genre_metal.name
