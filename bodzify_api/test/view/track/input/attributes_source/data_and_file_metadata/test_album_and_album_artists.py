#!/usr/bin/env python

from rest_framework import status

from bodzify_api import settings
from bodzify_api.test.view.track.TrackTestCase import TrackTestCase
from bodzify_api.serializer.track.input.endpoint.post import Fields as PostFields


class TestCase(TrackTestCase):

    def test_album_in_both_then_take_from_data(self):
        data_album_name = "ko"
        data_dict = {PostFields.ALBUM_NAME: data_album_name}
        response = self.post_lib_track_with_generic_sample_tags_max_length_of_a(data_dict=data_dict)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.album is not None
        assert self.saved_lib_track.album.name == data_album_name

    def test_only_album_in_data_and_only_album_artists_in_metadata_then_take_both(self):
        data_album_name = "oiuhgoi"
        data_dict = {PostFields.ALBUM_NAME: data_album_name}
        response = self.post_lib_track_with_generic_sample_tag_album_artists_koko_without_album(data_dict=data_dict)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.album is not None
        assert self.saved_lib_track.album.name == data_album_name
        assert self.saved_lib_track.album.album_artists.first().name == "koko"

    def test_only_album_in_data_and_album_and_album_artists_max_a_in_metadata_then_take_album_from_data_and_album_artists_from_metadata(self):
        data_album_name = "oiuhgoi"
        data_dict = {PostFields.ALBUM_NAME: data_album_name}
        response = self.post_lib_track_with_generic_sample_tags_max_length_of_a(data_dict=data_dict)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.album is not None
        assert self.saved_lib_track.album.name == data_album_name
        assert self.saved_lib_track.album.album_artists.first().name == 'a' * settings.ARTIST_NAME_LEN_MAX

    def test_album_and_album_artists_in_data_and_only_album_in_metadata_then_take_from_data(self):
        data_album_name = "non"
        data_album_artists_str = "oiuhgoi efe"
        data_dict = {
            PostFields.ALBUM_NAME: data_album_name,
            PostFields.ALBUM_ARTISTS_NAMES_STR: data_album_artists_str
        }
        response = self.post_lib_track_with_generic_sample_tag_album_koko_without_album_artists(data_dict=data_dict)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.album is not None
        assert self.saved_lib_track.album.name == data_album_name
        assert self.saved_lib_track.album.album_artists.first().name == data_album_artists_str

    def test_album_and_album_artists_in_data_and_metadata_then_take_from_data(self):
        data_album_name = "non"
        data_album_artists_str = "oiuhgoi efe"
        data_dict = {
            PostFields.ALBUM_NAME: data_album_name,
            PostFields.ALBUM_ARTISTS_NAMES_STR: data_album_artists_str
        }
        response = self.post_lib_track_with_generic_sample_tags_max_length_of_a(data_dict=data_dict)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.album is not None
        assert self.saved_lib_track.album.name == data_album_name
        assert self.saved_lib_track.album.album_artists.first().name == data_album_artists_str
