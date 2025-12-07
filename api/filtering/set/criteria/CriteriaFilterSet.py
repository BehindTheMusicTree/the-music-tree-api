from api.filtering.filter.char.NonEmptiableCharFilter import NonEmptiableCharFilter
from api.filtering.filter.foreign_key.DescendantAwareFilter import DescendantAwareFilter
from api.filtering.set.private_unique_resource.PrivateUniqueResourceFilterSet import (
    PrivateUniqueResourceFilterSet
)
from api.model.criteria.Criteria import Criteria

from .Fields import Fields


class CriteriaFilterSet(PrivateUniqueResourceFilterSet):
    name = NonEmptiableCharFilter(lookup_expr='icontains')
    parent = DescendantAwareFilter(queryset=Criteria.objects.all(),)

    class Meta:
        model = Criteria
        fields = [
            Fields.NAME_PUBLIC,
            Fields.PARENT,
            *PrivateUniqueResourceFilterSet.get_date_fields()
        ]
