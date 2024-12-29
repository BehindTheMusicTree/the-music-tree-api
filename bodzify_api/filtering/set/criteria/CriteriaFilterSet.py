from bodzify_api.filtering.filter.ForeignKeyFilter import ForeignKeyFilter
from bodzify_api.filtering.filter.char.NonEmptiableCharFilter import NonEmptiableCharFilter
from bodzify_api.filtering.set.AppFilterSet import AppFilterSet
from bodzify_api.model.criteria.Criteria import Criteria
from .Fields import Fields


class CriteriaFilterSet(AppFilterSet):
    name = NonEmptiableCharFilter(field_name=Fields.NAME, lookup_expr='icontains')
    parent = ForeignKeyFilter(field_name=Fields.PARENT)

    class Meta:
        model = Criteria

        fields = [Fields.NAME, Fields.PARENT]
