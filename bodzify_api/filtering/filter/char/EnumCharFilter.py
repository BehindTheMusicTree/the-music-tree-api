from typing import Type

from django.utils.translation import gettext_lazy as _

from bodzify_api.filtering.filter.char.EmptiableCharFilter import EmptiableCharFilter
from bodzify_api.filtering.set.AppFilterSet import AppFilterSet
from bodzify_api.view.error.AppValidationError import AppValidationError
from bodzify_api.view.error.FieldValidationErrorCode import FieldValidationErrorCode


class EnumCharFilter(EmptiableCharFilter):
    def __init__(self, *args, enum_class: Type, **kwargs):
        self.enum_class = enum_class
        super().__init__(*args, **kwargs)

    @property
    def valid_values(self) -> list[str]:
        return [str(value).lower() for value in vars(self.enum_class).values()
                if isinstance(value, str) and not value.startswith('_')]

    def filter(self, qs, value):
        if value == '':
            # Since this is field validation, use from_field
            raise AppValidationError.from_field(
                field=str(self.field_name),
                message=_('This field may not be blank.'),
                code=FieldValidationErrorCode.FIELD_BLANK
            )

        if value is not None:
            normalized_value = str(value).lower()
            if normalized_value not in self.valid_values:
                # Since this is field validation, use from_field
                raise AppValidationError.from_field(
                    field=str(self.field_name),
                    message=_('%(value)s is not a valid value. Allowed values are: %(valid_values)s') % {
                        'value': value,
                        'valid_values': ', '.join(self.valid_values)
                    },
                    code=FieldValidationErrorCode.FIELD_INVALID_ENUM
                )

            # If we have a method defined, use it for filtering
            if self.method_name:
                if hasattr(self, 'parent'):
                    parent: AppFilterSet = self.parent  # type: ignore
                    method = getattr(parent, self.method_name, None)
                    if not method:
                        raise AttributeError(f'{parent} object has no attribute {self.method_name}')
                    return method(qs, self.field_name, value)
                return qs

        # When no method is specified, just return the queryset (validation only)
        return qs
