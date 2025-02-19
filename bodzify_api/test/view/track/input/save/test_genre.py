from rest_framework import status

from bodzify_api import settings
from bodzify_api.serializer.schema.model.lib_track.input.post.post import Fields as PostFields
from bodzify_api.test.view.track.input.save.FieldModelStrTestCase import FieldModelStrTestCase
from bodzify_api.validator.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.view.error.ErrorResponseFields import ErrorResponseFields


class TestCase(FieldModelStrTestCase):

    def test_longest_then_ok(self):
        genre_name = "a" * settings.CRITERIA_NAME_LEN_MAX
        data = {PostFields.GENRE_NAME: genre_name}
        response = self._post_lib_track_with_generic_sample_no_tags(**data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.genre
        assert self.saved_object.genre.name == genre_name

    def test_too_long_then_error(self):
        genre_name = "a" * (settings.CRITERIA_NAME_LEN_MAX + 1)
        data = {PostFields.GENRE_NAME: genre_name}
        response = self._post_lib_track_with_generic_sample_no_tags(**data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error[ErrorResponseFields.FIELD] == PostFields.GENRE_NAME
        assert error[ErrorResponseFields.CODE] == FieldValidationErrorCode.STRING_TOO_LONG.value

    def test_empty_then_none(self):
        data = {PostFields.GENRE_NAME: ''}
        response = self._post_lib_track_with_generic_sample_no_tags(**data)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.genre == None

    def test_existing_then_ok(self):
        genre_name = "Kopoe"
        self.model_fixture_factory.create_genre(name=genre_name)

        data = {PostFields.GENRE_NAME: genre_name}
        response = self._post_lib_track_with_generic_sample_no_tags(**data)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.genre
        assert self.saved_object.genre.name == genre_name

    def test_not_existing(self):
        genre_name = "hoho"

        data = {PostFields.GENRE_NAME: genre_name}
        response = self._post_lib_track_with_generic_sample_no_tags(**data)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.genre
        assert self.saved_object.genre.name == genre_name

    def test_new_so_parent_none(self):
        genre_name = "Rock"

        data = {PostFields.GENRE_NAME: genre_name}
        response = self._post_lib_track_with_generic_sample_no_tags(**data)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.genre
        assert self.saved_object.genre.parent == None
