

from typing import cast

from rest_framework import status

from bodzify_api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.model.album.Album import Album
from bodzify_api.model.artist.Artist import Artist
from bodzify_api.test.utils.lib_track.TestLibTrackFilename import TestLibTrackFilename
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase
from bodzify_api.serializer.model.lib_track.input.post.Fields import Fields as PostFields
from bodzify_api.utils.data_transformer import to_camel_case


class TestCase(LibTrackTestCase):
    def test_album_provided_but_album_artists_not_then_400(self):
        data = {PostFields.ALBUM_NAME: "Koko"}
        response = self._post_lib_track(
            title="Time", test_lib_track_filename=TestLibTrackFilename.SIZE_SMALL_0_01_MO_MP3, **data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        error = self.bad_request_result_field_errors[0]
        assert error["field"] == to_camel_case(PostFields.ALBUM_ARTISTS_NAMES_ARRAY)
        assert error["code"] == FieldValidationErrorCode.DEPENDENCY_MISSING

    def test_album_artists_provided_but_album_not_then_400(self):
        data = {PostFields.ALBUM_ARTISTS_NAMES_ARRAY: ["Koko"]}
        response = self._post_lib_track(
            title="time", test_lib_track_filename=TestLibTrackFilename.SIZE_SMALL_0_01_MO_MP3, **data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        error = self.bad_request_result_field_errors[0]
        assert error["field"] == PostFields.ALBUM_ARTISTS_NAMES_ARRAY
        assert error["code"] == FieldValidationErrorCode.DEPENDENCY_MISSING

    def test_album_artists_provided_but_album_empty_then_400(self):
        data = {PostFields.ALBUM_NAME: "", PostFields.ALBUM_ARTISTS_NAMES_ARRAY: ["Koko"]}
        response = self._post_lib_track(
            title="time", test_lib_track_filename=TestLibTrackFilename.SIZE_SMALL_0_01_MO_MP3, **data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        error = self.bad_request_result_field_errors[0]
        assert error["field"] == PostFields.ALBUM_ARTISTS_NAMES_ARRAY
        assert error["code"] == FieldValidationErrorCode.DEPENDENCY_MISSING

    def test_provided_with_existing_album_then_link_to_it(self):
        album_old = self.model_fixture_factory.create_album(name="Jojo")
        lib_track = self.model_fixture_factory.create_lib_track_with_file(title="koko", album=album_old)
        album_new = self.model_fixture_factory.create_album(name="koko")
        album_artist_new = self.model_fixture_factory.create_artist(name="James")

        data = {PostFields.ALBUM_NAME: album_new.name, PostFields.ALBUM_ARTISTS_NAMES_ARRAY: [album_artist_new.name]}
        response = self._post_lib_track(
            title="time", test_lib_track_filename=TestLibTrackFilename.SIZE_SMALL_0_01_MO_MP3, **data)

        assert response.status_code == status.HTTP_200_OK
        assert self.saved_object.album == album_new
        assert self.saved_object.album.album_artists.count() == 1
        assert self.saved_object.album.album_artists.first() == album_artist_new

    def test_provided_with_new_album_name_then_create_it(self):
        album_old = self.model_fixture_factory.create_album(name="Jojo")
        lib_track = self.model_fixture_factory.create_lib_track_with_file(title="koko", album=album_old)
        album_artist_new = self.model_fixture_factory.create_artist(name="James")

        data = {PostFields.ALBUM_NAME: "koko", PostFields.ALBUM_ARTISTS_NAMES_ARRAY: [album_artist_new.name]}
        response = self._post_lib_track(
            title="time", test_lib_track_filename=TestLibTrackFilename.SIZE_SMALL_0_01_MO_MP3, **data)

        assert response.status_code == status.HTTP_200_OK
        assert Album.objects.filter(user=self.test_user1, name="koko").exists()
        assert self.saved_object.album.name == "koko"
        assert self.saved_object.album.album_artists.count() == 1
        assert self.saved_object.album.album_artists.first() == album_artist_new

    def test_provided_with_existing_album_artist_then_link_to_it(self):
        album_artist = self.model_fixture_factory.create_artist(name="a-ha")
        album = self.model_fixture_factory.create_album(name="Jojo", album_artists=[album_artist])

        data = {PostFields.ALBUM_NAME: album.name, PostFields.ALBUM_ARTISTS_NAMES_ARRAY: [album_artist.name]}
        response = self._post_lib_track(
            title="time", test_lib_track_filename=TestLibTrackFilename.SIZE_SMALL_0_01_MO_MP3, **data)

        assert response.status_code == status.HTTP_200_OK
        assert self.saved_object.album == album
        assert self.saved_object.album.album_artists.count() == 1
        assert self.saved_object.album.album_artists.first() == album_artist

    def test_provided_with_new_album_artist_name_then_create_it(self):
        album_old = self.model_fixture_factory.create_album(name="Jojo")
        lib_track = self.model_fixture_factory.create_lib_track_with_file(title="koko", album=album_old)
        album_new = self.model_fixture_factory.create_album(name="koko")

        data = {PostFields.ALBUM_NAME: album_new.name, PostFields.ALBUM_ARTISTS_NAMES_ARRAY: ["James"]}
        response = self._post_lib_track(
            title="time", test_lib_track_filename=TestLibTrackFilename.SIZE_SMALL_0_01_MO_MP3, **data)

        assert response.status_code == status.HTTP_200_OK
        assert Artist.objects.filter(user=self.test_user1, name="James").exists()
        assert self.saved_object.album.album_artists.count() == 1
        assert cast(Artist, self.saved_object.album.album_artists.first()).name == "James"
