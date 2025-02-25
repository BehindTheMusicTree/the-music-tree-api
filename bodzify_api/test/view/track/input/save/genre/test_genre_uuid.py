from rest_framework import status

from bodzify_api.exception.validation.FieldValidationErrorCode import \
    FieldValidationErrorCode
from bodzify_api.serializer.model.lib_track.input.post.Fields import \
    Fields as PostFields
from bodzify_api.test.utils.field.body_data.type.to_extend_from.ForeignKeyBodyDataTestCase import \
    ForeignKeyBodyDataTestCase
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase
from bodzify_api.utils.data_transformer import to_camel_case
from bodzify_api.view.error.ErrorResponseFields import ErrorResponseFields


class TestCase(ForeignKeyBodyDataTestCase, LibTrackTestCase):

    def test_non_existing_then_error(self):
        non_exisintg_uuid = "00000000-0000-0000-0000-000000000000"
        response = self._post_lib_track_with_generic_sample_no_tags(genre_uuid=non_exisintg_uuid)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error[ErrorResponseFields.FieldErrors.FIELD] == to_camel_case(PostFields.GENRE_UUID)
        assert error[ErrorResponseFields.FieldErrors.CODE] == FieldValidationErrorCode.INVALID_REFERENCE.value

    def test_value_then_ok(self):
        genre = self.model_fixture_factory.create_genre(name="rock")
        response = self._post_lib_track_with_generic_sample_no_tags(**{PostFields.GENRE_UUID: genre.uuid})

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object
        assert self.saved_object.genre == genre

    def test_empty_then_none(self):
        response = self._post_lib_track_with_generic_sample_no_tags(genre_uuid="")

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.genre is None

    def test_multiple_values_then_error(self):
        genre = self.model_fixture_factory.create_genre(name="rock")
        data = {
            PostFields.GENRE_UUID: genre.uuid,
            PostFields.GENRE_UUID: genre.uuid,
        }
        response = self._post_lib_track_with_generic_sample_no_tags(**data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error[ErrorResponseFields.FieldErrors.FIELD] == to_camel_case(PostFields.GENRE_UUID)
        assert error[ErrorResponseFields.FieldErrors.CODE] == FieldValidationErrorCode.FIELD_DUPLICATE.value

    def test_invalid_uuid_then_error(self):
        response = self._post_lib_track_with_generic_sample_no_tags(genre_uuid="invalid")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error[ErrorResponseFields.FieldErrors.FIELD] == PostFields.GENRE_UUID
        assert error[ErrorResponseFields.FieldErrors.CODE] == FieldValidationErrorCode.INVALID_FORMAT.value
