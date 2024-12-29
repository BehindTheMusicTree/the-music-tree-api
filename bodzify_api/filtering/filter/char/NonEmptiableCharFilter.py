from typing import Any
from rest_framework.exceptions import ValidationError
from django.db.models import QuerySet
from django_filters.filterset import FilterSet

from bodzify_api.filtering.filter.char.EmptiableCharFilter import EmptiableCharFilter


class NonEmptiableCharFilter(EmptiableCharFilter):
    parent: FilterSet

    def filter(self, qs: QuerySet, value: str) -> QuerySet:
        parent_data = getattr(self.parent, 'data', {})

        if (self.field_name_user_friendly or self.field_name) in parent_data:
            if value == '':
                raise ValidationError({self.field_name_user_friendly or self.field_name: "The field cannot be empty"})

        return super().filter(qs, value)
