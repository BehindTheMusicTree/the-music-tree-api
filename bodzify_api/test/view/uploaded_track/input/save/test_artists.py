from rest_framework import status

from bodzify_api import settings
from bodzify_api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.model.artist.Artist import Artist
from bodzify_api.serializer.model.uploaded_track.input.post.Fields import Fields as PostFields
from bodzify_api.test.utils.field.body_data.type.list.NullableListBodyDataTestCase import NullableListBodyDataTestCase
from bodzify_api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename
from bodzify_api.test.view.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase
from bodzify_api.utils.data_transformer import to_camel_case


class TestCase(NullableListBodyDataTestCase, UploadedTrackTestCase):

    def test_largest_then_ok(self) -> None:
        artist_name = "a" * settings.ARTIST_NAME_LEN_MAX
        data = {PostFields.ARTISTS_NAMES_MULTIPART: [artist_name]}
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_MP3, **data)

        assert response.status_code == status.HTTP_201_CREATED
        artists_list: list[Artist] = list(self.saved_object.artists.all())
        assert len(artists_list) > 0
        assert artists_list[0].name == artist_name

    def test_one_too_large_then_400_bad_request(self):
        artist_name = "a" * (settings.ARTIST_NAME_LEN_MAX + 1)
        data = {PostFields.ARTISTS_NAMES_MULTIPART: [artist_name]}
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_MP3, **data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error['field'] == to_camel_case(PostFields.ARTISTS_NAMES_MULTIPART)
        assert error['code'] == FieldValidationErrorCode.STRING_TOO_LONG

    def test_one_is_max_length_and_another_one_is_one_char_then_ok(self) -> None:
        artist_name = "a" * settings.ARTIST_NAME_LEN_MAX
        artist_name2 = "b"
        data = {PostFields.ARTISTS_NAMES_MULTIPART: [artist_name, artist_name2]}
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_MP3, **data)

        assert response.status_code == status.HTTP_201_CREATED
        artists_list: list[Artist] = list(self.saved_object.artists.all())
        assert len(artists_list) == 2
        assert artists_list[0].name == artist_name
        assert artists_list[1].name == artist_name2

    def test_malformed_array_then_400_bad_request(self) -> None:
        malformed_post_multipart_field_name = "artists_names"
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_MP3, **
                                             {malformed_post_multipart_field_name: ['muse']})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error['field'] == to_camel_case(malformed_post_multipart_field_name)
        assert error['code'] == FieldValidationErrorCode.LIST_MALFORMED

        track = self.model_fixture_factory.create_uploaded_track_with_file(title="koko")
        malformed_put_json_field_name = "artists_names[]"
        response = self._put_uploaded_track(track.uuid, **{malformed_put_json_field_name: ['muse']})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error['field'] == to_camel_case(malformed_put_json_field_name)
        assert error['code'] == FieldValidationErrorCode.UNKNOWN

    def test_comma_separated_then_only_one_value(self):
        data = {PostFields.ARTISTS_NAMES_MULTIPART: "Muse, Kopoe"}
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_MP3, **data)

        assert response.status_code == status.HTTP_201_CREATED
        artists_list: list[Artist] = list(self.saved_object.artists.all())
        assert len(artists_list) == 1
        assert artists_list[0].name == "Muse, Kopoe"

    def test_duplicate_values_then_400_bad_request(self) -> None:
        data = {PostFields.ARTISTS_NAMES_MULTIPART: ['Muse', 'Muse']}
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_MP3, **data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error['field'] == to_camel_case(PostFields.ARTISTS_NAMES_MULTIPART)
        assert error['code'] == FieldValidationErrorCode.LIST_VALUE_DUPLICATE

    def test_empty_then_ok(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_MP3,
                                             **{PostFields.ARTISTS_NAMES_MULTIPART: []})

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.artists.count() == 0

    def test_multiple_with_one_empty_then_400_bad_request(self) -> None:
        artist_name = "Muse"
        data = {PostFields.ARTISTS_NAMES_MULTIPART: [artist_name, ""]}
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_MP3, **data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error['field'] == to_camel_case(PostFields.ARTISTS_NAMES_MULTIPART)
        assert error['code'] == FieldValidationErrorCode.LIST_VALUE_EMPTY

    def test_one_existing_then_create_it(self) -> None:
        artist_name = "Kopoe"
        self.model_fixture_factory.create_artist(name=artist_name)

        data = {PostFields.ARTISTS_NAMES_MULTIPART: [artist_name]}
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_MP3, **data)

        assert response.status_code == status.HTTP_201_CREATED
        artists_list: list[Artist] = list(self.saved_object.artists.all())
        assert len(artists_list) > 0
        assert artists_list[0].name == artist_name

    def test_one_not_existing_then_ok(self) -> None:
        artist_name = "hoho"
        data = {PostFields.ARTISTS_NAMES_MULTIPART: [artist_name]}
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_MP3, **data)

        assert response.status_code == status.HTTP_201_CREATED
        artists_list: list[Artist] = list(self.saved_object.artists.all())
        assert len(artists_list) > 0
        assert artists_list[0].name == artist_name

    def test_multiple_existing_artists_then_ok(self) -> None:
        artist1_name = "Kopoe"
        artist2_name = "Steeve"
        self.model_fixture_factory.create_artist(name=artist1_name)
        self.model_fixture_factory.create_artist(name=artist2_name)

        data = {PostFields.ARTISTS_NAMES_MULTIPART: [artist1_name, artist2_name]}
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_MP3, **data)

        assert response.status_code == status.HTTP_201_CREATED
        artists_list: list[Artist] = list(self.saved_object.artists.all())
        assert len(artists_list) == 2
        assert artists_list[0].name == artist1_name
        assert artists_list[1].name == artist2_name

    def test_multiple_non_existing_artists_then_create_them(self) -> None:
        artist1_name = "NewArtist1"
        artist2_name = "NewArtist2"
        artist3_name = "NewArtist3"

        data = {PostFields.ARTISTS_NAMES_MULTIPART: [artist1_name, artist2_name, artist3_name]}
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_MP3, **data)

        assert response.status_code == status.HTTP_201_CREATED
        artists_list: list[Artist] = list(self.saved_object.artists.all().order_by('name'))
        assert len(artists_list) == 3
        assert artists_list[0].name == artist1_name
        assert artists_list[1].name == artist2_name
        assert artists_list[2].name == artist3_name

    def test_mix_existing_and_non_existing_artists(self) -> None:
        existing_artist = "Kopoe"
        self.model_fixture_factory.create_artist(name=existing_artist)
        new_artist1 = "NewArtist1"
        new_artist2 = "NewArtist2"

        data = {PostFields.ARTISTS_NAMES_MULTIPART: [existing_artist, new_artist1, new_artist2]}
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_MP3, **data)

        assert response.status_code == status.HTTP_201_CREATED
        artists_list: list[Artist] = list(self.saved_object.artists.all().order_by('name'))
        assert len(artists_list) == 3
        assert artists_list[0].name == existing_artist
        assert artists_list[1].name == new_artist1
        assert artists_list[2].name == new_artist2

    def test_multiple_with_one_too_large_then_400_bad_request(self) -> None:
        valid_artist = "ValidArtist"
        too_long_artist = "a" * (settings.ARTIST_NAME_LEN_MAX + 1)

        data = {PostFields.ARTISTS_NAMES_MULTIPART: [valid_artist, too_long_artist]}
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_MP3, **data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error['field'] == to_camel_case(PostFields.ARTISTS_NAMES_MULTIPART)
        assert error['code'] == FieldValidationErrorCode.STRING_TOO_LONG
