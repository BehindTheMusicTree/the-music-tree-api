from rest_framework import status

from bodzify_api.serializer.model.criteria.input.tree_import.Fields import Fields
from bodzify_api.test.utils.field.body_data.type.NotNullableListBodyDataTestCase import NotNullableListBodyDataTestCase
from bodzify_api.test.view.criteria.GenreTestCase import GenreTestCase


class TestStructure(GenreTestCase, NotNullableListBodyDataTestCase):
    def test_single_root_then_ok(self):
        data = [{Fields.NAME_PUBLIC: "Rock", Fields.CHILDREN: []}]
        response = self._post_genres_tree_import(data)
        assert response.status_code == status.HTTP_201_CREATED
        assert len(response.data) == 1
        assert response.data[0][Fields.NAME_PUBLIC] == "Rock"
        assert len(response.data[0][Fields.CHILDREN]) == 0

    def test_multiple_roots_then_ok(self):
        data = [
            {Fields.NAME_PUBLIC: "Rock", Fields.CHILDREN: []},
            {Fields.NAME_PUBLIC: "Jazz", Fields.CHILDREN: []}
        ]
        response = self._post_genres_tree_import(data)
        assert response.status_code == status.HTTP_201_CREATED
        assert len(response.data) == 2
        assert response.data[0][Fields.NAME_PUBLIC] == "Rock"
        assert response.data[1][Fields.NAME_PUBLIC] == "Jazz"

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
        response = self._post_genres_tree_import(data)
        assert response.status_code == status.HTTP_201_CREATED
        assert len(response.data) == 1
        assert response.data[0][Fields.NAME_PUBLIC] == "Rock"
        assert len(response.data[0][Fields.CHILDREN]) == 1
        assert response.data[0][Fields.CHILDREN][0][Fields.NAME_PUBLIC] == "Metal"
        assert len(response.data[0][Fields.CHILDREN][0][Fields.CHILDREN]) == 1
        assert response.data[0][Fields.CHILDREN][0][Fields.CHILDREN][0][Fields.NAME_PUBLIC] == "Heavy Metal"

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
        response = self._post_genres_tree_import(data)
        assert response.status_code == status.HTTP_201_CREATED
        assert len(response.data) == 1
        assert response.data[0][Fields.NAME_PUBLIC] == "Rock"
        assert len(response.data[0][Fields.CHILDREN]) == 1
        assert response.data[0][Fields.CHILDREN][0][Fields.NAME_PUBLIC] == "Metal"
        assert len(response.data[0][Fields.CHILDREN][0][Fields.CHILDREN]) == 1
        assert response.data[0][Fields.CHILDREN][0][Fields.CHILDREN][0][Fields.NAME_PUBLIC] == "Heavy Metal"
        assert len(response.data[0][Fields.CHILDREN][0][Fields.CHILDREN][0][Fields.CHILDREN]) == 1
        assert response.data[0][
            Fields.CHILDREN][0][
            Fields.CHILDREN][0][
            Fields.CHILDREN][0][
            Fields.NAME_PUBLIC] == "Classic Metal"
        assert len(response.data[0][Fields.CHILDREN][0][Fields.CHILDREN][0][Fields.CHILDREN][0][Fields.CHILDREN]) == 1
        assert response.data[0][
            Fields.CHILDREN][0][
            Fields.CHILDREN][0][
            Fields.CHILDREN][0][
            Fields.CHILDREN][0][
            Fields.NAME_PUBLIC] == "Power Metal"

    def test_multiple_children_then_ok(self):
        data = [{
            Fields.NAME_PUBLIC: "Rock",
            Fields.CHILDREN: [
                {Fields.NAME_PUBLIC: "Metal", Fields.CHILDREN: []},
                {Fields.NAME_PUBLIC: "Punk", Fields.CHILDREN: []},
                {Fields.NAME_PUBLIC: "Blues", Fields.CHILDREN: []}
            ]
        }]
        response = self._post_genres_tree_import(data)
        assert response.status_code == status.HTTP_201_CREATED
        assert len(response.data) == 1
        assert response.data[0][Fields.NAME_PUBLIC] == "Rock"
        assert len(response.data[0][Fields.CHILDREN]) == 3
        assert response.data[0][Fields.CHILDREN][0][Fields.NAME_PUBLIC] == "Metal"
        assert response.data[0][Fields.CHILDREN][1][Fields.NAME_PUBLIC] == "Punk"
        assert response.data[0][Fields.CHILDREN][2][Fields.NAME_PUBLIC] == "Blues"

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
        response = self._post_genres_tree_import(data)
        assert response.status_code == status.HTTP_201_CREATED
        assert len(response.data) == 2
        assert response.data[0][Fields.NAME_PUBLIC] == "Rock"
        assert len(response.data[0][Fields.CHILDREN]) == 2
        assert response.data[0][Fields.CHILDREN][0][Fields.NAME_PUBLIC] == "Metal"
        assert len(response.data[0][Fields.CHILDREN][0][Fields.CHILDREN]) == 2
        assert response.data[0][Fields.CHILDREN][1][Fields.NAME_PUBLIC] == "Punk"
        assert len(response.data[0][Fields.CHILDREN][1][Fields.CHILDREN]) == 2
        assert response.data[1][Fields.NAME_PUBLIC] == "Jazz"
        assert len(response.data[1][Fields.CHILDREN]) == 2
