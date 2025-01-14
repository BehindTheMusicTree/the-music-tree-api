from typing import TYPE_CHECKING

from django_filters import CharFilter

from bodzify_api.filtering.filter.AppFilter import AppFilter

if TYPE_CHECKING:
    from bodzify_api.filtering.set.AppFilterSet import AppFilterSet


class EmptiableCharFilter(CharFilter, AppFilter):
    def __init__(self, *args, **kwargs):
        self.method_name = kwargs.pop('method', None)
        super().__init__(*args, **kwargs)

    def filter(self, qs, value):
        print("\n=== EmptiableCharFilter Debug ===")
        print(f"Field name: {self.field_name}")
        print(f"Lookup expr: {self.lookup_expr}")
        print(f"Method name: {self.method_name}")
        print(f"Value: {value}")
        print(f"Initial queryset: {qs}")

        if not self.method_name:
            print("Using CharFilter's filter method")
            result = super().filter(qs, value)
            print(f"Result from CharFilter: {result}")
            return result

        if hasattr(self, 'parent'):
            parent: AppFilterSet = self.parent  # type: ignore
            method = getattr(parent, self.method_name, None)
            if not method:
                raise AttributeError(f'{parent} object has no attribute {self.method_name}')
            if value is not None:
                print(f"Using method {self.method_name}")
                qs = method(qs, self.field_name, value)
                print(f"Result from method: {qs}")
        print("=========================\n")
        return qs
