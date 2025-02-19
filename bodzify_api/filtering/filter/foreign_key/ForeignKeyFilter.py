from typing import Optional
import uuid
import re

from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import gettext as _
from django_filters import CharFilter, FilterSet

from bodzify_api.validator.AppValidationError import AppValidationError

from bodzify_api.filtering.filter.AppFilter import AppFilter
from bodzify_api.validator.FieldValidationErrorCode import FieldValidationErrorCode


class ForeignKeyFilter(CharFilter, AppFilter):
    def __init__(self, queryset=None, **kwargs):
        self._queryset = queryset
        kwargs.pop('queryset', None)
        super().__init__(**kwargs)

    def filter(self, queryset, value):
        parent: Optional[FilterSet] = getattr(self, 'parent', None)
        if not parent:
            raise ImproperlyConfigured('ForeignKeyFilter must be used within a FilterSet')

        if value == '':  # Empty string explicitly provided
            return queryset.filter(**{f"{self.field_name}__isnull": True})

        if re.match(r'{{.*}}', str(value)):
            raise AppValidationError(
                field=str(self.field_name),
                message=_('%(value)s is not a valid UUID') % {'value': value},
                field_validation_error_code=FieldValidationErrorCode.INVALID_FORMAT
            )

        try:
            if value and not isinstance(value, uuid.UUID):
                uuid.UUID(str(value))
        except (TypeError, ValueError):
            raise AppValidationError(
                field=str(self.field_name),
                message=_('%(value)s is not a valid UUID') % {'value': value},
                field_validation_error_code=FieldValidationErrorCode.INVALID_FORMAT
            )

        return super().filter(queryset, value)
