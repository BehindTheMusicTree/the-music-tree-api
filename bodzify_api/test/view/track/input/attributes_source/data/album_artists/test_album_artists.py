from typing import Optional

from rest_framework import status

from bodzify_api.model.artist.Artist import Artist
from bodzify_api.serializer.schema.model.lib_track.input.post import Fields as PostFields
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase
from bodzify_api.validator.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.view.error.ErrorResponseFields import ErrorResponseFields


class TestCase(LibTrackTestCase):

    def test_value_then_ok(self):
        value = 'astititit'
        data = {
            PostFields.ALBUM_NAME: 'albumito',
            PostFields.ALBUM_ARTISTS_NAMES: value
        }
        response = self._post_lib_track_with_generic_sample_no_tags(**data)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.album
        artist: Optional[Artist] = self.saved_object.album.album_artists.first()
        assert artist
        assert artist.name == value

    def test_empty_then_none(self):
        data = {
            PostFields.ALBUM_NAME: "albumito",
            PostFields.ALBUM_ARTISTS_NAMES: ""
        }
        response = self._post_lib_track_with_generic_sample_1_star(**data)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.album
        assert self.saved_object.album.album_artists.count() == 0

    def test_multiple_values_then_error(self):
        data = {
            PostFields.ALBUM_NAME: "albumito",
            PostFields.ALBUM_ARTISTS_NAMES: "astititit,astititit"
        }
        response = self._post_lib_track_with_generic_sample_1_star(**data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert self.bad_request_result_field_errors[0][ErrorResponseFields.FIELD] == PostFields.ALBUM_ARTISTS_NAMES
        assert self.bad_request_result_field_errors[0][
            ErrorResponseFields.CODE] == FieldValidationErrorCode.UNEXPECTED_LIST.value
