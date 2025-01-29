from django.db.models import QuerySet
from django_filters.filterset import FilterSet

from bodzify_api.filtering.filter.char.EnumCharFilter import EnumCharFilter


class OptionalEnumCharFilter(EnumCharFilter):
    parent: FilterSet

    def filter(self, qs: QuerySet, value: str) -> QuerySet:
        parent_data = getattr(self.parent, 'data', {})
        
        if (self.field_name_user_friendly or self.field_name) not in parent_data:
            return qs
            
        return super().filter(qs, value)