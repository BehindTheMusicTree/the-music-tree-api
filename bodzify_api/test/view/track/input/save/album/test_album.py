from rest_framework import status

from bodzify_api import settings
from bodzify_api.serializer.schema.model.lib_track.input.extract import Fields as ExtractFields
from bodzify_api.test.view.track.input.save.FieldModelStrTestCase import FieldModelStrTestCase
from bodzify_api.validator.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.view.error.ErrorResponseFields import ErrorResponseFields


class TestCase(FieldModelStrTestCase):

    def test_longest_then_ok(self):
        album_name = "a" * settings.ALBUM_NAME_LEN_MAX
        response = self._post_lib_track_with_generic_sample_no_tags(**{ExtractFields.ALBUM_NAME: album_name})

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.album
        assert self.saved_object.album.name == album_name

    def test_too_long_then_error(self):
        album_name = "a" * (settings.ALBUM_NAME_LEN_MAX + 1)
        response = self._post_lib_track_with_generic_sample_no_tags(**{ExtractFields.ALBUM_NAME: album_name})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error[ErrorResponseFields.FIELD] == ExtractFields.ALBUM_NAME
        assert error[ErrorResponseFields.CODE] == FieldValidationErrorCode.STRING_TOO_LONG.value

    def test_empty_then_none(self):
        response = self._post_lib_track_with_generic_sample_no_tags(**{ExtractFields.ALBUM_NAME: ''})

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.album == None

    def test_existing_then_ok(self):
        album_name = "Kopoe"
        self.model_fixture_factory.create_album(name=album_name)

        response = self._post_lib_track_with_generic_sample_no_tags(**{ExtractFields.ALBUM_NAME: album_name})

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.album
        assert self.saved_object.album.name == album_name

    def test_not_existing(self):
        album_name = "hoho"

        response = self._post_lib_track_with_generic_sample_no_tags(**{ExtractFields.ALBUM_NAME: album_name})

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.album
        assert self.saved_object.album.name == album_name
