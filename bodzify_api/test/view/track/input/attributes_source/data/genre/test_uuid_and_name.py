from rest_framework import status

from bodzify_api import settings
from bodzify_api.serializer.schema.model.lib_track.input.post import Fields as PostFields
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase
from bodzify_api.validator.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.view.error.ErrorResponseFields import ErrorResponseFields


class TestCase(LibTrackTestCase):

    def test_uuid_and_name_fields_null_then_none(self):
        data = {
            PostFields.GENRE_NAME: None,
            PostFields.GENRE_UUID: None,
        }
        response = self._post_lib_track_with_generic_sample_no_tags(**data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.genre == None

    def test_uuid_and_name_both_fed_then_error(self):
        data = {
            PostFields.GENRE_NAME: 'd',
            PostFields.GENRE_UUID: 'k' * settings.UUID_LEN,
        }
        response = self._post_lib_track_with_generic_sample_no_tags(**data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert self.bad_request_result_field_errors[0][ErrorResponseFields.FIELD] == PostFields.GENRE_UUID
        assert self.bad_request_result_field_errors[0][
            ErrorResponseFields.CODE] == FieldValidationErrorCode.MUTUALLY_EXCLUSIVE.value
