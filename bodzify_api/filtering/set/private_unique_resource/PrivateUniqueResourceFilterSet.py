from django_filters import DateTimeFilter

from bodzify_api.filtering.set.AppFilterSet import AppFilterSet
from bodzify_api.model.criteria.Criteria import Criteria
from .Fields import Fields


class PrivateUniqueResourceFilterSet(AppFilterSet):
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

    class Meta:
        model = Criteria
        fields = {
            Fields.CREATED_ON: ['exact', 'gt', 'lt', 'gte', 'lte'],
            Fields.UPDATED_ON: ['exact', 'gt', 'lt', 'gte', 'lte']
        }
