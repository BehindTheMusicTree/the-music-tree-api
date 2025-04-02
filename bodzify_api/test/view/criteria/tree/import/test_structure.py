from rest_framework import status

from bodzify_api.model.criteria.children.genre.Genre import Genre
from bodzify_api.serializer.model.criteria.input.tree_import.Fields import Fields
from bodzify_api.test.view.criteria.GenreTestCase import GenreTestCase


class TestStructure(GenreTestCase):
    def test_single_root_then_ok(self):
        data = [{Fields.NAME_PUBLIC: "Rock", Fields.CHILDREN: []}]
        response = self._post_genres_tree_import(data={Fields.TREE: data})
        assert response.status_code == status.HTTP_201_CREATED

        genres = Genre.objects.filter(user=self.test_user1)
        assert genres.count() == 1
        rock = genres.first()
        assert rock is not None
        assert rock.name == "Rock"
        assert rock.parent is None

    def test_multiple_roots_then_ok(self):
        data = [
            {Fields.NAME_PUBLIC: "Rock", Fields.CHILDREN: []},
            {Fields.NAME_PUBLIC: "Jazz", Fields.CHILDREN: []}
        ]
        response = self._post_genres_tree_import(data={Fields.TREE: data})
        assert response.status_code == status.HTTP_201_CREATED

        genres = Genre.objects.filter(user=self.test_user1)
        assert genres.count() == 2
        rock = genres.get(name="Rock")
        jazz = genres.get(name="Jazz")
        assert rock is not None
        assert jazz is not None
        assert rock.parent is None
        assert jazz.parent is None

    def test_nested_structure_then_ok(self):
        data = [{
            Fields.NAME_PUBLIC: "Rock",
            Fields.CHILDREN: [
                {
                    Fields.NAME_PUBLIC: "Metal",
                    Fields.CHILDREN: [
                        {Fields.NAME_PUBLIC: "Heavy Metal", Fields.CHILDREN: []}
                    ]
                }
            ]
        }]
        response = self._post_genres_tree_import(data={Fields.TREE: data})
        assert response.status_code == status.HTTP_201_CREATED

        genres = Genre.objects.filter(user=self.test_user1)
        assert genres.count() == 3
        rock = genres.get(name="Rock")
        metal = genres.get(name="Metal")
        heavy_metal = genres.get(name="Heavy Metal")
        assert rock is not None
        assert metal is not None
        assert heavy_metal is not None
        assert rock.parent is None
        assert metal.parent == rock
        assert heavy_metal.parent == metal

    def test_deep_nesting_then_ok(self):
        data = [{
            Fields.NAME_PUBLIC: "Rock",
            Fields.CHILDREN: [
                {
                    Fields.NAME_PUBLIC: "Metal",
                    Fields.CHILDREN: [
                        {
                            Fields.NAME_PUBLIC: "Heavy Metal",
                            Fields.CHILDREN: [
                                {
                                    Fields.NAME_PUBLIC: "Classic Metal",
                                    Fields.CHILDREN: [
                                        {Fields.NAME_PUBLIC: "Power Metal", Fields.CHILDREN: []}
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }]
        response = self._post_genres_tree_import(data={Fields.TREE: data})
        assert response.status_code == status.HTTP_201_CREATED

        genres = Genre.objects.filter(user=self.test_user1)
        assert genres.count() == 5
        rock = genres.get(name="Rock")
        metal = genres.get(name="Metal")
        heavy_metal = genres.get(name="Heavy Metal")
        classic_metal = genres.get(name="Classic Metal")
        power_metal = genres.get(name="Power Metal")
        assert rock is not None
        assert metal is not None
        assert heavy_metal is not None
        assert classic_metal is not None
        assert power_metal is not None
        assert rock.parent is None
        assert metal.parent == rock
        assert heavy_metal.parent == metal
        assert classic_metal.parent == heavy_metal
        assert power_metal.parent == classic_metal

    def test_multiple_children_then_ok(self):
        data = [{
            Fields.NAME_PUBLIC: "Rock",
            Fields.CHILDREN: [
                {Fields.NAME_PUBLIC: "Metal", Fields.CHILDREN: []},
                {Fields.NAME_PUBLIC: "Punk", Fields.CHILDREN: []},
                {Fields.NAME_PUBLIC: "Blues", Fields.CHILDREN: []}
            ]
        }]
        response = self._post_genres_tree_import(data={Fields.TREE: data})
        assert response.status_code == status.HTTP_201_CREATED

        genres = Genre.objects.filter(user=self.test_user1)
        assert genres.count() == 4
        rock = genres.get(name="Rock")
        metal = genres.get(name="Metal")
        punk = genres.get(name="Punk")
        blues = genres.get(name="Blues")
        assert rock is not None
        assert metal is not None
        assert punk is not None
        assert blues is not None
        assert rock.parent is None
        assert metal.parent == rock
        assert punk.parent == rock
        assert blues.parent == rock

    def test_complex_structure_then_ok(self):
        data = [
            {
                Fields.NAME_PUBLIC: "Rock",
                Fields.CHILDREN: [
                    {
                        Fields.NAME_PUBLIC: "Metal",
                        Fields.CHILDREN: [
                            {Fields.NAME_PUBLIC: "Heavy Metal", Fields.CHILDREN: []},
                            {Fields.NAME_PUBLIC: "Death Metal", Fields.CHILDREN: []}
                        ]
                    },
                    {
                        Fields.NAME_PUBLIC: "Punk",
                        Fields.CHILDREN: [
                            {Fields.NAME_PUBLIC: "Hardcore", Fields.CHILDREN: []},
                            {Fields.NAME_PUBLIC: "Pop Punk", Fields.CHILDREN: []}
                        ]
                    }
                ]
            },
            {
                Fields.NAME_PUBLIC: "Jazz",
                Fields.CHILDREN: [
                    {Fields.NAME_PUBLIC: "Bebop", Fields.CHILDREN: []},
                    {Fields.NAME_PUBLIC: "Fusion", Fields.CHILDREN: []}
                ]
            }
        ]
        response = self._post_genres_tree_import(data={Fields.TREE: data})
        assert response.status_code == status.HTTP_201_CREATED

        genres = Genre.objects.filter(user=self.test_user1)
        assert genres.count() == 10
        rock = genres.get(name="Rock")
        metal = genres.get(name="Metal")
        heavy_metal = genres.get(name="Heavy Metal")
        death_metal = genres.get(name="Death Metal")
        punk = genres.get(name="Punk")
        hardcore = genres.get(name="Hardcore")
        pop_punk = genres.get(name="Pop Punk")
        jazz = genres.get(name="Jazz")
        bebop = genres.get(name="Bebop")
        fusion = genres.get(name="Fusion")
        assert rock is not None
        assert metal is not None
        assert heavy_metal is not None
        assert death_metal is not None
        assert punk is not None
        assert hardcore is not None
        assert pop_punk is not None
        assert jazz is not None
        assert bebop is not None
        assert fusion is not None
        assert rock.parent is None
        assert metal.parent == rock
        assert heavy_metal.parent == metal
        assert death_metal.parent == metal
        assert punk.parent == rock
        assert hardcore.parent == punk
        assert pop_punk.parent == punk
        assert jazz.parent is None
        assert bebop.parent == jazz
        assert fusion.parent == jazz
