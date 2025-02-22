
from rest_framework import status

from bodzify_api.serializer.model.lib_track.input.extract.Fields import Fields as LibTrackFields
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase
from bodzify_api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.view.error.ErrorResponseFields import ErrorResponseFields


class TestMultipartDuplicateFields(LibTrackTestCase):

    def test_duplicate_fields_on_multipart_post_then_400(self):
        data = {
            LibTrackFields.TITLE: ['Jo', 'steeve']  # Multiple values will be converted to separate form fields
        }
        response = self._post_lib_track_with_generic_sample_no_tags(**data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error[ErrorResponseFields.FieldErrors.FIELD] == LibTrackFields.TITLE

        # The raised error will be invalid format as the duplicated data in multipart form data will be converted to
        # a list
        assert error[ErrorResponseFields.FieldErrors.CODE] == FieldValidationErrorCode.INVALID_FORMAT.value

    def test_duplicate_fields_on_multipart_put_then_400(self):
        lib_track = self.model_fixture_factory.create_lib_track_with_file(title="Hey Ho")

        data = {
            LibTrackFields.TITLE: ['Jo', 'steeve']  # Multiple values will be converted to separate form fields
        }
        response = self._put_lib_track(lib_track.uuid, **data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        self._set_bad_request_result(response)
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error[ErrorResponseFields.FieldErrors.FIELD] == LibTrackFields.TITLE
        assert error[ErrorResponseFields.FieldErrors.CODE] == FieldValidationErrorCode.INVALID_FORMAT.value

    def test_duplicate_fields_on_multipart_patch_then_400(self):
        # PATCH is not supported
        pass

    def test_list_fields_allowed_duplicates_on_multipart_then_ok(self):
        # Test array fields that allow duplicate values
        data = {
            LibTrackFields.TITLE: 'test',
            LibTrackFields.ARTISTS_NAMES_ARRAY: ['artist1', 'artist2', 'artist3']
        }
        response = self._post_lib_track_with_generic_sample_no_tags(**data)

        # This should succeed as duplicate values in arrays are allowed
        assert response.status_code == status.HTTP_201_CREATED
