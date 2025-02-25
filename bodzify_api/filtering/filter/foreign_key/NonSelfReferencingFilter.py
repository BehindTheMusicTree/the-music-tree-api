

from django.utils.translation import gettext as _
from django_filters import FilterSet

from bodzify_api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.exception.validation.app.AppValidationError import AppValidationException
from bodzify_api.filtering.filter.foreign_key.ForeignKeyFilter import ForeignKeyFilter


class NonSelfReferencingFilter(ForeignKeyFilter):
    def __init__(self, queryset=None, **kwargs):
        self._queryset = queryset
        super().__init__(**kwargs)

    def filter(self, queryset, value):
        parent: FilterSet | None = getattr(self, 'parent', None)

        # First perform all standard ForeignKeyFilter validations
        filtered_queryset = super().filter(queryset, value)

        if value and parent and hasattr(parent, 'instance'):
            instance = getattr(parent, 'instance', None)
            if instance and str(instance.pk) == str(value):
                raise AppValidationException(
                    field_name=str(self.field_name),
                    message=_('Self-referencing is not allowed'),
                    field_validation_error_code=FieldValidationErrorCode.SELF_REFERENCE
                )

        return filtered_queryset
