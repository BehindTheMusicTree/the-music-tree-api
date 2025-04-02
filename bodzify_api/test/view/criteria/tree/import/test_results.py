from rest_framework import status

from bodzify_api.serializer.model.criteria.input.Fields import Fields as InputFields
from bodzify_api.serializer.model.criteria.input.tree_import.Fields import Fields as TreeImportFields
from bodzify_api.test.view.criteria.GenreTestCase import GenreTestCase


class TestResults(GenreTestCase):
    def test_single_root_then_returns_correct_structure(self):
        data = [{TreeImportFields.NAME_PUBLIC: "Rock", TreeImportFields.CHILDREN: []}]
        response = self._post_genres_tree_import(data={TreeImportFields.TREE: data})
        assert response.status_code == status.HTTP_201_CREATED

        assert len(self.results) == 1
        assert self.results[0][InputFields.NAME_PUBLIC] == "Rock"
        assert self.results[0][InputFields.PARENT] is None

    def test_multiple_roots_then_returns_correct_structure(self):
        data = [
            {TreeImportFields.NAME_PUBLIC: "Rock", TreeImportFields.CHILDREN: []},
            {TreeImportFields.NAME_PUBLIC: "Jazz", TreeImportFields.CHILDREN: []}
        ]
        response = self._post_genres_tree_import(data={TreeImportFields.TREE: data})
        assert response.status_code == status.HTTP_201_CREATED

        assert len(self.results) == 2
        rock = next(g for g in self.results if g[InputFields.NAME_PUBLIC] == "Rock")
        jazz = next(g for g in self.results if g[InputFields.NAME_PUBLIC] == "Jazz")

        assert rock[InputFields.PARENT] is None
        assert jazz[InputFields.PARENT] is None

    def test_nested_structure_then_returns_correct_structure(self):
        data = [{
            TreeImportFields.NAME_PUBLIC: "Rock",
            TreeImportFields.CHILDREN: [
                {
                    TreeImportFields.NAME_PUBLIC: "Metal",
                    TreeImportFields.CHILDREN: [
                        {TreeImportFields.NAME_PUBLIC: "Heavy Metal", TreeImportFields.CHILDREN: []}
                    ]
                }
            ]
        }]
        response = self._post_genres_tree_import(data={TreeImportFields.TREE: data})
        assert response.status_code == status.HTTP_201_CREATED

        assert len(self.results) == 3
        rock = next(g for g in self.results if g[InputFields.NAME_PUBLIC] == "Rock")
        metal = next(g for g in self.results if g[InputFields.NAME_PUBLIC] == "Metal")
        heavy_metal = next(g for g in self.results if g[InputFields.NAME_PUBLIC] == "Heavy Metal")

        assert rock[InputFields.PARENT] is None
        assert metal[InputFields.PARENT][InputFields.NAME_PUBLIC] == "Rock"
        assert heavy_metal[InputFields.PARENT][InputFields.NAME_PUBLIC] == "Metal"

    def test_deep_nesting_then_returns_correct_structure(self):
        data = [{
            TreeImportFields.NAME_PUBLIC: "Rock",
            TreeImportFields.CHILDREN: [
                {
                    TreeImportFields.NAME_PUBLIC: "Metal",
                    TreeImportFields.CHILDREN: [
                        {
                            TreeImportFields.NAME_PUBLIC: "Heavy Metal",
                            TreeImportFields.CHILDREN: [
                                {
                                    TreeImportFields.NAME_PUBLIC: "Classic Metal",
                                    TreeImportFields.CHILDREN: [
                                        {TreeImportFields.NAME_PUBLIC: "Power Metal", TreeImportFields.CHILDREN: []}
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }]
        response = self._post_genres_tree_import(data={TreeImportFields.TREE: data})
        assert response.status_code == status.HTTP_201_CREATED

        assert len(self.results) == 5
        rock = next(g for g in self.results if g[InputFields.NAME_PUBLIC] == "Rock")
        metal = next(g for g in self.results if g[InputFields.NAME_PUBLIC] == "Metal")
        heavy_metal = next(g for g in self.results if g[InputFields.NAME_PUBLIC] == "Heavy Metal")
        classic_metal = next(g for g in self.results if g[InputFields.NAME_PUBLIC] == "Classic Metal")
        power_metal = next(g for g in self.results if g[InputFields.NAME_PUBLIC] == "Power Metal")

        assert rock[InputFields.PARENT] is None
        assert metal[InputFields.PARENT][InputFields.NAME_PUBLIC] == "Rock"
        assert heavy_metal[InputFields.PARENT][InputFields.NAME_PUBLIC] == "Metal"
        assert classic_metal[InputFields.PARENT][InputFields.NAME_PUBLIC] == "Heavy Metal"
        assert power_metal[InputFields.PARENT][InputFields.NAME_PUBLIC] == "Classic Metal"

    def test_multiple_children_then_returns_correct_structure(self):
        data = [{
            TreeImportFields.NAME_PUBLIC: "Rock",
            TreeImportFields.CHILDREN: [
                {TreeImportFields.NAME_PUBLIC: "Metal", TreeImportFields.CHILDREN: []},
                {TreeImportFields.NAME_PUBLIC: "Punk", TreeImportFields.CHILDREN: []},
                {TreeImportFields.NAME_PUBLIC: "Blues", TreeImportFields.CHILDREN: []}
            ]
        }]
        response = self._post_genres_tree_import(data={TreeImportFields.TREE: data})
        assert response.status_code == status.HTTP_201_CREATED

        assert len(self.results) == 4
        rock = next(g for g in self.results if g[InputFields.NAME_PUBLIC] == "Rock")
        metal = next(g for g in self.results if g[InputFields.NAME_PUBLIC] == "Metal")
        punk = next(g for g in self.results if g[InputFields.NAME_PUBLIC] == "Punk")
        blues = next(g for g in self.results if g[InputFields.NAME_PUBLIC] == "Blues")

        assert rock[InputFields.PARENT] is None
        assert metal[InputFields.PARENT][InputFields.NAME_PUBLIC] == "Rock"
        assert punk[InputFields.PARENT][InputFields.NAME_PUBLIC] == "Rock"
        assert blues[InputFields.PARENT][InputFields.NAME_PUBLIC] == "Rock"

    def test_complex_structure_then_returns_correct_structure(self):
        data = [
            {
                TreeImportFields.NAME_PUBLIC: "Rock",
                TreeImportFields.CHILDREN: [
                    {
                        TreeImportFields.NAME_PUBLIC: "Metal",
                        TreeImportFields.CHILDREN: [
                            {TreeImportFields.NAME_PUBLIC: "Heavy Metal", TreeImportFields.CHILDREN: []},
                            {TreeImportFields.NAME_PUBLIC: "Death Metal", TreeImportFields.CHILDREN: []}
                        ]
                    },
                    {
                        TreeImportFields.NAME_PUBLIC: "Punk",
                        TreeImportFields.CHILDREN: [
                            {TreeImportFields.NAME_PUBLIC: "Hardcore", TreeImportFields.CHILDREN: []},
                            {TreeImportFields.NAME_PUBLIC: "Pop Punk", TreeImportFields.CHILDREN: []}
                        ]
                    }
                ]
            },
            {
                TreeImportFields.NAME_PUBLIC: "Jazz",
                TreeImportFields.CHILDREN: [
                    {TreeImportFields.NAME_PUBLIC: "Bebop", TreeImportFields.CHILDREN: []},
                    {TreeImportFields.NAME_PUBLIC: "Fusion", TreeImportFields.CHILDREN: []}
                ]
            }
        ]
        response = self._post_genres_tree_import(data={TreeImportFields.TREE: data})
        assert response.status_code == status.HTTP_201_CREATED

        assert len(self.results) == 10
        rock = next(g for g in self.results if g[InputFields.NAME_PUBLIC] == "Rock")
        metal = next(g for g in self.results if g[InputFields.NAME_PUBLIC] == "Metal")
        heavy_metal = next(g for g in self.results if g[InputFields.NAME_PUBLIC] == "Heavy Metal")
        death_metal = next(g for g in self.results if g[InputFields.NAME_PUBLIC] == "Death Metal")
        punk = next(g for g in self.results if g[InputFields.NAME_PUBLIC] == "Punk")
        hardcore = next(g for g in self.results if g[InputFields.NAME_PUBLIC] == "Hardcore")
        pop_punk = next(g for g in self.results if g[InputFields.NAME_PUBLIC] == "Pop Punk")
        jazz = next(g for g in self.results if g[InputFields.NAME_PUBLIC] == "Jazz")
        bebop = next(g for g in self.results if g[InputFields.NAME_PUBLIC] == "Bebop")
        fusion = next(g for g in self.results if g[InputFields.NAME_PUBLIC] == "Fusion")

        assert rock[InputFields.PARENT] is None
        assert metal[InputFields.PARENT][InputFields.NAME_PUBLIC] == "Rock"
        assert heavy_metal[InputFields.PARENT][InputFields.NAME_PUBLIC] == "Metal"
        assert death_metal[InputFields.PARENT][InputFields.NAME_PUBLIC] == "Metal"
        assert punk[InputFields.PARENT][InputFields.NAME_PUBLIC] == "Rock"
        assert hardcore[InputFields.PARENT][InputFields.NAME_PUBLIC] == "Punk"
        assert pop_punk[InputFields.PARENT][InputFields.NAME_PUBLIC] == "Punk"
        assert jazz[InputFields.PARENT] is None
        assert bebop[InputFields.PARENT][InputFields.NAME_PUBLIC] == "Jazz"
        assert fusion[InputFields.PARENT][InputFields.NAME_PUBLIC] == "Jazz"
