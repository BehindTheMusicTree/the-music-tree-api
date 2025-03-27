from django_filters import DateTimeFilter

from bodzify_api.filtering.set.AppFilterSet import AppFilterSet

from .Fields import Fields


class PrivateUniqueResourceFilterSet(AppFilterSet):
    """
    An abstract FilterSet for models that inherit from PrivateUniqueResource.
    Provides common date filtering capabilities.
    """
    created_on = DateTimeFilter(field_name=Fields.CREATED_ON)
    created_on_gt = DateTimeFilter(field_name=Fields.CREATED_ON, lookup_expr='gt')
    created_on_lt = DateTimeFilter(field_name=Fields.CREATED_ON, lookup_expr='lt')
    created_on_gte = DateTimeFilter(field_name=Fields.CREATED_ON, lookup_expr='gte')
    created_on_lte = DateTimeFilter(field_name=Fields.CREATED_ON, lookup_expr='lte')

    updated_on = DateTimeFilter(field_name=Fields.UPDATED_ON)
    updated_on_gt = DateTimeFilter(field_name=Fields.UPDATED_ON, lookup_expr='gt')
    updated_on_lt = DateTimeFilter(field_name=Fields.UPDATED_ON, lookup_expr='lt')
    updated_on_gte = DateTimeFilter(field_name=Fields.UPDATED_ON, lookup_expr='gte')
    updated_on_lte = DateTimeFilter(field_name=Fields.UPDATED_ON, lookup_expr='lte')

    @classmethod
    def get_date_fields(cls):
        return [
            Fields.CREATED_ON,
            Fields.CREATED_ON_GT,
            Fields.CREATED_ON_LT,
            Fields.CREATED_ON_GTE,
            Fields.CREATED_ON_LTE,
            Fields.UPDATED_ON,
            Fields.UPDATED_ON_GT,
            Fields.UPDATED_ON_LT,
            Fields.UPDATED_ON_GTE,
            Fields.UPDATED_ON_LTE,
        ]

    class Meta:
        abstract = True
        fields = [
            Fields.CREATED_ON,
            Fields.UPDATED_ON,
        ]
