from rest_framework import status

from bodzify_api import settings
from bodzify_api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.serializer.model.lib_track.input.post.Fields import Fields as PostFields
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase
from bodzify_api.utils.data_transformer import to_camel_case
from bodzify_api.view.error.ErrorResponseFields import ErrorResponseFields


class TestCase(LibTrackTestCase):

    def test_empty_then_none(self):
        response = self._post_lib_track_with_generic_sample_no_tags(**{PostFields.TRACK_NUMBER: None})

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.track_number == None

    def test_empty_string_then_none(self):
        response = self._post_lib_track_with_generic_sample_no_tags(**{PostFields.TRACK_NUMBER: ''})

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.track_number == None

    def test_zero_then_error(self):
        response = self._post_lib_track_with_generic_sample_no_tags(**{PostFields.TRACK_NUMBER: 0})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error[ErrorResponseFields.FieldErrors.FIELD] == to_camel_case(PostFields.TRACK_NUMBER)
        assert error[ErrorResponseFields.FieldErrors.CODE] == FieldValidationErrorCode.TRACK_NUMBER_TOO_SMALL

    def test_one_then_ok(self):
        track_number = 1

        response = self._post_lib_track_with_generic_sample_no_tags(
            albumName='hey', track_number=track_number)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.track_number == track_number

    def test_max_then_ok(self):
        track_number = settings.LIB_TRACK_TRACK_NUMBER_MAX
        response = self._post_lib_track_with_generic_sample_no_tags(
            album_name='album', track_number=track_number)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.track_number == track_number

    def test_max_plus_one_then_error(self):
        response = self._post_lib_track_with_generic_sample_no_tags(
            album_name='album', track_number=settings.LIB_TRACK_TRACK_NUMBER_MAX + 1)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error[ErrorResponseFields.FieldErrors.FIELD] == to_camel_case(PostFields.TRACK_NUMBER)
        assert error[ErrorResponseFields.FieldErrors.CODE] == FieldValidationErrorCode.TRACK_NUMBER_TOO_LARGE

    def test_negative_one_then_error(self):
        response = self._post_lib_track_with_generic_sample_no_tags(album_name='album', track_number=-1)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error[ErrorResponseFields.FieldErrors.FIELD] == to_camel_case(PostFields.TRACK_NUMBER)
        assert error[ErrorResponseFields.FieldErrors.CODE] == FieldValidationErrorCode.TRACK_NUMBER_TOO_SMALL

    def test_not_integer_then_error(self):
        response = self._post_lib_track_with_generic_sample_no_tags(**{PostFields.TRACK_NUMBER: 5.5})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error[ErrorResponseFields.FieldErrors.FIELD] == to_camel_case(PostFields.TRACK_NUMBER)
        assert error[ErrorResponseFields.FieldErrors.CODE] == FieldValidationErrorCode.INVALID_FORMAT
