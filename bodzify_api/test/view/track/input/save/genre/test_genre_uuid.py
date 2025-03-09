from rest_framework import status

from bodzify_api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.serializer.model.lib_track.input.post.Fields import Fields as PostFields
from bodzify_api.test.utils.field.body_data.type.ForeignKeyBodyDataTestCase import ForeignKeyBodyDataTestCase
from bodzify_api.test.utils.lib_track.TestLibTrackFilename import TestLibTrackFilename
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


class TestCase(ForeignKeyBodyDataTestCase, LibTrackTestCase):

    def test_non_existing_then_400(self):
        non_exisintg_uuid = "00000000-0000-0000-0000-000000000000"
        response = self._post_lib_track(TestLibTrackFilename.METADATA_NONE_MP3, **{PostFields.GENRE: non_exisintg_uuid})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error['field'] == PostFields.GENRE
        assert error['code'] == FieldValidationErrorCode.REFERENCE_INVALID

    def test_existing_then_ok(self):
        genre = self.model_fixture_factory.create_genre(name="rock")
        response = self._post_lib_track(TestLibTrackFilename.METADATA_NONE_MP3, **{PostFields.GENRE: genre.uuid})

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object
        assert self.saved_object.genre == genre

    def test_empty_then_none(self):
        response = self._post_lib_track(TestLibTrackFilename.METADATA_NONE_MP3, **{PostFields.GENRE: ""})

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.genre is None

    def test_multi_value_then_400(self):
        genre = self.model_fixture_factory.create_genre(name="rock")

        response = self._post_lib_track(
            TestLibTrackFilename.METADATA_NONE_MP3, **{PostFields.GENRE: [genre.uuid, genre.uuid]})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error['field'] == PostFields.GENRE
        assert error['code'] == FieldValidationErrorCode.FORMAT_INVALID

    def test_invalid_uuid_then_400(self):
        invalid_uuid = "036aa19e-d5ae-425a-93f2-125ccd145a15"
        response = self._post_lib_track(TestLibTrackFilename.METADATA_NONE_MP3, **{PostFields.GENRE: invalid_uuid})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error['field'] == PostFields.GENRE
        assert error['code'] == FieldValidationErrorCode.REFERENCE_INVALID
