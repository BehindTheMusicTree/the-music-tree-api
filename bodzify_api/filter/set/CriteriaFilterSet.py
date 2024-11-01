import logging

from django_filters import CharFilter

from bodzify_api.filter.ForeignKeyFilter import ForeignKeyFilter
from bodzify_api.filter.set.AppFilterSet import AppFilterSet
from bodzify_api.model.criteria.Criteria import Fields as ModelFields, Criteria

logger = logging.getLogger(__name__)


class Fields:
    NAME = ModelFields.NAME
    PARENT = ModelFields.PARENT


class CriteriaFilterSet(AppFilterSet):
    name = CharFilter(field_name=Fields.NAME, lookup_expr='icontains')
    parent = ForeignKeyFilter(field_name=Fields.PARENT)

    class Meta:
        model = Criteria
        fields = [Fields.NAME, Fields.PARENT]
