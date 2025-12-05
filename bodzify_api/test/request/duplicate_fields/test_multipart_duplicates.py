from rest_framework import status

from bodzify_api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.serializer.model.uploaded_track.input.post.Fields import Fields as UploadedTrackFields
from bodzify_api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename
from bodzify_api.test.view.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase


class TestMultipartDuplicateFields(UploadedTrackTestCase):

    def test_duplicate_fields_on_multipart_post_then_400_bad_request(self):
        data = {
            UploadedTrackFields.TITLE: ['Jo', 'steeve']  # Multiple values will be converted to separate form fields
        }
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_MP3, **data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error['field'] == UploadedTrackFields.TITLE

        assert error['code'] == FieldValidationErrorCode.DUPLICATE

    def test_duplicate_fields_on_multipart_put_then_400_bad_request(self):
        uploaded_track = self.model_fixture_factory.create_uploaded_track_with_file(title="Hey Ho")

        data = {
            UploadedTrackFields.TITLE: ['Jo', 'steeve']  # Multiple values will be converted to separate form fields
        }
        response = self._put_uploaded_track(uuid=uploaded_track.uuid, **data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        self._set_error_response_result_if_failure(response)
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error['field'] == UploadedTrackFields.TITLE
        assert error['code'] == FieldValidationErrorCode.DUPLICATE

    def test_duplicate_fields_on_multipart_patch_then_400_bad_request(self):
        # PATCH is not supported yet by the app
        pass

    def test_list_fields_allowed_duplicates_on_multipart_then_ok(self):
        data = {
            UploadedTrackFields.TITLE: 'test',
            UploadedTrackFields.ARTISTS_NAMES_MULTIPART: ['artist1', 'artist2', 'artist3']
        }
        response = self._post_uploaded_track(UploadedTrackTestFilename.METADATA_NONE_MP3, **data)

        assert response.status_code == status.HTTP_201_CREATED
