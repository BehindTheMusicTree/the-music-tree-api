from rest_framework import status

from bodzify_api import settings
from bodzify_api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.serializer.model.uploaded_track.input.post.Fields import Fields as PostFields
from bodzify_api.test.utils.field.body_data.type.NullableCharBodyDataTestCase import NullableCharBodyDataTestCase
from bodzify_api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename
from bodzify_api.test.view.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase
from bodzify_api.utils.data_transformer import to_camel_case


class TestCase(NullableCharBodyDataTestCase, UploadedTrackTestCase):

    def test_largest_then_ok(self):
        genre_name = "a" * settings.CRITERIA_NAME_LEN_MAX
        response = self._post_uploaded_track(
            UploadedTrackTestFilename.METADATA_NONE_MP3, **{PostFields.GENRE: genre_name})

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.genre
        assert self.saved_object.genre.name == genre_name

    def test_too_large_then_400_bad_request(self):
        genre_name = "a" * (settings.CRITERIA_NAME_LEN_MAX + 1)
        response = self._post_uploaded_track(
            UploadedTrackTestFilename.METADATA_NONE_MP3, **{PostFields.GENRE: genre_name})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error['field'] == to_camel_case(PostFields.GENRE)
        assert error['code'] == FieldValidationErrorCode.STRING_TOO_LONG

    def test_empty_then_ok(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_MP3, **{PostFields.GENRE: ''})

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.genre == None

    def test_existing_then_ok(self):
        genre_name = "Kopoe"
        self.model_fixture_factory.create_genre(name=genre_name)

        response = self._post_uploaded_track(
            UploadedTrackTestFilename.METADATA_NONE_MP3, **{PostFields.GENRE: genre_name})

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.genre
        assert self.saved_object.genre.name == genre_name

    def test_not_existing(self):
        genre_name = "hoho"
        response = self._post_uploaded_track(
            UploadedTrackTestFilename.METADATA_NONE_MP3, **{PostFields.GENRE: genre_name})

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.genre
        assert self.saved_object.genre.name == genre_name

    def test_new_so_parent_none(self):
        genre_name = "Rock"
        response = self._post_uploaded_track(
            UploadedTrackTestFilename.METADATA_NONE_MP3, **{PostFields.GENRE: genre_name})

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.genre
        assert self.saved_object.genre.parent == None

    def test_multi_value_then_400_bad_request(self):
        response = self._post_uploaded_track(
            UploadedTrackTestFilename.METADATA_NONE_MP3, **{PostFields.GENRE: ['a', 'b']})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error['field'] == to_camel_case(PostFields.GENRE)
        assert error['code'] == FieldValidationErrorCode.DUPLICATE  # because multipart
