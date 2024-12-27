from bodzify_api.filter.ForeignKeyFilter import ForeignKeyFilter
from bodzify_api.filter.NonEmptyCharFilter import NonEmptyCharFilter
from bodzify_api.filter.set.AppFilterSet import AppFilterSet
from bodzify_api.model.criteria.Criteria import Criteria
from .Fields import Fields


class CriteriaFilterSet(AppFilterSet):
    name = NonEmptyCharFilter(field_name=Fields.NAME, lookup_expr='icontains')
    parent = ForeignKeyFilter(field_name=Fields.PARENT)

    class Meta:
        model = Criteria
   
        fields = [Fields.NAME, Fields.PARENT]
