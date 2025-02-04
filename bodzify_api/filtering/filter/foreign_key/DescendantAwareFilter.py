from typing import Optional

from django.utils.translation import gettext as _
from django_filters import FilterSet

from bodzify_api.filtering.filter.foreign_key.NonSelfReferencingFilter import NonSelfReferencingFilter
from bodzify_api.utils.validation_error_utils import raise_validation_error
from bodzify_api.view.error.FieldValidationErrorCode import FieldValidationErrorCode


class DescendantAwareFilter(NonSelfReferencingFilter):
    def __init__(self, queryset=None, **kwargs):
        self._queryset = queryset
        super().__init__(**kwargs)

    def filter(self, queryset, value):
        parent: Optional[FilterSet] = getattr(self, 'parent', None)

        # First perform all NonSelfReferencingFilter validations
        filtered_queryset = super().filter(queryset, value)

        if value and parent and hasattr(parent, 'instance'):
            instance = getattr(parent, 'instance', None)
            if instance is None:
                return filtered_queryset

            # Check if model has required method
            if not hasattr(instance, 'is_descendant_of'):
                raise AttributeError(
                    f'Model {instance.__class__.__name__} must implement is_descendant_of method'
                )

            # Get the target object from the queryset's model
            target = queryset.model.objects.filter(pk=value).first()
            if target is not None and instance.is_descendant_of(target):
                raise_validation_error(
                    message=_('Cannot reference an ancestor'),
                    field_validation_error_code=FieldValidationErrorCode.FIELD_ANCESTOR_REFERENCE,
                    field=str(self.field_name)
                )

        return filtered_queryset
