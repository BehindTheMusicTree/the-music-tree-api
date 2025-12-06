from rest_framework import status

from bodzify_api import settings
from bodzify_api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.serializer.model.uploaded_track.input.post.Fields import Fields as PostFields
from bodzify_api.test.utils.field.body_data.type.NullableCharBodyDataTestCase import NullableCharBodyDataTestCase
from bodzify_api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename
from bodzify_api.test.integration.view.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase
from bodzify_api.utils.data_transformer import to_camel_case


class TestCase(UploadedTrackTestCase, NullableCharBodyDataTestCase):

    def test_largest_then_ok(self):
        album_name = "a" * settings.ALBUM_NAME_LEN_MAX
        data = {PostFields.ALBUM_NAME: album_name, PostFields.ALBUM_ARTISTS_NAMES_MULTIPART: ["muse"]}
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_MP3, **data)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.album
        assert self.saved_object.album.name == album_name

    def test_too_large_then_400_bad_request(self):
        album_name = "a" * (settings.ALBUM_NAME_LEN_MAX + 1)
        data = {PostFields.ALBUM_NAME: album_name, PostFields.ARTISTS_NAMES_MULTIPART: ["muse"]}
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_MP3, **data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error['field'] == to_camel_case(PostFields.ALBUM_NAME)
        assert error['code'] == FieldValidationErrorCode.STRING_TOO_LONG

    def test_empty_then_ok(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_MP3, **{PostFields.ALBUM_NAME: ''})

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.album == None

    def test_existing_then_ok(self):
        album_name = "Kopoe"
        album = self.model_fixture_factory.create_album(name=album_name)

        data = {PostFields.ALBUM_NAME: album_name, PostFields.ALBUM_ARTISTS_NAMES_MULTIPART: []}
        response = self._post_uploaded_track(
            test_uploaded_track_filename=UploadedTrackTestFilename.METADATA_NONE_MP3, **data)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.album
        assert self.saved_object.album.uuid == album.uuid

    def test_not_existing(self):
        album_name = "hoho"
        data = {PostFields.ALBUM_NAME: album_name, PostFields.ALBUM_ARTISTS_NAMES_MULTIPART: ["muse"]}
        response = self._post_uploaded_track(
            test_uploaded_track_filename=UploadedTrackTestFilename.METADATA_NONE_MP3, **data)

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.album
        assert self.saved_object.album.name == album_name

    def test_multi_value_then_400_bad_request(self):
        data = {PostFields.ALBUM_NAME: ['a', 'b'], PostFields.ARTISTS_NAMES_MULTIPART: ["muse"]}
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_MP3, **data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error['field'] == to_camel_case(PostFields.ALBUM_NAME)
        assert error['code'] == FieldValidationErrorCode.DUPLICATE
