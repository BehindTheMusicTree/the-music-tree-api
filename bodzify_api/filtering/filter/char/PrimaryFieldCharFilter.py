

from django.core.exceptions import ImproperlyConfigured
from django.db.models import Q, QuerySet

from bodzify_api.filtering.filter.char.EmptiableCharFilter import \
    EmptiableCharFilter


class PrimaryFieldCharFilter(EmptiableCharFilter):
    """
    A filter that handles filtering by a primary field of a related instance.
    When the filter value is empty, it returns results with no related instance.
    """

    def __init__(self, primary_field: str, lookup_expr: str = 'iexact', *args, **kwargs):
        if not primary_field:
            raise ImproperlyConfigured(
                f'{self.__class__.__name__} requires a primary_field argument.'
            )

        self.primary_field = primary_field
        # Pass lookup_expr through kwargs instead of setting it directly as self.lookup_expr
        # to ensure proper field-level configuration in CharFilter parent class
        kwargs['lookup_expr'] = lookup_expr
        super().__init__(*args, **kwargs)

    def filter(self, qs: QuerySet, value: str | None) -> QuerySet:
        if not self.field_name:
            raise ImproperlyConfigured(
                f'{self.__class__.__name__} requires a field_name to be set.'
            )

        if not value:
            return qs.filter(**{f"{self.field_name}__isnull": True})

        lookup = f"{self.field_name}__{self.primary_field}__{self.lookup_expr}"
        return qs.filter(Q(**{lookup: value}))
