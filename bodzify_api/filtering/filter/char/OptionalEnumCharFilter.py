
from django_filters.filterset import FilterSet

from bodzify_api.filtering.filter.char.EnumCharFilter import EnumCharFilter
from bodzify_api.model.base.BaseQuerySet import BaseQuerySet


class OptionalEnumCharFilter(EnumCharFilter):
    parent: FilterSet

    def filter(self, qs: BaseQuerySet, value: str) -> BaseQuerySet:
        parent_data = getattr(self.parent, 'data', {})

        if (self.field_name_user_friendly or self.field_name) not in parent_data:
            return qs

        return super().filter(qs, value)
