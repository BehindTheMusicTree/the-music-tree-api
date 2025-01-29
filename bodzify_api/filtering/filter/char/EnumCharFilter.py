from typing import Type

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from bodzify_api.filtering.filter.char.EmptiableCharFilter import EmptiableCharFilter
from bodzify_api.filtering.set.AppFilterSet import AppFilterSet


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
            raise ValidationError({
                str(self.field_name): [_('This field may not be blank.')]
            }, code='blank')

        if value is not None:
            normalized_value = str(value).lower()
            if normalized_value not in self.valid_values:
                raise ValidationError(
                    _('%(value)s is not a valid value. Allowed values are: %(valid_values)s'),
                    params={'value': value, 'valid_values': ', '.join(self.valid_values)},
                    code='invalid_enum'
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
