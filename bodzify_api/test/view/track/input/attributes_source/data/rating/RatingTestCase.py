from rest_framework import status

from bodzify_api.serializer.schema.model.lib_track.input.post import Fields as PostFields
from bodzify_api.test.view.track.input.attributes_source.data.FieldFromDataTestCase import FieldIntFromDataTestCase
from bodzify_api.validator.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.view.error.ErrorResponseFields import ErrorResponseFields


class RatingTestCase(FieldIntFromDataTestCase):
    post_field_key = PostFields.RATING

    def test_value_then_ok(self):
        value = 1
        response = self._post_lib_track_with_generic_sample_no_tags(**{PostFields.RATING: value})
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.rating == value

    def test_empty_then_none(self):
        response = self._post_lib_track_with_generic_sample_1_star(**{PostFields.RATING: ""})
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.rating == None

    def test_rating_too_large_then_error(self):
        response = self._post_lib_track_with_generic_sample_no_tags(**{PostFields.RATING: 11})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error[ErrorResponseFields.FIELD] == PostFields.RATING
        assert error[ErrorResponseFields.CODE] == FieldValidationErrorCode.RATING_TOO_LARGE

    def test_rating_negative_then_error(self):
        response = self._post_lib_track_with_generic_sample_no_tags(**{PostFields.RATING: -1})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error[ErrorResponseFields.FIELD] == PostFields.RATING
        assert error[ErrorResponseFields.CODE] == FieldValidationErrorCode.RATING_TOO_SMALL

    def test_field_twice_then_error(self):
        response = self._post_lib_track_with_generic_sample_no_tags(**{PostFields.RATING: [1, 2]})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error[ErrorResponseFields.FIELD] == PostFields.RATING
        assert error[ErrorResponseFields.CODE] == FieldValidationErrorCode.INVALID_FORMAT
