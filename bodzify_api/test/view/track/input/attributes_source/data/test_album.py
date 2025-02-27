from rest_framework import status

from bodzify_api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.serializer.model.lib_track.input.post.Fields import Fields as PostFields
from bodzify_api.test.utils.field.body_data.type.NullableCharBodyDataTestCase import NullableCharBodyDataTestCase
from bodzify_api.test.utils.lib_track.TestLibTrackFilename import TestLibTrackFilename
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase
from bodzify_api.view.error.ErrorResponseFields import ErrorResponseFields


class TestCase(LibTrackTestCase, NullableCharBodyDataTestCase):

    def test_value_then_ok(self):
        value = 'fofof'
        response = self._post_lib_track(TestLibTrackFilename.METADATA_NONE_MP3, **{PostFields.ALBUM_NAME: value})

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.album
        assert self.saved_object.album.name == value

    def test_empty_then_none(self):
        response = self._post_lib_track(TestLibTrackFilename.METADATA_NONE_MP3, **{PostFields.ALBUM_NAME: ""})

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.album == None

    def test_list_then_400(self):
        response = self._post_lib_track(TestLibTrackFilename.METADATA_NONE_MP3, **{PostFields.ALBUM_NAME: "a",
                                                                                   PostFields.ALBUM_NAME: "b"})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        error = self.bad_request_result_field_errors[0]
        assert error[ErrorResponseFields.FieldErrors.FIELD] == PostFields.ALBUM_NAME
        assert error[ErrorResponseFields.FieldErrors.CODE] == FieldValidationErrorCode.FIELD_DUPLICATE
