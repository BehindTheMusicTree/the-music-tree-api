
import re
import uuid

from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import gettext as _
from django_filters import FilterSet

from bodzify_api.exception.validation.app.AppValidationException import AppValidationException
from bodzify_api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.filtering.filter.char.EmptiableCharFilter import EmptiableCharFilter


class ForeignKeyFilter(EmptiableCharFilter):
    def __init__(self, queryset=None, **kwargs):
        self._queryset = queryset
        kwargs.pop('queryset', None)
        super().__init__(**kwargs)

    def filter(self, queryset, value):
        if value is None:
            return queryset
        elif value == '':
            # Check if the parameter was actually in the URL or if it's an artifact
            parent: FilterSet | None = getattr(self, 'parent', None)
            if not parent:
                raise ImproperlyConfigured('ForeignKeyFilter must be used within a FilterSet')

            # If we have a request and this parameter isn't in the original URL params,
            # treat it as if the parameter wasn't provided (no filtering)
            if hasattr(parent, 'request') and parent.request:
                original_params = parent.request.GET if hasattr(parent.request, 'GET') else parent.request.query_params
                if self.field_name not in original_params:
                    # Parameter wasn't in the URL, so don't filter
                    return queryset

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
