import pytest
from unittest.mock import Mock, MagicMock
from django.http import HttpRequest, QueryDict
from rest_framework.request import Request

from api.exception.validation.app.AppValidationException import AppValidationException
from api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from api.middleware.list_value_validation.middleware import ListValueValidationMiddleware


class TestListValueValidationMiddleware:

    def test_validate_list_values_multipart_with_mixed_empty_and_non_empty_then_raises_exception(self):
        middleware = ListValueValidationMiddleware(get_response=Mock())
        data = QueryDict(mutable=True)
        data.setlist('artists_names[]', ['Muse', ''])

        with pytest.raises(AppValidationException) as exc_info:
            middleware._validate_list_values_multipart(data)

        assert exc_info.value.field_validation_error_code == FieldValidationErrorCode.LIST_VALUE_EMPTY
        assert 'artistsNames[]' in exc_info.value.field or 'artists_names[]' in exc_info.value.field

    def test_validate_list_values_multipart_with_all_non_empty_then_passes(self):
        middleware = ListValueValidationMiddleware(get_response=Mock())
        data = QueryDict(mutable=True)
        data.setlist('artists_names[]', ['Muse', 'Radiohead'])

        # Should not raise
        middleware._validate_list_values_multipart(data)

    def test_validate_list_values_multipart_with_all_empty_then_passes(self):
        middleware = ListValueValidationMiddleware(get_response=Mock())
        data = QueryDict(mutable=True)
        data.setlist('artists_names[]', ['', ''])

        # Should not raise (all empty is allowed)
        middleware._validate_list_values_multipart(data)

    def test_validate_list_values_multipart_with_single_value_then_passes(self):
        middleware = ListValueValidationMiddleware(get_response=Mock())
        data = QueryDict(mutable=True)
        data.setlist('artists_names[]', ['Muse'])

        # Should not raise (single value doesn't trigger validation)
        middleware._validate_list_values_multipart(data)

    def test_validate_list_values_multipart_with_none_value_then_raises_exception(self):
        middleware = ListValueValidationMiddleware(get_response=Mock())
        data = QueryDict(mutable=True)
        # QueryDict.setlist doesn't accept None, so we'll test with empty string instead
        # None values would come from data transformation, not directly from QueryDict
        data.setlist('artists_names[]', ['Muse', ''])

        with pytest.raises(AppValidationException) as exc_info:
            middleware._validate_list_values_multipart(data)

        assert exc_info.value.field_validation_error_code == FieldValidationErrorCode.LIST_VALUE_EMPTY

    def test_validate_list_values_multipart_with_dict_then_handles_correctly(self):
        middleware = ListValueValidationMiddleware(get_response=Mock())
        data = {'artists_names[]': ['Muse', '']}

        with pytest.raises(AppValidationException) as exc_info:
            middleware._validate_list_values_multipart(data)

        assert exc_info.value.field_validation_error_code == FieldValidationErrorCode.LIST_VALUE_EMPTY

    def test_validate_list_values_multipart_with_non_list_field_then_passes(self):
        middleware = ListValueValidationMiddleware(get_response=Mock())
        data = QueryDict(mutable=True)
        data['title'] = 'My Title'

        # Should not raise (non-list fields are ignored)
        middleware._validate_list_values_multipart(data)

    def test_validate_list_values_json_with_mixed_empty_and_non_empty_then_raises_exception(self):
        middleware = ListValueValidationMiddleware(get_response=Mock())
        data = {'artistsNames': ['Muse', '']}

        with pytest.raises(AppValidationException) as exc_info:
            middleware._validate_list_values_json(data)

        assert exc_info.value.field_validation_error_code == FieldValidationErrorCode.LIST_VALUE_EMPTY

    def test_validate_list_values_json_with_all_non_empty_then_passes(self):
        middleware = ListValueValidationMiddleware(get_response=Mock())
        data = {'artistsNames': ['Muse', 'Radiohead']}

        # Should not raise
        middleware._validate_list_values_json(data)

    def test_validate_list_values_json_with_single_value_then_passes(self):
        middleware = ListValueValidationMiddleware(get_response=Mock())
        data = {'artistsNames': ['Muse']}

        # Should not raise (single value doesn't trigger validation)
        middleware._validate_list_values_json(data)

    def test_validate_list_values_json_with_non_list_value_then_passes(self):
        middleware = ListValueValidationMiddleware(get_response=Mock())
        data = {'title': 'My Title'}

        # Should not raise (non-list values are ignored)
        middleware._validate_list_values_json(data)

    def test_validate_list_values_json_with_empty_list_then_passes(self):
        middleware = ListValueValidationMiddleware(get_response=Mock())
        data = {'artistsNames': []}

        # Should not raise (empty list doesn't trigger validation)
        middleware._validate_list_values_json(data)

    def test_handle_validation_error_then_returns_json_response(self):
        middleware = ListValueValidationMiddleware(get_response=Mock())
        exc = AppValidationException(
            field_name='artistsNames',
            message='Empty values are not allowed',
            field_validation_error_code=FieldValidationErrorCode.LIST_VALUE_EMPTY
        )

        response = middleware._handle_validation_error(exc)

        assert response.status_code == 400
        import json
        response_data = json.loads(response.content)
        assert 'details' in response_data
        assert 'fieldErrors' in response_data['details'] or 'field_errors' in response_data['details']
