from django_filters import rest_framework as filters

from bodzify_api.filtering.set.private_unique_resource.PrivateUniqueResourceFilterSet \
    import PrivateUniqueResourceFilterSet
from .Fields import Fields


class SearchFilterSet(PrivateUniqueResourceFilterSet):
    """
    Base filterset for search functionality across different models.
    Each model using this filterset should specify the search_fields in Meta class.
    """
    query = filters.CharFilter(method='filter_query')

    def filter_query(self, queryset, name, value):
        if not value:
            return queryset

        search_fields = getattr(self.Meta, 'search_fields', [])
        if not search_fields:
            return queryset

        filters = []
        for field in search_fields:
            filters.append({f"{field}__icontains": value})

        q_objects = filters[0]
        for f in filters[1:]:
            q_objects |= f

        return queryset.filter(**q_objects).distinct()

    class Meta:
        fields = [Fields.QUERY]