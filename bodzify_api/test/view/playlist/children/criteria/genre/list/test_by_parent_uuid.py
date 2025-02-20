from rest_framework import status

from bodzify_api.serializer.model.playlist.children.criteria.output.detailed import Fields as RietrieveFields
from bodzify_api.test.utils.field.filter.foreign_key.PrivateForeignKeyFilterTestCase import PrivateForeignKeyFilterTestCase
from bodzify_api.test.view.playlist.children.criteria.genre.GenrePlaylistTestCase import GenrePlaylistTestCase
from bodzify_api.validator.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.view.error.ErrorResponseFields import ErrorResponseFields


class TestCase(GenrePlaylistTestCase, PrivateForeignKeyFilterTestCase):

    def setUp(self, methods_names_to_implement=None):
        return super().setUp(allow_empty_value=True, methods_names_to_implement=methods_names_to_implement)

    def test_not_provided_then_results(self):
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")
        self.model_fixture_factory.create_genre(name="Rockabilly")
        self.model_fixture_factory.create_genre(name="Koko", parent=genre_rock)

        response = self._get_genre_playlists()

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 4

    def test_invalid_uuid_then_error(self):
        self.model_fixture_factory.create_genre(name="Rock")

        response = self._get_genre_playlists(**{RietrieveFields.PARENT: 'invalid-uuid'})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert self.bad_request_result_field_errors[0][ErrorResponseFields.FieldErrors.FIELD] == RietrieveFields.PARENT
        assert self.bad_request_result_field_errors[0][
            ErrorResponseFields.FieldErrors.CODE] == FieldValidationErrorCode.BLANK.value

    def test_empty_then_results(self):
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")
        genre_rockabilly = self.model_fixture_factory.create_genre(name="Rockabilly")
        genre_koko = self.model_fixture_factory.create_genre(name="Koko", parent=genre_rock)

        response = self._get_genre_playlists(**{RietrieveFields.PARENT: ''})

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 3
        result_names = [result[RietrieveFields.NAME] for result in self.results]
        assert genre_rock.name in result_names
        assert genre_rockabilly.name in result_names
        assert genre_koko.name not in result_names

    def test_genres_playlist_parent_corresponds_to_filter_then_return_instances(self):
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")
        genre_rockabilly = self.model_fixture_factory.create_genre(name="Rockabilly", parent=genre_rock)
        genre_punk = self.model_fixture_factory.create_genre(name="Punk", parent=genre_rock)

        response = self._get_genre_playlists(**{RietrieveFields.PARENT: genre_rock.criteria_playlist.uuid})

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 2
        result_names = [result[RietrieveFields.NAME] for result in self.results]
        assert genre_rockabilly.name in result_names
        assert genre_punk.name in result_names
