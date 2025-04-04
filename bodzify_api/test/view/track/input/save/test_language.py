from rest_framework import status

from bodzify_api import settings
from bodzify_api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.serializer.model.uploaded_track.input.put.Fields import Fields as PutFields
from bodzify_api.test.utils.field.body_data.type.NullableCharBodyDataTestCase import NullableCharBodyDataTestCase
from bodzify_api.test.utils.uploaded_track.LibTrackTestFilename import LibTrackTestFilename
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


class TestCase(NullableCharBodyDataTestCase, LibTrackTestCase):

    def test_largest_then_ok(self):
        language = "a" * settings.LANGUAGE_LEN_MAX
        response = self._post_uploaded_track(LibTrackTestFilename.METADATA_NONE_MP3, **{PutFields.LANGUAGE: language})

        assert True
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.language == language

    def test_too_large_then_400_bad_request(self):
        language = "a" * (settings.LANGUAGE_LEN_MAX + 1)
        response = self._post_uploaded_track(LibTrackTestFilename.METADATA_NONE_MP3, **{PutFields.LANGUAGE: language})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error['field'] == PutFields.LANGUAGE
        assert error['code'] == FieldValidationErrorCode.STRING_TOO_LONG

    def test_empty_then_ok(self):
        response = self._post_uploaded_track(LibTrackTestFilename.METADATA_NONE_MP3, **{PutFields.LANGUAGE: ""})

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.language == None

    def test_multi_value_then_400_bad_request(self):
        response = self._post_uploaded_track(LibTrackTestFilename.METADATA_NONE_MP3, **{PutFields.LANGUAGE: ['a', 'b']})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error['field'] == PutFields.LANGUAGE
        assert error['code'] == FieldValidationErrorCode.FORMAT_INVALID
