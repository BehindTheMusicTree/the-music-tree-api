#!/usr/bin/env python

from requests import post
from bodzify_api.serializer.track.input.schema.endpoint.LibTrackPostSerializer import FIELDS as POST_FIELDS
from rest_framework import status

from bodzify_api.test.view.track.TrackTestCase import TrackTestCase


class FieldFromDataTestCase(TrackTestCase):
    post_field_key = None

    def setUp(self, methods_names_to_implement: list[str] | None = None):
        class_methods_names_to_implement = ['test_value_then_ok']
        if methods_names_to_implement:
            class_methods_names_to_implement += methods_names_to_implement
        return super().setUp(class_methods_names_to_implement)


class FieldStrFromDataTestCase(FieldFromDataTestCase):

    def test_multiple_values_then_error(self):
        if not self.post_field_key:
            raise NotImplementedError("post_field_key is not set")
        data = {
            self.post_field_key: ["value", "value2"],
        }
        response = self.post_lib_track_with_generic_sample_no_tags(data_dict=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST  # type: ignore


class FieldIntFromDataTestCase(FieldFromDataTestCase):

    def test_field_twice_then_error(self):
        if not self.post_field_key:
            raise NotImplementedError("post_field_key is not set")
        data = {
            self.post_field_key: [1, 2],
        }
        response = self.post_lib_track_with_generic_sample_no_tags(data_dict=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST  # type: ignore


class NullableStrFieldFromDataTestCase(FieldStrFromDataTestCase):

    def setUp(self, methods_names_to_implement: list[str] | None = None):
        class_methods_names_to_implement = ['test_empty_then_none']
        if methods_names_to_implement:
            class_methods_names_to_implement += methods_names_to_implement
        return super().setUp(class_methods_names_to_implement)


class NonNullableStrFieldFromDataTestCase(FieldStrFromDataTestCase):

    def test_empty_then_error(self):
        data = {self.post_field_key: ""}
        response = self.post_lib_track_with_generic_sample_no_tags(extension='mp3', data_dict=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST  # type: ignore


class TitleTestCase(NonNullableStrFieldFromDataTestCase):
    post_field_key = POST_FIELDS.TITLE

    def test_value_then_ok(self):
        value = 'fr'
        data = {POST_FIELDS.TITLE: value}
        response = self.post_lib_track_with_generic_sample_no_tags(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED  # type: ignore
        assert self.saved_lib_track.title == value


class AlbumTestCase(NullableStrFieldFromDataTestCase):
    post_field_key = POST_FIELDS.ALBUM_NAME

    def test_value_then_ok(self):
        value = 'fofof'
        data = {POST_FIELDS.ALBUM_NAME: value}
        response = self.post_lib_track_with_generic_sample_no_tags(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED  # type: ignore
        assert self.saved_lib_track.album.name == value  # type: ignore

    def test_empty_then_none(self):
        data = {POST_FIELDS.ALBUM_NAME: ""}
        response = self.post_lib_track_with_generic_sample_1_star(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED  # type: ignore
        assert self.saved_lib_track.album == None


class AlbumArtistsTestCase(NullableStrFieldFromDataTestCase):
    post_field_key = POST_FIELDS.ALBUM_ARTISTS_NAMES_STRING

    def test_value_then_ok(self):
        value = 'astititit'
        data = {
            POST_FIELDS.ALBUM_NAME: 'albumito',
            POST_FIELDS.ALBUM_ARTISTS_NAMES_STRING: value
        }
        response = self.post_lib_track_with_generic_sample_no_tags(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED  # type: ignore
        assert self.saved_lib_track.album.album_artists.all()[0].name == value  # type: ignore

    def test_empty_then_none(self):
        data = {
            POST_FIELDS.ALBUM_NAME: "alnumito",
            POST_FIELDS.ALBUM_ARTISTS_NAMES_STRING: ""
        }
        response = self.post_lib_track_with_generic_sample_1_star(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED  # type: ignore
        assert self.saved_lib_track.album.album_artists.count() == 0  # type: ignore


class RatingTestCase(FieldIntFromDataTestCase):
    post_field_key = POST_FIELDS.RATING

    def test_value_then_ok(self):
        value = 1
        data = {POST_FIELDS.RATING: value}
        response = self.post_lib_track_with_generic_sample_no_tags(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED  # type: ignore
        assert self.saved_lib_track.rating == value

    def test_empty_then_none(self):
        data = {POST_FIELDS.RATING: ""}
        response = self.post_lib_track_with_generic_sample_1_star(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED  # type: ignore
        assert self.saved_lib_track.rating == None


class LanguageTestCase(NullableStrFieldFromDataTestCase):
    post_field_key = POST_FIELDS.LANGUAGE

    def test_value_then_ok(self):
        value = 'fr'
        data = {POST_FIELDS.LANGUAGE: value}
        response = self.post_lib_track_with_generic_sample_no_tags(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED  # type: ignore
        assert self.saved_lib_track.language == value

    def test_empty_then_none(self):
        data = {POST_FIELDS.LANGUAGE: ""}
        response = self.post_lib_track_with_generic_sample_1_star(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED  # type: ignore
        assert self.saved_lib_track.language == None


class GenreTestCase(NullableStrFieldFromDataTestCase):
    post_field_key = POST_FIELDS.GENRE_NAME

    def test_value_then_ok(self):
        value = 'rovk'
        data = {POST_FIELDS.GENRE_NAME: value}
        response = self.post_lib_track_with_generic_sample_no_tags(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED  # type: ignore
        assert self.saved_lib_track.genre.name == value  # type: ignore

    def test_empty_then_none(self):
        data = {POST_FIELDS.GENRE_NAME: ""}
        response = self.post_lib_track_with_generic_sample_1_star(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED  # type: ignore
        assert self.saved_lib_track.genre == None


class ArtistTestCase(NullableStrFieldFromDataTestCase):
    post_field_key = POST_FIELDS.ARTIST_NAME

    def test_value_then_ok(self):
        value = 'rovk'
        data = {POST_FIELDS.ARTIST_NAME: value}
        response = self.post_lib_track_with_generic_sample_no_tags(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED  # type: ignore
        assert self.saved_lib_track.artist.name == value  # type: ignore

    def test_empty_then_none(self):
        data = {POST_FIELDS.ARTIST_NAME: ""}
        response = self.post_lib_track_with_generic_sample_1_star(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED  # type: ignore
        assert self.saved_lib_track.artist == None
