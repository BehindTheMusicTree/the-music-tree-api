from rest_framework import status

from bodzify_api.serializer.schema.model.lib_track.input.post.Fields import Fields as PostFields
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase
from bodzify_api.validator.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.view.error.ErrorResponseFields import ErrorResponseFields


class TestCase(LibTrackTestCase):

    def test_empty_then_none(self):
        response = self._post_lib_track_with_generic_sample_no_tags(**{PostFields.RATING: None})

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.rating == None

    def test_zero(self):
        rating = 0
        response = self._post_lib_track_with_generic_sample_no_tags(**{PostFields.RATING: rating})

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.rating == rating

    def test_four(self):
        rating = 4
        response = self._post_lib_track_with_generic_sample_no_tags(**{PostFields.RATING: rating})

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.rating == rating

    def test_ten(self):
        rating = 10
        response = self._post_lib_track_with_generic_sample_no_tags(**{PostFields.RATING: rating})

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.rating == rating

    def test_error_when_above_maximum(self):
        response = self._post_lib_track_with_generic_sample_no_tags(**{PostFields.RATING: 11})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error[ErrorResponseFields.FieldErrors.FIELD] == PostFields.RATING
        assert error[ErrorResponseFields.FieldErrors.CODE] == FieldValidationErrorCode.RATING_TOO_LARGE.value

    def test_error_when_below_minimum(self):
        response = self._post_lib_track_with_generic_sample_no_tags(**{PostFields.RATING: -1})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error[ErrorResponseFields.FieldErrors.FIELD] == PostFields.RATING
        assert error[ErrorResponseFields.FieldErrors.CODE] == FieldValidationErrorCode.RATING_TOO_SMALL.value

    def test_error_when_not_integer(self):
        response = self._post_lib_track_with_generic_sample_no_tags(**{PostFields.RATING: 5.5})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error[ErrorResponseFields.FieldErrors.FIELD] == PostFields.RATING
        assert error[ErrorResponseFields.FieldErrors.CODE] == FieldValidationErrorCode.INVALID_FORMAT.value
