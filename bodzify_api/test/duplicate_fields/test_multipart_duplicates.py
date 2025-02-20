from django.core.files.uploadedfile import SimpleUploadedFile
from django.test.client import encode_multipart
from django.urls import reverse
from rest_framework import status

from bodzify_api.serializer.schema.model.lib_track.input.extract.Fields import Fields as LibTrackFields
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase
from bodzify_api.validator.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.view.error.ErrorResponseFields import ErrorResponseFields


class TestMultipartDuplicateFields(LibTrackTestCase):

    def test_duplicate_fields_on_multipart_post_then_400(self):
        data = {
            LibTrackFields.TITLE: 'test',
            LibTrackFields.TITLE: 'test2',
        }
        response = self._post_lib_track_with_generic_sample_no_tags(**data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        self._set_bad_request_result(response)
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error[ErrorResponseFields.FieldErrors.FIELD] == LibTrackFields.TITLE
        assert error[ErrorResponseFields.FieldErrors.CODE] == FieldValidationErrorCode.FIELD_DUPLICATE.value

    def test_duplicate_fields_on_multipart_put_then_400(self):
        lib_track = self.model_fixture_factory.create_lib_track_with_file(title="Hey Ho")

        response = self._put_lib_track(lib_track.uuid, **{LibTrackFields.TITLE: "test", LibTrackFields.TITLE: "test2"})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        self._set_bad_request_result(response)
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error[ErrorResponseFields.FieldErrors.FIELD] == LibTrackFields.TITLE
        assert error[ErrorResponseFields.FieldErrors.CODE] == FieldValidationErrorCode.FIELD_DUPLICATE.value

    def test_duplicate_fields_on_multipart_patch_then_400(self):
        # PATCH is not supported
        pass

    def test_list_fields_allowed_duplicates_on_multipart_then_ok(self):
        data = {
            LibTrackFields.TITLE: 'test',
            LibTrackFields.ARTISTS_NAMES_ARRAY: ['artist1', 'artist2', 'artist1'],
        }
        response = self._post_lib_track_with_generic_sample_no_tags(**data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
