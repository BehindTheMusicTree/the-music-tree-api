from rest_framework import status

from api import settings
from api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from api.serializer.model.track.input.Fields import Fields as PostFields
from api.test.utils.field.body_data.type.NotNullableCharBodyDataTestCase import NotNullableCharBodyDataTestCase
from api.test.integration.view.track.TrackTestCase import TrackTestCase


class TestCase(NotNullableCharBodyDataTestCase, TrackTestCase):

    def test_largest_then_ok(self):
        value = "a" * settings.TRACK_TITLE_LEN_MAX
        response = self._post_track(**{PostFields.TITLE: value})

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.title == value

    def test_too_large_then_400_bad_request(self):
        value = "a" * (settings.TRACK_TITLE_LEN_MAX + 1)
        response = self._post_track(**{PostFields.TITLE: value})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error['field'] == PostFields.TITLE
        assert error['code'] == FieldValidationErrorCode.STRING_TOO_LONG

    def test_empty_then_400_bad_request(self):
        response = self._post_track(**{PostFields.TITLE: ""})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error['field'] == PostFields.TITLE
        assert error['code'] == FieldValidationErrorCode.BLANK

    def test_multi_value_then_400_bad_request(self):
        response = self._post_track(**{PostFields.TITLE: ["a", "b"]})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error['field'] == PostFields.TITLE
        assert error['code'] == FieldValidationErrorCode.DUPLICATE
