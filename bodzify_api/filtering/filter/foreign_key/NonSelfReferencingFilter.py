from typing import Optional

from django.db.models import QuerySet
from django_filters import FilterSet
from rest_framework.exceptions import ValidationError

from bodzify_api.filtering.filter.foreign_key.ForeignKeyFilter import ForeignKeyFilter


class NonSelfReferencingFilter(ForeignKeyFilter):
    def __init__(self, queryset=None, **kwargs):
        self._queryset = queryset
        super().__init__(**kwargs)

    def filter(self, queryset, value):
        parent: Optional[FilterSet] = getattr(self, 'parent', None)

        # First perform all standard ForeignKeyFilter validations
        filtered_queryset = super().filter(queryset, value)

        if value and parent and hasattr(parent, 'instance'):
            # If we have an instance and a value, check for self-reference
            instance = getattr(parent, 'instance', None)
            if instance and str(instance.pk) == str(value):
                raise ValidationError({
                    'message': 'Self-referencing is not allowed',
                    'code': 'validation_self_reference'
                })

        return filtered_queryset
