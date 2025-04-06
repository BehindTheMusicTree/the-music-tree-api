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
        data = {PostFields.ALBUM_NAME: "Best Of", PostFields.ALBUM_ARTISTS_NAMES_MULTIPART: [artist_name]}
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_MP3, **data)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.album
        artists_list: list[Artist] = list(self.saved_object.album.album_artists.all())
        assert len(artists_list) > 0
        assert artists_list[0].name == artist_name

    def test_one_too_large_then_400_bad_request(self):
        artist_name = "a" * (settings.ARTIST_NAME_LEN_MAX + 1)
        data = {PostFields.ALBUM_NAME: "Best Of", PostFields.ALBUM_ARTISTS_NAMES_MULTIPART: artist_name}
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_MP3, **data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error['field'] == to_camel_case(PostFields.ALBUM_ARTISTS_NAMES_MULTIPART)
        assert error['code'] == FieldValidationErrorCode.STRING_TOO_LONG

    def test_malformed_array_then_400_bad_request(self) -> None:
        malformed_post_multipart_field_name = "album_artists_names"
        data = {PostFields.ALBUM_NAME: "Best Of", malformed_post_multipart_field_name: ['muse']}
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_MP3, **data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error['field'] == to_camel_case(malformed_post_multipart_field_name)
        assert error['code'] == FieldValidationErrorCode.LIST_MALFORMED

        track = self.model_fixture_factory.create_uploaded_track_with_file(title="koko")
        malformed_put_json_field_name = "album_artists_names[]"
        data = {PostFields.ALBUM_NAME: "Best Of", malformed_put_json_field_name: ['muse']}
        response = self._put_uploaded_track(track.uuid, **data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error['field'] == to_camel_case(malformed_put_json_field_name)
        assert error['code'] == FieldValidationErrorCode.UNKNOWN

    def test_empty_then_ok(self):
        data = {PostFields.ALBUM_NAME: "Best Of", PostFields.ALBUM_ARTISTS_NAMES_MULTIPART: []}
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_MP3, **data)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.artists.count() == 0

    def test_existing_then_ok(self) -> None:
        artist = self.model_fixture_factory.create_artist(name="Kopoe")

        data = {PostFields.ALBUM_NAME: "Best Of", PostFields.ALBUM_ARTISTS_NAMES_MULTIPART: [artist.name]}
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_MP3, **data)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.album
        artists_list: list[Artist] = list(self.saved_object.album.album_artists.all())
        assert len(artists_list) == 1
        assert artists_list[0].uuid == artist.uuid

    def test_not_existing_then_ok(self) -> None:
        artist_name = "hoho"
        data = {PostFields.ALBUM_NAME: "Best Of", PostFields.ALBUM_ARTISTS_NAMES_MULTIPART: artist_name}
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_MP3, **data)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.album
        artists_list: list[Artist] = list(self.saved_object.album.album_artists.all())
        assert len(artists_list) > 0
        assert artists_list[0].name == artist_name

    def test_multiple_existing_artists_then_ok(self) -> None:
        artist1 = self.model_fixture_factory.create_artist(name="Kopoe")
        artist2 = self.model_fixture_factory.create_artist(name="Steeve")

        data = {PostFields.ALBUM_NAME: "Best Of",
                PostFields.ALBUM_ARTISTS_NAMES_MULTIPART: [artist1.name, artist2.name]}
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_MP3, **data)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.album
        artists_list: list[Artist] = list(self.saved_object.album.album_artists.all())
        assert len(artists_list) == 2
        album_artists_uuids = [artist.uuid for artist in artists_list]
        assert artist1.uuid in album_artists_uuids
        assert artist2.uuid in album_artists_uuids

    def test_multiple_non_existing_artists_then_ok(self) -> None:
        artist1_name = "NewArtist1"
        artist2_name = "NewArtist2"
        artist3_name = "NewArtist3"

        data = {PostFields.ALBUM_NAME: "Best Of",
                PostFields.ALBUM_ARTISTS_NAMES_MULTIPART: [artist1_name, artist2_name, artist3_name]}
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_MP3, **data)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.album
        artists_list: list[Artist] = list(self.saved_object.album.album_artists.all())
        artists_names = [artist.name for artist in artists_list]
        assert len(artists_list) == 3
        assert artist1_name in artists_names
        assert artist2_name in artists_names
        assert artist3_name in artists_names

    def test_mix_existing_and_non_existing_artists_then_ok(self) -> None:
        existing_artist = self.model_fixture_factory.create_artist(name="Kopoe")
        new_artist1_name = "NewArtist1"
        new_artist2_name = "NewArtist2"

        data = {PostFields.ALBUM_NAME: "Best Of",
                PostFields.ALBUM_ARTISTS_NAMES_MULTIPART: [existing_artist.name, new_artist1_name, new_artist2_name]}
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_MP3, **data)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.album
        artists_list: list[Artist] = list(self.saved_object.album.album_artists.all())
        assert len(artists_list) == 3
        artists_uuids = [artist.uuid for artist in artists_list]
        assert existing_artist.uuid in artists_uuids
        artists_names = [artist.name for artist in artists_list]
        assert new_artist1_name in artists_names
        assert new_artist2_name in artists_names

    def test_multiple_with_one_too_large_then_400_bad_request(self) -> None:
        valid_artist = "ValidArtist"
        too_long_artist = "a" * (settings.ARTIST_NAME_LEN_MAX + 1)

        data = {PostFields.ALBUM_NAME: "Best Of",
                PostFields.ALBUM_ARTISTS_NAMES_MULTIPART: [valid_artist, too_long_artist]}
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_MP3, **data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error['field'] == to_camel_case(PostFields.ALBUM_ARTISTS_NAMES_MULTIPART)
        assert error['code'] == FieldValidationErrorCode.STRING_TOO_LONG

    def test_multiple_with_one_empty_then_400_bad_request(self) -> None:
        data = {PostFields.ALBUM_NAME: "Best Of", PostFields.ALBUM_ARTISTS_NAMES_MULTIPART: ['', 'Muse']}
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_MP3, **data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error['field'] == to_camel_case(PostFields.ALBUM_ARTISTS_NAMES_MULTIPART)
        assert error['code'] == FieldValidationErrorCode.LIST_VALUE_EMPTY

    def test_comma_separated_then_only_one_value(self) -> None:
        artist_name = "mat, muse"
        data = {PostFields.ALBUM_NAME: "Best Of", PostFields.ALBUM_ARTISTS_NAMES_MULTIPART: [artist_name]}
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_MP3, **data)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.album
        artists_list: list[Artist] = list(self.saved_object.album.album_artists.all())
        assert len(artists_list) == 1
        assert artists_list[0].name == artist_name

    def test_duplicate_values_then_400_bad_request(self) -> None:
        data = {PostFields.ALBUM_NAME: "Best Of", PostFields.ALBUM_ARTISTS_NAMES_MULTIPART: ['Muse', 'Muse']}
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_MP3, **data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error['field'] == to_camel_case(PostFields.ALBUM_ARTISTS_NAMES_MULTIPART)
        assert error['code'] == FieldValidationErrorCode.LIST_VALUE_DUPLICATE
