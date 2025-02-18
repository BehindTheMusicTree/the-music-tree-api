from typing import Any

from django.core.exceptions import ObjectDoesNotExist
from rest_framework.relations import PrimaryKeyRelatedField

from bodzify_api.serializer.field.AppField import AppField
from bodzify_api.validator.AppValidationError import AppValidationError
from bodzify_api.validator.FieldValidationErrorCode import FieldValidationErrorCode


class ForeignKeyField(AppField, PrimaryKeyRelatedField):
    """
    Custom ForeignKey serializer field that raises AppValidationError instead of DRF's ValidationError.
    This ensures consistent error handling across the application.

    Supports additional filters for validation:
        track = ForeignKeyField(
            queryset=LibraryTrack.objects.all(),
            additional_filters={'user': request.user}
        )
    """

    def __init__(self, **kwargs):
        self.additional_filters = kwargs.pop('additional_filters', {})
        super().__init__(**kwargs)

    def fail(self, key: str, **kwargs: Any) -> None:
        """
        Raise an AppValidationError with appropriate error code and message.

        Args:
            key: The error key that maps to an error message
            **kwargs: Format parameters for the error message
        """
        try:
            msg = self.error_messages[key]
            if kwargs:
                msg = msg.format(**kwargs)
        except KeyError:
            class_name = self.__class__.__name__
            msg = f"Invalid input for {class_name}."

        if key == 'required':
            code = FieldValidationErrorCode.REQUIRED
        elif key == 'does_not_exist':
            code = FieldValidationErrorCode.INVALID_REFERENCE
        elif key == 'incorrect_type':
            code = FieldValidationErrorCode.INVALID_FORMAT
        else:
            code = FieldValidationErrorCode.DEFAULT

        raise AppValidationError(field=self.get_error_field_name(), message=msg, code=code)

    def get_queryset(self) -> Any:
        queryset = super().get_queryset()
        if self.additional_filters:
            queryset = queryset.filter(**self.additional_filters)
        return queryset

    def to_internal_value(self, data: Any) -> Any:
        if data == '' or (self.allow_null and data is None):
            if self.required:
                raise AppValidationError(
                    field=self.get_error_field_name(),
                    message='This field is required.',
                    code=FieldValidationErrorCode.REQUIRED,
                )
            return None

        return super().to_internal_value(data)
