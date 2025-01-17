from typing import Optional
import uuid
import re

from django.core.exceptions import ImproperlyConfigured
from django_filters import CharFilter, FilterSet
from rest_framework.exceptions import ValidationError

from bodzify_api.filtering.filter.AppFilter import AppFilter


class ForeignKeyFilter(CharFilter, AppFilter):

    def filter(self, queryset, value):
        parent: Optional[FilterSet] = getattr(self, 'parent', None)
        if not parent:
            raise ImproperlyConfigured('ForeignKeyFilter must be used within a FilterSet')

        if self.field_name not in parent.data:
            return queryset

        if value == '':  # Empty string explicitly provided
            return queryset.filter(**{f"{self.field_name}__isnull": True})

        # Check if value is a template variable
        if re.match(r'{{.*}}', str(value)):
            raise ValidationError({
                'message': f'{value} is not a valid UUID',
                'code': 'validation_invalid_input'
            })

        # Custom UUID validation
        try:
            if value and not isinstance(value, uuid.UUID):
                uuid.UUID(str(value))
        except (TypeError, ValueError):
            raise ValidationError({
                'message': f'{value} is not a valid UUID',
                'code': 'validation_invalid_input'
            })

        return super().filter(queryset, value)
