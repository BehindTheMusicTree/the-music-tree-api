from typing import TYPE_CHECKING

from django_filters import CharFilter
from django_filters.constants import EMPTY_VALUES

if TYPE_CHECKING:
    from bodzify_api.filter.set.AppFilterSet import AppFilterSet


class EmptiableCharFilter(CharFilter):
    def __init__(self, *args, **kwargs):
        self.method_name = kwargs.pop('method', None)
        super().__init__(*args, **kwargs)

    def filter(self, qs, value):
        if not self.method_name:
            return super().filter(qs, value)

        if hasattr(self, 'parent'):
            parent: AppFilterSet = self.parent  # type: ignore
            method = getattr(parent, self.method_name, None)
            if not method:
                raise AttributeError(f'{parent} object has no attribute {self.method_name}')
            if value is not None:
                qs = method(qs, self.field_name, value)
        return qs
