from rest_framework import status

from bodzify_api import settings
from bodzify_api.serializer.schema.model.lib_track.input.post import Fields as PostFields
from bodzify_api.test.view import album
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase
from bodzify_api.validator.FieldValidationErrorCode import FieldValidationErrorCode


class TestCase(LibTrackTestCase):

    def test_empty_then_none(self):
        response = self._post_lib_track_with_generic_sample_no_tags(**{PostFields.POSITION_IN_ALBUM: None})

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.position_in_album == None

    def test_empty_string_then_none(self):
        response = self._post_lib_track_with_generic_sample_no_tags(**{PostFields.POSITION_IN_ALBUM: ''})

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.position_in_album == None

    def test_zero_then_error(self):
        response = self._post_lib_track_with_generic_sample_no_tags(**{PostFields.POSITION_IN_ALBUM: 0})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error['field'] == PostFields.POSITION_IN_ALBUM
        assert error['code'] == FieldValidationErrorCode.POSITION_IN_ALBUM_TOO_SMALL

    def test_one_then_ok(self):
        position_in_album = 1

        response = self._post_lib_track_with_generic_sample_no_tags(
            albumName='hey', position_in_album=position_in_album)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.position_in_album == position_in_album

    def test_max_then_ok(self):
        position_in_album = settings.LIB_TRACK_POSITION_IN_ALBUM_MAX
        response = self._post_lib_track_with_generic_sample_no_tags(
            album_name='album', position_in_album=position_in_album)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.position_in_album == position_in_album

    def test_max_plus_one_then_error(self):
        response = self._post_lib_track_with_generic_sample_no_tags(
            album_name='album', position_in_album=settings.LIB_TRACK_POSITION_IN_ALBUM_MAX + 1)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error['field'] == PostFields.POSITION_IN_ALBUM
        assert error['code'] == FieldValidationErrorCode.POSITION_IN_ALBUM_TOO_LARGE

    def test_negative_one_then_error(self):
        response = self._post_lib_track_with_generic_sample_no_tags(album_name='album', position_in_album=-1)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error['field'] == PostFields.POSITION_IN_ALBUM
        assert error['code'] == FieldValidationErrorCode.POSITION_IN_ALBUM_TOO_SMALL

    def test_not_integer_then_error(self):
        response = self._post_lib_track_with_generic_sample_no_tags(**{PostFields.POSITION_IN_ALBUM: 5.5})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error['field'] == PostFields.POSITION_IN_ALBUM
        assert error['code'] == FieldValidationErrorCode.INVALID_FORMAT
