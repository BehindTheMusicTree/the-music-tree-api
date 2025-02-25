from rest_framework import status

from bodzify_api.exception.validation.FieldValidationErrorCode import \
    FieldValidationErrorCode
from bodzify_api.serializer.model.criteria.input.Fields import \
    Fields as CriteriaFields
from bodzify_api.serializer.model.lib_track.input.post.Fields import \
    Fields as PostFields
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase
from bodzify_api.utils.data_transformer import to_camel_case
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
        genre = self.model_fixture_factory.create_genre(**{CriteriaFields.NAME_PUBLIC: 'Rock'})
        data = {
            PostFields.GENRE_NAME: 'dnb',
            PostFields.GENRE_UUID: genre.uuid,
        }
        response = self._post_lib_track_with_generic_sample_no_tags(**data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert self.bad_request_result_field_errors[0][
            ErrorResponseFields.FieldErrors.FIELD] == to_camel_case(
            PostFields.GENRE_NAME)
        assert self.bad_request_result_field_errors[0][
            ErrorResponseFields.FieldErrors.CODE] == FieldValidationErrorCode.MUTUALLY_EXCLUSIVE.value
