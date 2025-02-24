from rest_framework import status

from bodzify_api import settings
from bodzify_api.serializer.model.lib_track.input.post.Fields import Fields as PostFields
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase):

    def test_album_in_both_then_take_from_data(self):
        data_album_name = "ko"
        data_ = {PostFields.ALBUM_NAME: data_album_name}
        response = self._post_lib_track_with_generic_sample_tags_max_length_of_a(**data_)

        assert response.status_code == status.HTTP_201_CREATED
        album = self.saved_object.album
        assert album
        assert album.name == data_album_name

    def test_only_album_in_data_and_only_album_artists_in_metadata_then_take_both(self):
        data_album_name = "Best of"
        data_ = {PostFields.ALBUM_NAME: data_album_name}
        response = self._post_lib_track_with_generic_sample_tag_album_artists_koko_without_album(**data_)

        assert response.status_code == status.HTTP_201_CREATED
        album = self.saved_object.album
        assert album
        assert album.name == data_album_name
        album_artist = album.album_artists.first()
        assert album_artist
        assert album_artist.name == "koko"

    def test_only_album_in_data_and_album_and_album_artists_max_a_in_metadata_then_take_album_from_data_and_album_artists_from_metadata(self):
        data_album_name = "oiuhgoi"
        data_ = {PostFields.ALBUM_NAME: data_album_name}
        response = self._post_lib_track_with_generic_sample_tags_max_length_of_a(**data_)

        assert response.status_code == status.HTTP_201_CREATED
        album = self.saved_object.album
        assert album
        assert album.name == data_album_name
        album_artist = album.album_artists.first()
        assert album_artist
        assert album_artist.name == 'a' * settings.ARTIST_NAME_LEN_MAX

    def test_album_and_album_artists_in_data_and_only_album_in_metadata_then_take_from_data(self):
        data_album_name = "non"
        data_album_artists_str = "oiuhgoi efe"
        data_ = {
            PostFields.ALBUM_NAME: data_album_name,
            PostFields.ALBUM_ARTISTS_NAMES_ARRAY: data_album_artists_str
        }
        response = self._post_lib_track_with_generic_sample_tag_album_koko_without_album_artists(**data_)

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
        data_ = {PostFields.ALBUM_NAME: data_album_name,
                 PostFields.ALBUM_ARTISTS_NAMES_ARRAY: data_album_artists_str}
        response = self._post_lib_track_with_generic_sample_tags_max_length_of_a(**data_)

        assert response.status_code == status.HTTP_201_CREATED
        album = self.saved_object.album
        assert album
        assert album.name == data_album_name
        album_artist = album.album_artists.first()
        assert album_artist
        assert album_artist.name == data_album_artists_str
