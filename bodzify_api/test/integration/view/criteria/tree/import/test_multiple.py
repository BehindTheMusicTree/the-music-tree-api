from rest_framework import status

from bodzify_api.serializer.model.criteria.input.tree_import.Fields import Fields
from bodzify_api.model.criteria.children.genre.Genre import Genre
from bodzify_api.test.integration.view.criteria.GenreTestCase import GenreTestCase


class TestMultiple(GenreTestCase):
    def test_multiple_roots_then_multiple_trees(self):
        tree_data = [
            {
                Fields.NAME_PUBLIC: "Rock",
                Fields.CHILDREN: [
                    {Fields.NAME_PUBLIC: "Punk", Fields.CHILDREN: []}
                ]
            },
            {
                Fields.NAME_PUBLIC: "Jazz",
                Fields.CHILDREN: [
                    {Fields.NAME_PUBLIC: "Blues", Fields.CHILDREN: []}
                ]
            }
        ]
        response = self._post_genres_tree_import(data={Fields.TREE: tree_data})

        assert response.status_code == status.HTTP_201_CREATED

        # Verify all genres exist in DB
        genres = Genre.objects.filter(user=self.test_user1)
        assert genres.count() == 4  # 2 roots + 2 children

        # Verify Rock tree
        rock = genres.get(name="Rock")
        assert rock.parent is None
        punk = genres.get(name="Punk")
        assert punk.parent == rock
        assert punk.user == self.test_user1

        # Verify Jazz tree
        jazz = genres.get(name="Jazz")
        assert jazz.parent is None
        blues = genres.get(name="Blues")
        assert blues.parent == jazz
        assert blues.user == self.test_user1

    def test_import_tree_then_pagination_works(self):
        # Create a tree with 15 nodes (5 roots with 2 children each)
        tree_data = []
        for i in range(5):
            tree_data.append({
                Fields.NAME_PUBLIC: f"Root {i}",
                Fields.CHILDREN: [
                    {Fields.NAME_PUBLIC: f"Child {i}-1", Fields.CHILDREN: []},
                    {Fields.NAME_PUBLIC: f"Child {i}-2", Fields.CHILDREN: []}
                ]
            })

        response = self._post_genres_tree_import(data={Fields.TREE: tree_data})

        assert response.status_code == status.HTTP_201_CREATED

        # Verify all genres exist in DB
        genres = Genre.objects.filter(user=self.test_user1)
        assert genres.count() == 15  # 5 roots + 10 children

        # Verify all roots have no parent
        for i in range(5):
            root = genres.get(name=f"Root {i}")
            assert root.parent is None
            assert root.user == self.test_user1

            # Verify children
            child1 = genres.get(name=f"Child {i}-1")
            child2 = genres.get(name=f"Child {i}-2")
            assert child1.parent == root
            assert child2.parent == root
            assert child1.user == self.test_user1
            assert child2.user == self.test_user1
