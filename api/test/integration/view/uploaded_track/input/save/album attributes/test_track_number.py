from rest_framework import status

from api import settings
from api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from api.serializer.model.uploaded_track.input.post.Fields import Fields as PostFields
from api.test.utils.field.body_data.type.NullablePositiveIntBodyDataTestCase import NullablePositiveIntBodyDataTestCase
from api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename
from api.test.integration.view.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase
from api.utils.data_transformer import to_camel_case


class TestCase(UploadedTrackTestCase, NullablePositiveIntBodyDataTestCase):

    def test_empty_then_none(self):
        response = self._post_uploaded_track(
            UploadedTrackTestFilename.METADATA_NONE_MP3, **{PostFields.TRACK_NUMBER: None})

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.track_number == None

    def test_empty_string_then_none(self):
        response = self._post_uploaded_track(
            UploadedTrackTestFilename.METADATA_NONE_MP3, **{PostFields.TRACK_NUMBER: ''})

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.track_number == None

    def test_string_castable_then_ok(self):
        response = self._post_uploaded_track(
            UploadedTrackTestFilename.METADATA_NONE_MP3, **
            {PostFields.ALBUM_NAME: 'album', PostFields.TRACK_NUMBER: '5'})

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.track_number == 5

    def test_string_not_castable_then_400_bad_request(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_MP3,
                                             **{PostFields.ALBUM_NAME: 'album', PostFields.TRACK_NUMBER: 'five'})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error['field'] == to_camel_case(PostFields.TRACK_NUMBER)
        assert error['code'] == FieldValidationErrorCode.FORMAT_INVALID

    def string_castable_then_ok(self):
        response = self._post_uploaded_track(
            UploadedTrackTestFilename.METADATA_NONE_MP3, **{PostFields.TRACK_NUMBER: '5'})

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.track_number == 5

    def test_zero_then_400_bad_request(self):
        response = self._post_uploaded_track(
            UploadedTrackTestFilename.METADATA_NONE_MP3, **{PostFields.TRACK_NUMBER: 0})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error['field'] == to_camel_case(PostFields.TRACK_NUMBER)
        assert error['code'] == FieldValidationErrorCode.TRACK_NUMBER_TOO_SMALL

    def test_one_then_ok(self):
        track_number = 1

        response = self._post_uploaded_track(
            UploadedTrackTestFilename.METADATA_NONE_MP3, **
            {PostFields.ALBUM_NAME: 'album', PostFields.TRACK_NUMBER: track_number})

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.track_number == track_number

    def test_largest_then_ok(self):
        track_number = settings.UPLOADED_TRACK_TRACK_NUMBER_MAX
        response = self._post_uploaded_track(
            UploadedTrackTestFilename.METADATA_NONE_MP3, **
            {PostFields.ALBUM_NAME: 'album', PostFields.TRACK_NUMBER: track_number})

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.track_number == track_number

    def test_too_large_then_400_bad_request(self):
        response = self._post_uploaded_track(
            UploadedTrackTestFilename.METADATA_NONE_MP3,
            **{PostFields.ALBUM_NAME: 'album', PostFields.TRACK_NUMBER: settings.UPLOADED_TRACK_TRACK_NUMBER_MAX + 1})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error['field'] == to_camel_case(PostFields.TRACK_NUMBER)
        assert error['code'] == FieldValidationErrorCode.TRACK_NUMBER_TOO_LARGE

    def test_negative_then_400_bad_request(self):
        response = self._post_uploaded_track(
            UploadedTrackTestFilename.METADATA_NONE_MP3, **{PostFields.TRACK_NUMBER: -1})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error['field'] == to_camel_case(PostFields.TRACK_NUMBER)
        assert error['code'] == FieldValidationErrorCode.TRACK_NUMBER_TOO_SMALL

    def test_float_then_400_bad_request(self):
        response = self._post_uploaded_track(
            UploadedTrackTestFilename.METADATA_NONE_MP3, **{PostFields.TRACK_NUMBER: 5.5})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error['field'] == to_camel_case(PostFields.TRACK_NUMBER)
        assert error['code'] == FieldValidationErrorCode.FORMAT_INVALID

    def test_multi_value_then_400_bad_request(self):
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_MP3,
                                             **{PostFields.TRACK_NUMBER: [1, 2]})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error['field'] == to_camel_case(PostFields.TRACK_NUMBER)
        assert error['code'] == FieldValidationErrorCode.DUPLICATE
