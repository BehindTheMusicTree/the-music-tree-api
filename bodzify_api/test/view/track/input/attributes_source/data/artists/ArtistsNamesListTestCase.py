
from rest_framework import status

from bodzify_api.model.artist.Artist import Artist
from bodzify_api.serializer.schema.model.lib_track.input.post import Fields as PostFields
from bodzify_api.test.field.body_data.type.NullableListDataTestCase import NullableListDataTestCase
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase
from bodzify_api.validator.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.view.error.ErrorResponseFields import ErrorResponseFields


class ArtistsNamesListTestCase(LibTrackTestCase, NullableListDataTestCase):

    def test_array_notation_then_ok(self) -> None:
        artist_name1 = "mat"
        artist_name2 = "muse"
        data = {
            f"{PostFields.ARTISTS_NAMES}[]": [artist_name1, artist_name2]
        }
        response = self._post_lib_track_with_generic_sample_no_tags(**data)

        assert response.status_code == status.HTTP_201_CREATED
        artists_list: list[Artist] = list(self.saved_object.artists.all())
        assert len(artists_list) == 2
        assert {artist.name for artist in artists_list} == {artist_name1, artist_name2}

    def test_empty_array_then_none(self) -> None:
        data = {
            f"{PostFields.ARTISTS_NAMES}[]": []
        }
        response = self._post_lib_track_with_generic_sample_no_tags(**data)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.artists.count() == 0

    def test_values_with_one_empty_then_error(self) -> None:
        data = {
            f"{PostFields.ARTISTS_NAMES}[]": ["mat", ""]
        }
        response = self._post_lib_track_with_generic_sample_no_tags(**data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert self.bad_request_result_field_errors[0][
            ErrorResponseFields.CODE] == FieldValidationErrorCode.ARTIST_NAME_EMPTY_IN_LIST
        assert self.bad_request_result_field_errors[0][ErrorResponseFields.FIELD] == PostFields.ARTISTS_NAMES

    def test_non_array_then_error(self) -> None:
        data = {
            PostFields.ARTISTS_NAMES: "mat"
        }
        response = self._post_lib_track_with_generic_sample_no_tags(**data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert self.bad_request_result_field_errors[0][
            ErrorResponseFields.CODE] == FieldValidationErrorCode.LIST_EXPECTED
        assert self.bad_request_result_field_errors[0][ErrorResponseFields.FIELD] == PostFields.ARTISTS_NAMES

    def test_comma_separated_then_only_one_value(self) -> None:
        artists_names_str = "mat, muse"
        data = {
            PostFields.ARTISTS_NAMES: artists_names_str  # Non-array format
        }
        response = self._post_lib_track_with_generic_sample_no_tags(**data)
        assert response.status_code == status.HTTP_200_OK
        artists_list: list[Artist] = list(self.saved_object.artists.all())
        assert len(artists_list) == 1
        assert artists_list[0].name == artists_names_str

    def test_duplicate_values_then_error(self) -> None:
        data = {
            PostFields.ARTISTS_NAMES: "mat, mat"
        }
        response = self._post_lib_track_with_generic_sample_no_tags(**data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert self.bad_request_result_field_errors[0][
            ErrorResponseFields.CODE] == FieldValidationErrorCode.ARTIST_NAMES_DUPLICATE
        assert self.bad_request_result_field_errors[0][ErrorResponseFields.FIELD] == PostFields.ARTISTS_NAMES
