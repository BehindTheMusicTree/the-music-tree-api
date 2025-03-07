from rest_framework import status

from bodzify_api.serializer.model.lib_track.input.post.Fields import Fields as PostFields
from bodzify_api.test.utils.lib_track.TestLibTrackFilename import TestLibTrackFilename
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase):

    def test_album_in_both_then_take_from_data(self):
        data_album_name = "ko"
        data_dict = {PostFields.ALBUM_NAME: data_album_name}
        response = self._post_lib_track(TestLibTrackFilename.METADATA_LONG_A_ID3V1_SMALL_MP3, **data_dict)

        assert response.status_code == status.HTTP_201_CREATED
        album = self.saved_object.album
        assert album
        assert album.name == data_album_name

    def test_album_and_album_artists_in_data_and_only_album_in_metadata_then_take_from_data(self):
        data_album_name = "non"
        data_album_artists_str = "oiuhgoi efe"
        data_dict = {
            PostFields.ALBUM_NAME: data_album_name,
            PostFields.ALBUM_ARTISTS_NAMES_ARRAY: data_album_artists_str
        }
        response = self._post_lib_track(TestLibTrackFilename.ALBUM_KOKO_ID3V2_MP3, **data_dict)

        assert response.status_code == status.HTTP_201_CREATED
        album = self.saved_object.album
        assert album
        assert album.name == data_album_name
        album_artist = album.album_artists.first()
        assert album_artist
        assert album_artist.name == data_album_artists_str

    def test_album_and_album_artists_in_data_and_metadata_then_take_from_data(self):
        data_album_name = "non"
        data_album_artists_str = "oiuhgoi efe"
        data_dict = {
            PostFields.ALBUM_NAME: data_album_name,
            PostFields.ALBUM_ARTISTS_NAMES_ARRAY: data_album_artists_str
        }
        response = self._post_lib_track(TestLibTrackFilename.METADATA_LONG_A_ID3V2_SMALL_MP3, **data_dict)

        assert response.status_code == status.HTTP_201_CREATED
        album = self.saved_object.album
        assert album
        assert album.name == data_album_name
        album_artist = album.album_artists.first()
        assert album_artist
        assert album_artist.name == data_album_artists_str
