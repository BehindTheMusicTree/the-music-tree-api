
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status

from bodzify_api.serializer.schema.model.criteria.input.Fields import Fields as CriteriaPostFields
from bodzify_api.test.view.criteria.GenreTestCase import GenreTestCase
from bodzify_api.validator.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.view.error.ErrorResponseFields import ErrorResponseFields


class TestCase(GenreTestCase):
    def setUp(self):
        super().setUp()
        # Create a test genre for PUT/PATCH operations
        response = self._post_genre(name="Test Genre")
        self._set_saved_object(response)

    def test_duplicate_fields_on_content_type_json_then_400(self):
        json_str = '{"name": "test", "name": "test2"}'
        response = self.client.post(
            reverse(self.list_endpoint),
            json_str.encode('utf-8'),
            content_type='application/json',
            HTTP_ACCEPT='application/json'
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        self._set_bad_request_result(response)
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error[ErrorResponseFields.FieldErrors.FIELD] == CriteriaPostFields.NAME_PUBLIC
        assert error[ErrorResponseFields.FieldErrors.CODE] == FieldValidationErrorCode.FIELD_DUPLICATE.value

    def test_duplicate_fields_on_multipart_then_400(self):
        """Test that duplicate non-list fields in multipart/form-data are detected"""
        test_file = SimpleUploadedFile("test.txt", b"test content")
        data = {
            'name': 'test',  # First occurrence
            'name': 'test2',  # Second occurrence - should be detected as duplicate
            'file': test_file
        }
        response = self.client.post(
            reverse(self.list_endpoint),
            data,
            HTTP_ACCEPT='application/json'
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        self._set_bad_request_result(response)
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error[ErrorResponseFields.FieldErrors.FIELD] == CriteriaPostFields.NAME_PUBLIC
        assert error[ErrorResponseFields.FieldErrors.CODE] == FieldValidationErrorCode.FIELD_DUPLICATE.value

    def test_list_fields_allowed_duplicates_on_multipart(self):
        """Test that list fields are allowed to have duplicates in multipart/form-data"""
        test_file = SimpleUploadedFile("test.txt", b"test content")
        # Use list notation for multiple values which Django's test client will properly format
        data = {
            'name': 'test',
            'tags[]': ['tag1', 'tag2'],  # List field with multiple values
            'file': test_file
        }
        response = self.client.post(
            reverse(self.list_endpoint),
            data,
            HTTP_ACCEPT='application/json'
        )

        # Should not return 400, as list fields are allowed to have duplicates
        assert response.status_code != status.HTTP_400_BAD_REQUEST

    def test_duplicate_fields_on_multipart_put_then_400(self):
        """Test that duplicate non-list fields in multipart/form-data PUT requests are detected"""
        test_file = SimpleUploadedFile("test.txt", b"test content")
        data = {
            'name': 'test',  # First occurrence
            'name': 'test2',  # Second occurrence - should be detected as duplicate
            'file': test_file
        }
        response = self.client.put(
            reverse(self.detail_endpoint, kwargs={'pk': self.saved_object.uuid}),
            data,
            HTTP_ACCEPT='application/json'
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        self._set_bad_request_result(response)
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error[ErrorResponseFields.FieldErrors.FIELD] == CriteriaPostFields.NAME_PUBLIC
        assert error[ErrorResponseFields.FieldErrors.CODE] == FieldValidationErrorCode.FIELD_DUPLICATE.value

    def test_duplicate_fields_on_multipart_patch_then_400(self):
        """Test that duplicate non-list fields in multipart/form-data PATCH requests are detected"""
        test_file = SimpleUploadedFile("test.txt", b"test content")
        data = {
            'name': 'test',  # First occurrence
            'name': 'test2',  # Second occurrence - should be detected as duplicate
            'file': test_file
        }
        response = self.client.patch(
            reverse(self.detail_endpoint, kwargs={'pk': self.saved_object.uuid}),
            data,
            HTTP_ACCEPT='application/json'
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        self._set_bad_request_result(response)
        assert len(self.bad_request_result_field_errors) == 1
        error = self.bad_request_result_field_errors[0]
        assert error[ErrorResponseFields.FieldErrors.FIELD] == CriteriaPostFields.NAME_PUBLIC
        assert error[ErrorResponseFields.FieldErrors.CODE] == FieldValidationErrorCode.FIELD_DUPLICATE.value

    def test_list_fields_allowed_duplicates_on_multipart_put(self):
        """Test that list fields are allowed to have duplicates in multipart/form-data PUT requests"""
        test_file = SimpleUploadedFile("test.txt", b"test content")
        data = {
            'name': 'test',
            'tags[]': ['tag1', 'tag2'],  # List field with multiple values
            'file': test_file
        }
        response = self.client.put(
            reverse(self.detail_endpoint, kwargs={'pk': self.saved_object.uuid}),
            data,
            HTTP_ACCEPT='application/json'
        )

        # Should not return 400, as list fields are allowed to have duplicates
        assert response.status_code != status.HTTP_400_BAD_REQUEST

    def test_list_fields_allowed_duplicates_on_multipart_patch(self):
        """Test that list fields are allowed to have duplicates in multipart/form-data PATCH requests"""
        test_file = SimpleUploadedFile("test.txt", b"test content")
        data = {
            'name': 'test',
            'tags[]': ['tag1', 'tag2'],  # List field with multiple values
            'file': test_file
        }
        response = self.client.patch(
            reverse(self.detail_endpoint, kwargs={'pk': self.saved_object.uuid}),
            data,
            HTTP_ACCEPT='application/json'
        )

        # Should not return 400, as list fields are allowed to have duplicates
        assert response.status_code != status.HTTP_400_BAD_REQUEST

        # Also test with repeated field names in multipart data
        from django.test.client import encode_multipart

        # Use a regular dict with lists for multiple values
        multipart_data = {
            'name': 'test',
            'tags': ['tag1', 'tag2'],  # Multiple values for same field
            'file': test_file
        }
        content = encode_multipart('boundary', multipart_data)
        response = self.client.post(
            reverse(self.list_endpoint),
            content,
            content_type='multipart/form-data; boundary=boundary',
            HTTP_ACCEPT='application/json'
        )

        # Should not return 400, as list fields are allowed to have duplicates
        assert response.status_code != status.HTTP_400_BAD_REQUEST
