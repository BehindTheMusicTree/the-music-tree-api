from rest_framework import status

from api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from api.serializer.model.track.input.post.Fields import Fields as TrackFields
from api.test.integration.view.track.TrackTestCase import Track


class TestMultipartDuplicateFields(Track):

    def test_duplicate_fields_on_multipart_post_then_400_bad_request(self):
        data = {
            TrackFields.TITLE: ['Jo', 'steeve']  # Multiple values will be converted to separate form fields
        }
        response = self._post_track(**data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error['field'] == TrackFields.TITLE

        assert error['code'] == FieldValidationErrorCode.DUPLICATE

    def test_duplicate_fields_on_multipart_put_then_400_bad_request(self):
        track = self.model_fixture_factory.create_track_with_file(title="Hey Ho")

        data = {
            TrackFields.TITLE: ['Jo', 'steeve']  # Multiple values will be converted to separate form fields
        }
        response = self._put_track(uuid=track.uuid, **data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        self._set_error_response_result_if_failure(response)
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error['field'] == TrackFields.TITLE
        assert error['code'] == FieldValidationErrorCode.DUPLICATE

    def test_duplicate_fields_on_multipart_patch_then_400_bad_request(self):
        # PATCH is not supported yet by the app
        pass

    def test_list_fields_allowed_duplicates_on_multipart_then_ok(self):
        data = {
            TrackFields.TITLE: 'test',
            TrackFields.ARTISTS_NAMES_MULTIPART: ['artist1', 'artist2', 'artist3']
        }
        response = self._post_track(**data)

        assert response.status_code == status.HTTP_201_CREATED
