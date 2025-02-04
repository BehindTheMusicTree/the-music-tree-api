from typing import Optional

from django.utils.translation import gettext as _
from django_filters import FilterSet

from bodzify_api.filtering.filter.foreign_key.ForeignKeyFilter import ForeignKeyFilter
from bodzify_api.view.error.AppValidationError import AppValidationError
from bodzify_api.view.error.FieldValidationErrorCode import FieldValidationErrorCode


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
                # Since this is field validation (filter), use from_field
                raise AppValidationError.from_field(
                    field=str(self.field_name),
                    message=_('Self-referencing is not allowed'),
                    code=FieldValidationErrorCode.FIELD_SELF_REFERENCE
                )

        return filtered_queryset
