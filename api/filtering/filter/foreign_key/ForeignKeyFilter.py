
import re
import uuid

from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import gettext as _
from django_filters import FilterSet

from api.exception.validation.app.AppValidationException import AppValidationException
from api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from api.filtering.filter.char.EmptiableCharFilter import EmptiableCharFilter


class ForeignKeyFilter(EmptiableCharFilter):
    def __init__(self, queryset=None, **kwargs):
        self._queryset = queryset
        kwargs.pop('queryset', None)
        super().__init__(**kwargs)

    def filter(self, queryset, value):
        # Let the parent AppFilter handle None values and URL parameter checking for empty strings
        if value is None or (value == '' and not self.is_param_in_request()):
            return queryset

        if value == '':
            # Empty string was explicitly provided in the URL, filter for NULL
            return queryset.filter(**{f"{self.field_name}__isnull": True})

        parent: FilterSet | None = getattr(self, 'parent', None)
        if not parent:
            raise ImproperlyConfigured('ForeignKeyFilter must be used within a FilterSet')

        if re.match(r'{{.*}}', str(value)):
            raise AppValidationException(
                field_name=str(self.field_name),
                message=_('%(value)s is not a valid UUID') % {'value': value},
                field_validation_error_code=FieldValidationErrorCode.FORMAT_INVALID
            )

        try:
            if value and not isinstance(value, uuid.UUID):
                uuid.UUID(str(value))
        except (TypeError, ValueError):
            raise AppValidationException(
                field_name=str(self.field_name),
                message=_('%(value)s is not a valid UUID') % {'value': value},
                field_validation_error_code=FieldValidationErrorCode.FORMAT_INVALID
            )

        return super().filter(queryset, value)
