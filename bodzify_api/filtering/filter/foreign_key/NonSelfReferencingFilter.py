from typing import Optional

from django.utils.translation import gettext as _
from django_filters import FilterSet

from bodzify_api.filtering.filter.foreign_key.ForeignKeyFilter import ForeignKeyFilter
from bodzify_api.utils.validation_error_utils import raise_validation_error
from bodzify_api.view.error.ValidationResponseCode import ValidationResponseCode


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
                raise_validation_error(
                    message=_('Self-referencing is not allowed'),
                    code=ValidationResponseCode.FIELD_SELF_REFERENCE.value,
                    field=str(self.field_name)
                )

        return filtered_queryset
