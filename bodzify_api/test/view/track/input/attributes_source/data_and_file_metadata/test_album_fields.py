from rest_framework import status

from bodzify_api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.serializer.model.lib_track.input.post.Fields import Fields as PostFields
from bodzify_api.test.utils.lib_track.LibTrackTestFilename import LibTrackTestFilename
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase
from bodzify_api.utils.data_transformer import to_camel_case


class TestCase(LibTrackTestCase):

    def test_album_in_both_then_take_from_data(self):
        data_album_name = "Best of"
        data_dict = {PostFields.ALBUM_NAME: data_album_name, PostFields.ALBUM_ARTISTS_NAMES_ARRAY: ["Muse"]}
        response = self._post_lib_track(LibTrackTestFilename.METADATA_LONG_A_ID3V1_SMALL_MP3, **data_dict)

        assert response.status_code == status.HTTP_201_CREATED
        album = self.saved_object.album
        assert album
        assert album.name == data_album_name

    def test_album_and_album_artists_in_data_and_only_album_in_metadata_then_take_from_data(self):
        data_album_name = "Best of"
        data_artist_name = "Muse"
        data = {PostFields.ALBUM_NAME: data_album_name, PostFields.ALBUM_ARTISTS_NAMES_ARRAY: [data_artist_name]}
        response = self._post_lib_track(LibTrackTestFilename.ALBUM_KOKO_ID3V2_MP3, **data)

        assert response.status_code == status.HTTP_201_CREATED
        album = self.saved_object.album
        assert album
        assert album.name == data_album_name
        album_artist = album.album_artists.first()
        assert album_artist
        assert album_artist.name == data_artist_name

    def test_album_and_album_artists_in_data_and_metadata_then_take_from_data(self):
        data_album_name = "non"
        data_album_artists_str = "oiuhgoi efe"
        data_dict = {
            PostFields.ALBUM_NAME: data_album_name,
            PostFields.ALBUM_ARTISTS_NAMES_ARRAY: data_album_artists_str
        }
        response = self._post_lib_track(LibTrackTestFilename.METADATA_LONG_A_ID3V2_SMALL_MP3, **data_dict)

        assert response.status_code == status.HTTP_201_CREATED
        album = self.saved_object.album
        assert album
        assert album.name == data_album_name
        album_artist = album.album_artists.first()
        assert album_artist
        assert album_artist.name == data_album_artists_str

    def test_only_album_artists_in_data_and_album_in_metadata_then_400(self):
        data_album_artists_name = "Muse"
        data = {PostFields.ALBUM_ARTISTS_NAMES_ARRAY: [data_album_artists_name]}
        response = self._post_lib_track(LibTrackTestFilename.METADATA_LONG_A_ID3V2_SMALL_MP3, **data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        error = self.bad_request_result_field_errors[0]
        assert error["field"] == to_camel_case(PostFields.ALBUM_NAME)
        assert error["code"] == FieldValidationErrorCode.DEPENDENCY_MISSING

    def test_only_album_name_in_data_and_album_artists_in_metadata_then_400(self):
        data_album_name = "Best of"
        data = {PostFields.ALBUM_NAME: data_album_name}
        response = self._post_lib_track(LibTrackTestFilename.METADATA_LONG_A_ID3V1_SMALL_MP3, **data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        error = self.bad_request_result_field_errors[0]
        assert error["field"] == to_camel_case(PostFields.ALBUM_ARTISTS_NAMES_ARRAY)
        assert error["code"] == FieldValidationErrorCode.DEPENDENCY_MISSING
