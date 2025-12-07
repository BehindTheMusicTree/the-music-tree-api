import pytest

from api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from api.exception.validation.app.AppValidationException import AppValidationException
from api.serializer.field.AppBooleanField import AppBooleanField


class TestAppBooleanField:

    def test_string_true_then_returns_true(self):
        field = AppBooleanField()
        assert field.to_internal_value("true") is True

    def test_string_true_uppercase_then_returns_true(self):
        field = AppBooleanField()
        assert field.to_internal_value("TRUE") is True

    def test_string_false_then_returns_false(self):
        field = AppBooleanField()
        assert field.to_internal_value("false") is False

    def test_string_false_uppercase_then_returns_false(self):
        field = AppBooleanField()
        assert field.to_internal_value("FALSE") is False

    def test_string_1_then_raises_app_validation_exception(self):
        field = AppBooleanField()
        field.field_name = "archived"

        with pytest.raises(AppValidationException) as exc_info:
            field.to_internal_value("1")

        assert exc_info.value.field_validation_error_code == FieldValidationErrorCode.DEFAULT

    def test_string_0_then_raises_app_validation_exception(self):
        field = AppBooleanField()
        field.field_name = "archived"

        with pytest.raises(AppValidationException) as exc_info:
            field.to_internal_value("0")

        assert exc_info.value.field_validation_error_code == FieldValidationErrorCode.DEFAULT

    def test_string_empty_then_raises_app_validation_exception(self):
        field = AppBooleanField()
        field.field_name = "archived"

        with pytest.raises(AppValidationException) as exc_info:
            field.to_internal_value("")

        assert exc_info.value.field_validation_error_code == FieldValidationErrorCode.DEFAULT

    def test_string_t_then_raises_app_validation_exception(self):
        field = AppBooleanField()
        field.field_name = "archived"

        with pytest.raises(AppValidationException) as exc_info:
            field.to_internal_value("t")

        assert exc_info.value.field_validation_error_code == FieldValidationErrorCode.DEFAULT

    def test_string_f_then_raises_app_validation_exception(self):
        field = AppBooleanField()
        field.field_name = "archived"

        with pytest.raises(AppValidationException) as exc_info:
            field.to_internal_value("f")

        assert exc_info.value.field_validation_error_code == FieldValidationErrorCode.DEFAULT

    def test_string_yes_then_raises_app_validation_exception(self):
        field = AppBooleanField()
        field.field_name = "archived"

        with pytest.raises(AppValidationException) as exc_info:
            field.to_internal_value("yes")

        assert exc_info.value.field_validation_error_code == FieldValidationErrorCode.DEFAULT

    def test_string_no_then_raises_app_validation_exception(self):
        field = AppBooleanField()
        field.field_name = "archived"

        with pytest.raises(AppValidationException) as exc_info:
            field.to_internal_value("no")

        assert exc_info.value.field_validation_error_code == FieldValidationErrorCode.DEFAULT

    def test_string_on_then_raises_app_validation_exception(self):
        field = AppBooleanField()
        field.field_name = "archived"

        with pytest.raises(AppValidationException) as exc_info:
            field.to_internal_value("on")

        assert exc_info.value.field_validation_error_code == FieldValidationErrorCode.DEFAULT

    def test_string_off_then_raises_app_validation_exception(self):
        field = AppBooleanField()
        field.field_name = "archived"

        with pytest.raises(AppValidationException) as exc_info:
            field.to_internal_value("off")

        assert exc_info.value.field_validation_error_code == FieldValidationErrorCode.DEFAULT

    def test_string_with_whitespace_then_strips_and_returns_true(self):
        field = AppBooleanField()
        assert field.to_internal_value("  true  ") is True

    def test_string_with_whitespace_then_strips_and_returns_false(self):
        field = AppBooleanField()
        assert field.to_internal_value("  false  ") is False

    def test_int_1_then_raises_app_validation_exception(self):
        field = AppBooleanField()
        field.field_name = "archived"

        with pytest.raises(AppValidationException) as exc_info:
            field.to_internal_value(1)

        assert exc_info.value.field_validation_error_code == FieldValidationErrorCode.DEFAULT

    def test_int_0_then_raises_app_validation_exception(self):
        field = AppBooleanField()
        field.field_name = "archived"

        with pytest.raises(AppValidationException) as exc_info:
            field.to_internal_value(0)

        assert exc_info.value.field_validation_error_code == FieldValidationErrorCode.DEFAULT

    def test_float_1_then_raises_app_validation_exception(self):
        field = AppBooleanField()
        field.field_name = "archived"

        with pytest.raises(AppValidationException) as exc_info:
            field.to_internal_value(1.0)

        assert exc_info.value.field_validation_error_code == FieldValidationErrorCode.DEFAULT

    def test_float_0_then_raises_app_validation_exception(self):
        field = AppBooleanField()
        field.field_name = "archived"

        with pytest.raises(AppValidationException) as exc_info:
            field.to_internal_value(0.0)

        assert exc_info.value.field_validation_error_code == FieldValidationErrorCode.DEFAULT

    def test_bool_true_then_returns_true(self):
        field = AppBooleanField()
        assert field.to_internal_value(True) is True

    def test_bool_false_then_returns_false(self):
        field = AppBooleanField()
        assert field.to_internal_value(False) is False

    def test_none_with_allow_null_then_returns_none(self):
        field = AppBooleanField(allow_null=True)
        assert field.to_internal_value(None) is None

    def test_none_without_allow_null_then_raises_app_validation_exception(self):
        field = AppBooleanField(allow_null=False)
        field.field_name = "archived"

        with pytest.raises(AppValidationException) as exc_info:
            field.to_internal_value(None)

        assert exc_info.value.field_validation_error_code == FieldValidationErrorCode.REQUIRED

    def test_invalid_string_then_raises_app_validation_exception(self):
        field = AppBooleanField()
        field.field_name = "archived"

        with pytest.raises(AppValidationException) as exc_info:
            field.to_internal_value("invalid")

        assert exc_info.value.field_validation_error_code == FieldValidationErrorCode.DEFAULT

    def test_invalid_int_then_raises_app_validation_exception(self):
        field = AppBooleanField()
        field.field_name = "archived"

        with pytest.raises(AppValidationException) as exc_info:
            field.to_internal_value(2)

        assert exc_info.value.field_validation_error_code == FieldValidationErrorCode.DEFAULT

    def test_invalid_float_then_raises_app_validation_exception(self):
        field = AppBooleanField()
        field.field_name = "archived"

        with pytest.raises(AppValidationException) as exc_info:
            field.to_internal_value(0.5)

        assert exc_info.value.field_validation_error_code == FieldValidationErrorCode.DEFAULT

    def test_dict_then_raises_app_validation_exception(self):
        field = AppBooleanField()
        field.field_name = "archived"

        with pytest.raises(AppValidationException) as exc_info:
            field.to_internal_value({"value": True})

        assert exc_info.value.field_validation_error_code == FieldValidationErrorCode.DEFAULT
