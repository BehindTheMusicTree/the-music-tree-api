from rest_framework import status

from bodzify_api.test.field.filter.foreign_key.PrivateForeignKeyFilterTestCase import PrivateForeignKeyFilterTestCase
from bodzify_api.test.view.criteria.GenreTestCase import GenreTestCase
from bodzify_api.filtering.set.criteria.Fields import Fields as FilterfFields
from bodzify_api.model.criteria.Fields import Fields as ModelFields
from bodzify_api.view.error.FieldValidationErrorCode import FieldValidationErrorCode


class TestCase(GenreTestCase, PrivateForeignKeyFilterTestCase):

    def setUp(self):
        super().setUp(allow_empty_value=True)

    def test_invalid_uuid_then_error(self):
        self.model_fixture_factory.create_genre(name="Rock")

        response = self._get_genres(**{FilterfFields.PARENT: 'invalid-uuid'})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error['field'] == FilterfFields.PARENT
        assert error['code'] == FieldValidationErrorCode.INVALID_FORMAT

    def test_of_another_user_then_empty(self):
        test_user1_genre = self.model_fixture_factory.create_genre(name="Rock")
        self.model_fixture_factory.create_genre(name="Pop", parent=test_user1_genre)

        self._login_as_test_user2()
        response = self._get_genres(**{FilterfFields.PARENT: test_user1_genre.uuid})
        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 0

    def test_not_provided_then_results(self):
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")
        self.model_fixture_factory.create_genre(name="Pop", parent=genre_rock)

        response = self._get_genres()

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 2

    def test_empty_then_results(self):
        genre_punk = self.model_fixture_factory.create_genre(name="Punk")
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")
        self.model_fixture_factory.create_genre(name="Pop", parent=genre_rock)

        response = self._get_genres(**{FilterfFields.PARENT: ''})

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 2
        result_names = [result[ModelFields.NAME_PUBLIC] for result in self.results]
        assert genre_punk.name in result_names
        assert genre_rock.name in result_names

    def test_exists_then_ok(self):
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")
        genre_punk = self.model_fixture_factory.create_genre(name="Punk", parent=genre_rock)
        genre_slow = self.model_fixture_factory.create_genre(name="Slow", parent=genre_rock)

        response = self._get_genres(**{FilterfFields.PARENT: genre_rock.uuid})

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 2
        result_names = [result[ModelFields.NAME_PUBLIC] for result in self.results]
        assert genre_punk.name in result_names
        assert genre_slow.name in result_names

    def test_no_parent_uuid_corresponds_then_return_nothing(self):
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")
        genre_punk = self.model_fixture_factory.create_genre(name="Punk", parent=genre_rock)

        response = self._get_genres(**{FilterfFields.PARENT: genre_punk.uuid})

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 0
