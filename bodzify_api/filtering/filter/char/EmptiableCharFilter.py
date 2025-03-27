from typing import TYPE_CHECKING

from django_filters import CharFilter

from bodzify_api.filtering.filter.AppFilter import AppFilter
from bodzify_api.model.base.BaseQuerySet import BaseQuerySet


if TYPE_CHECKING:
    from bodzify_api.filtering.set.AppFilterSet import AppFilterSet


class EmptiableCharFilter(CharFilter, AppFilter):
    def __init__(self, *args, **kwargs):
        self.method_name = kwargs.pop('method', None)
        super().__init__(*args, **kwargs)

    def filter(self, qs: BaseQuerySet, value):
        # Handle None values first, no filtering
        if value is None:
            return qs

        if not self.method_name:
            if value == '':
                # Check if the parameter is in the URL before filtering
                if not self.is_param_in_request():
                    return qs
                # Empty string was explicitly provided, filter for NULL
                lookup = f"{self.field_name}__isnull"
                return qs.filter(**{lookup: True})
            else:
                result = super().filter(qs, value)
                return result

        if hasattr(self, 'parent'):
            parent: AppFilterSet = self.parent  # type: ignore
            method = getattr(parent, self.method_name, None)
            if not method:
                raise AttributeError(f'{parent} object has no attribute {self.method_name}')
            if value is not None:
                qs = method(qs, self.field_name, value)
        return qs
