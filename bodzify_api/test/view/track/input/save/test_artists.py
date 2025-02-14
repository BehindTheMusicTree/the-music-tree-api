from rest_framework import status

from bodzify_api import settings
from bodzify_api.model.artist.Artist import Artist
from bodzify_api.serializer.schema.model.lib_track.input.extract import Fields as ExtractFields
from bodzify_api.test.view.track.input.save.FieldModelStrTestCase import FieldModelStrTestCase
from bodzify_api.validator.FieldValidationErrorCode import FieldValidationErrorCode


class TestCase(FieldModelStrTestCase):

    def test_longest_then_ok(self) -> None:
        artist_name = "a" * settings.ARTIST_NAME_LEN_MAX
        data = {ExtractFields.ARTISTS_NAMES_STR: artist_name}
        response = self._post_lib_track_with_generic_sample_no_tags(**data)

        assert response.status_code == status.HTTP_201_CREATED
        artists_list: list[Artist] = list(self.saved_lib_track.artists.all())
        assert len(artists_list) > 0
        assert artists_list[0].name == artist_name

    def test_too_long_then_error(self):
        artist_name = "a" * (settings.ARTIST_NAME_LEN_MAX + 1)
        data = {ExtractFields.ARTISTS_NAMES_STR: artist_name}
        response = self._post_lib_track_with_generic_sample_no_tags(**data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error['field'] == ExtractFields.ARTISTS_NAMES_STR
        assert error['code'] == FieldValidationErrorCode.INVALID_FORMAT

    def test_empty_then_none(self):
        response = self._post_lib_track_with_generic_sample_no_tags(**{ExtractFields.ARTISTS_NAMES_STR: ''})

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.artists.count() == 0

    def test_existing(self) -> None:
        artist_name = "Kopoe"
        self.model_fixture_factory.create_artist(name=artist_name)

        data = {ExtractFields.ARTISTS_NAMES_STR: artist_name}
        response = self._post_lib_track_with_generic_sample_no_tags(**data)

        assert response.status_code == status.HTTP_201_CREATED
        artists_list: list[Artist] = list(self.saved_lib_track.artists.all())
        assert len(artists_list) > 0
        assert artists_list[0].name == artist_name

    def test_not_existing(self) -> None:
        artist_name = "hoho"
        data = {ExtractFields.ARTISTS_NAMES_STR: artist_name}
        response = self._post_lib_track_with_generic_sample_no_tags(**data)

        assert response.status_code == status.HTTP_201_CREATED
        artists_list: list[Artist] = list(self.saved_lib_track.artists.all())
        assert len(artists_list) > 0
        assert artists_list[0].name == artist_name

    def test_multiple_existing_artists(self) -> None:
        artist1_name = "Kopoe"
        artist2_name = "Steeve"
        self.model_fixture_factory.create_artist(name=artist1_name)
        self.model_fixture_factory.create_artist(name=artist2_name)

        data = {ExtractFields.ARTISTS_NAMES_STR: f"{artist1_name}, {artist2_name}"}
        response = self._post_lib_track_with_generic_sample_no_tags(**data)

        assert response.status_code == status.HTTP_201_CREATED
        artists_list: list[Artist] = list(self.saved_lib_track.artists.all().order_by('name'))
        assert len(artists_list) == 2
        assert artists_list[0].name == artist1_name
        assert artists_list[1].name == artist2_name

    def test_multiple_non_existing_artists(self) -> None:
        artist1_name = "NewArtist1"
        artist2_name = "NewArtist2"
        artist3_name = "NewArtist3"

        data = {ExtractFields.ARTISTS_NAMES_STR: f"{artist1_name}, {artist2_name}, {artist3_name}"}
        response = self._post_lib_track_with_generic_sample_no_tags(**data)

        assert response.status_code == status.HTTP_201_CREATED
        artists_list: list[Artist] = list(self.saved_lib_track.artists.all().order_by('name'))
        assert len(artists_list) == 3
        assert artists_list[0].name == artist1_name
        assert artists_list[1].name == artist2_name
        assert artists_list[2].name == artist3_name

    def test_mix_existing_and_non_existing_artists(self) -> None:
        existing_artist = "Kopoe"
        self.model_fixture_factory.create_artist(name=existing_artist)
        new_artist1 = "NewArtist1"
        new_artist2 = "NewArtist2"

        data = {ExtractFields.ARTISTS_NAMES_STR: f"{existing_artist}, {new_artist1}, {new_artist2}"}
        response = self._post_lib_track_with_generic_sample_no_tags(**data)

        assert response.status_code == status.HTTP_201_CREATED
        artists_list: list[Artist] = list(self.saved_lib_track.artists.all().order_by('name'))
        assert len(artists_list) == 3
        assert artists_list[0].name == existing_artist
        assert artists_list[1].name == new_artist1
        assert artists_list[2].name == new_artist2

    def test_multiple_artists_one_too_long_then_error(self) -> None:
        valid_artist = "ValidArtist"
        too_long_artist = "a" * (settings.ARTIST_NAME_LEN_MAX + 1)

        data = {ExtractFields.ARTISTS_NAMES_STR: f"{valid_artist}, {too_long_artist}"}
        response = self._post_lib_track_with_generic_sample_no_tags(**data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error['field'] == ExtractFields.ARTISTS_NAMES_STR
        assert error['code'] == FieldValidationErrorCode.INVALID_FORMAT

    def test_multiple_artists_with_duplicates_then_error(self) -> None:
        artist_name = "DuplicateArtist"
        data = {ExtractFields.ARTISTS_NAMES_STR: f"{artist_name}, {artist_name}, {artist_name}"}
        response = self._post_lib_track_with_generic_sample_no_tags(**data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error['field'] == ExtractFields.ARTISTS_NAMES_STR
        assert error['code'] == FieldValidationErrorCode.ARTIST_NAMES_DUPLICATE

    def test_multiple_artists_with_empty_names_then_error(self) -> None:
        valid_artist = "ValidArtist"
        data = {ExtractFields.ARTISTS_NAMES_STR: f"{valid_artist}, , , {valid_artist}"}
        response = self._post_lib_track_with_generic_sample_no_tags(**data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error['field'] == ExtractFields.ARTISTS_NAMES_STR
        assert error['code'] == FieldValidationErrorCode.ARTIST_NAME_EMPTY_IN_LIST
