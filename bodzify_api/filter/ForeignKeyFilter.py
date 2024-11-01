from typing import Optional

from django_filters import CharFilter, FilterSet
from django.http import HttpRequest
from rest_framework.request import Request


class ForeignKeyFilter(CharFilter):

    def filter(self, queryset, value):
        parent: Optional[FilterSet] = getattr(self, 'parent', None)
        if not parent:
            raise ValueError('ForeignKeyFilter must be used within a FilterSet')

        if self.field_name not in parent.data:
            return queryset

        if value == '':  # Empty string explicitly provided
            return queryset.filter(**{f"{self.field_name}__isnull": True})
        return super().filter(queryset, value)
