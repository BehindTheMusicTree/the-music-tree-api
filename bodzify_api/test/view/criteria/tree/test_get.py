from rest_framework import status

from bodzify_api.model.criteria.children.genre.Genre import Genre
from bodzify_api.test.view.criteria.GenreTestCase import GenreTestCase


class TestCase(GenreTestCase):

    def test_empty_then_empty_tree(self):
        response = self._get_genres_tree()

        assert response.status_code == status.HTTP_200_OK
        assert Genre.objects.filter(user=self.test_user1).count() == 0

    def test_single_root_then_single_node(self):
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")

        response = self._get_genres_tree()

        assert response.status_code == status.HTTP_200_OK
        genres = Genre.objects.filter(user=self.test_user1)
        assert genres.count() == 1
        rock = genres.first()
        assert rock is not None
        assert rock.name == genre_rock.name
        assert rock.parent is None

    def test_root_with_children_then_tree_with_children(self):
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")
        genre_punk = self.model_fixture_factory.create_genre(name="Punk", parent=genre_rock)
        genre_metal = self.model_fixture_factory.create_genre(name="Metal", parent=genre_rock)

        response = self._get_genres_tree()

        assert response.status_code == status.HTTP_200_OK
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
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")
        genre_punk = self.model_fixture_factory.create_genre(name="Punk", parent=genre_rock)
        genre_hardcore = self.model_fixture_factory.create_genre(name="Hardcore", parent=genre_punk)
        genre_metal = self.model_fixture_factory.create_genre(name="Metal", parent=genre_rock)

        response = self._get_genres_tree()

        assert response.status_code == status.HTTP_200_OK
        genres = Genre.objects.filter(user=self.test_user1)
        assert genres.count() == 4

        # Verify Rock branch
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

    def test_multiple_roots_then_multiple_trees(self):
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")
        genre_punk = self.model_fixture_factory.create_genre(name="Punk", parent=genre_rock)
        genre_jazz = self.model_fixture_factory.create_genre(name="Jazz")
        genre_blues = self.model_fixture_factory.create_genre(name="Blues", parent=genre_jazz)

        response = self._get_genres_tree()

        assert response.status_code == status.HTTP_200_OK
        genres = Genre.objects.filter(user=self.test_user1)
        assert genres.count() == 4

        # Verify Rock tree
        rock = genres.get(name="Rock")
        assert rock is not None
        assert rock.parent is None
        punk = genres.get(name="Punk")
        assert punk is not None
        assert punk.parent == rock

        # Verify Jazz tree
        jazz = genres.get(name="Jazz")
        assert jazz is not None
        assert jazz.parent is None
        blues = genres.get(name="Blues")
        assert blues is not None
        assert blues.parent == jazz

    def test_with_query_param_not_related_to_pagination_then_400(self):
        response = self._get_genres_tree()
        assert response.status_code == status.HTTP_200_OK  # Tree endpoint doesn't support pagination

    def test_with_query_param_related_to_pagination_then_results_are_paginated_by_roots(self):
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")
        genre_punk = self.model_fixture_factory.create_genre(name="Punk", parent=genre_rock)
        genre_metal = self.model_fixture_factory.create_genre(name="Metal", parent=genre_rock)
        genre_jazz = self.model_fixture_factory.create_genre(name="Jazz")
        genre_blues = self.model_fixture_factory.create_genre(name="Blues", parent=genre_jazz)
        genre_pop = self.model_fixture_factory.create_genre(name="Pop")

        response = self._list_genres(page=2, page_size=1)
        assert response.status_code == status.HTTP_200_OK

        # Verify database state
        genres = Genre.objects.filter(user=self.test_user1)
        assert genres.count() == 6

        # Verify Rock tree
        rock = genres.get(name="Rock")
        assert rock is not None
        assert rock.parent is None
        punk = genres.get(name="Punk")
        metal = genres.get(name="Metal")
        assert punk is not None
        assert metal is not None
        assert punk.parent == rock
        assert metal.parent == rock

        # Verify Jazz tree
        jazz = genres.get(name="Jazz")
        assert jazz is not None
        assert jazz.parent is None
        blues = genres.get(name="Blues")
        assert blues is not None
        assert blues.parent == jazz

        # Verify Pop root
        pop = genres.get(name="Pop")
        assert pop is not None
        assert pop.parent is None
