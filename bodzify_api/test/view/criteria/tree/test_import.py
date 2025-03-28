from typing import cast

from rest_framework import status

from bodzify_api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.model.criteria.children.genre.Genre import Genre
from bodzify_api.serializer.model.criteria.output.Fields import Fields as GenreFields
from bodzify_api.test.view.criteria.GenreTestCase import GenreTestCase


class TestCase(GenreTestCase):

    def test_empty_array_then_error(self):
        response = self._post_genres_tree_import([])

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert self.bad_request_result_field_errors[0]["field"] == "data"
        assert self.bad_request_result_field_errors[0]["code"] == FieldValidationErrorCode.REQUIRED

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
        assert cast(Genre, genres.first()).name == "Rock"

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

        # Verify all genres are returned
        result_names = [result[GenreFields.NAME] for result in self.results]
        assert "Rock" in result_names
        assert "Punk" in result_names
        assert "Metal" in result_names

        # Verify parent relationships
        rock = next(result for result in self.results if result[GenreFields.NAME] == "Rock")
        assert rock[GenreFields.PARENT] is None

        punk = next(result for result in self.results if result[GenreFields.NAME] == "Punk")
        metal = next(result for result in self.results if result[GenreFields.NAME] == "Metal")
        assert punk[GenreFields.PARENT] == rock[GenreFields.UUID]
        assert metal[GenreFields.PARENT] == rock[GenreFields.UUID]

        # Verify database state
        genres = Genre.objects.filter(user=self.test_user1)
        assert genres.count() == 3

        # Check root
        root = genres.get(name="Rock")
        assert root.parent is None

        # Check children
        children = genres.filter(parent=root)
        assert children.count() == 2
        child_names = [child.name for child in children]
        assert "Punk" in child_names
        assert "Metal" in child_names

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

    def test_invalid_input_then_error(self):
        # Test with non-array input
        response = self._post_genres_tree_import({"name": "Rock"})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert self.bad_request_result_field_errors[0]["field"] == "data"
        assert self.bad_request_result_field_errors[0]["code"] == FieldValidationErrorCode.FORMAT_INVALID
        assert "Input must be an array" in self.bad_request_result_field_errors[0]["message"]

        # Test with invalid node structure
        response = self._post_genres_tree_import([{"invalid": "Rock"}])
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert self.bad_request_result_field_errors[0]["field"] == "data"
        assert self.bad_request_result_field_errors[0]["code"] == FieldValidationErrorCode.FORMAT_INVALID
        assert "must have a 'name' field" in self.bad_request_result_field_errors[0]["message"]

        # Test with invalid children structure
        response = self._post_genres_tree_import([{"name": "Rock", "children": "invalid"}])
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert self.bad_request_result_field_errors[0]["field"] == "data"
        assert self.bad_request_result_field_errors[0]["code"] == FieldValidationErrorCode.FORMAT_INVALID
        assert "Children must be an array" in self.bad_request_result_field_errors[0]["message"]

    def test_import_overwrites_existing(self):
        # Create initial genre
        self.model_fixture_factory.create_genre(name="Old Rock")

        # Import new tree
        tree_data = [{"name": "New Rock", "children": []}]
        response = self._post_genres_tree_import(tree_data)

        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Verify old genre is gone and new one exists
        genres = Genre.objects.filter(user=self.test_user1)
        assert genres.count() == 1
        assert cast(Genre, genres.first()).name == "New Rock"

    def test_duplicate_names_then_error(self):
        duplicate_name = "Rock"
        tree_data = [
            {"name": duplicate_name, "children": []},
            {"name": duplicate_name, "children": []}  # Duplicate name
        ]
        response = self._post_genres_tree_import(tree_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert self.bad_request_result_field_errors[0]["field"] == "name"
        assert self.bad_request_result_field_errors[0]["code"] == FieldValidationErrorCode.NAME_DUPLICATE
        assert duplicate_name in self.bad_request_result_field_errors[0]["message"]

    def test_empty_name_then_error(self):
        tree_data = [{"name": "", "children": []}]
        response = self._post_genres_tree_import(tree_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert self.bad_request_result_field_errors[0]["field"] == "name"
        assert self.bad_request_result_field_errors[0]["code"] == FieldValidationErrorCode.NAME_EMPTY
        assert "Name cannot be empty" in self.bad_request_result_field_errors[0]["message"]

    def test_missing_name_then_error(self):
        tree_data = [{"children": []}]  # Missing name field
        response = self._post_genres_tree_import(tree_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert self.bad_request_result_field_errors[0]["field"] == "data"
        assert self.bad_request_result_field_errors[0]["code"] == FieldValidationErrorCode.FORMAT_INVALID
        assert "must have a 'name' field" in self.bad_request_result_field_errors[0]["message"]

    def test_error_during_import_then_rollback(self):
        # Create initial genre
        initial_genre = self.model_fixture_factory.create_genre(name="Initial Rock")
        initial_genre_id = initial_genre.uuid

        # Try to import a tree with a duplicate name that will cause an error
        tree_data = [
            {
                "name": "Rock",
                "children": [
                    {"name": "Punk", "children": []},
                    {"name": "Rock", "children": []}  # This will cause a duplicate name error
                ]
            }
        ]
        response = self._post_genres_tree_import(tree_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert self.bad_request_result_field_errors[0]["field"] == "name"
        assert self.bad_request_result_field_errors[0]["code"] == FieldValidationErrorCode.NAME_DUPLICATE
        assert "already exists for this user" in self.bad_request_result_field_errors[0]["message"]

        # Verify that the initial genre still exists and no new genres were created
        genres = Genre.objects.filter(user=self.test_user1)
        assert genres.count() == 1
        genre = cast(Genre, genres.first())
        assert genre.uuid == initial_genre_id
        assert genre.name == "Initial Rock"
