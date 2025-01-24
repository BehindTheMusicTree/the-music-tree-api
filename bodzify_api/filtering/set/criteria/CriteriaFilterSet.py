from bodzify_api.filtering.filter.char.NonEmptiableCharFilter import NonEmptiableCharFilter
from bodzify_api.filtering.filter.foreign_key.DescendantAwareFilter import DescendantAwareFilter
from bodzify_api.filtering.set.private_unique_resource.PrivateUniqueResourceFilterSet import \
    PrivateUniqueResourceFilterSet
from bodzify_api.model.criteria.Criteria import Criteria
from .Fields import Fields


class CriteriaFilterSet(PrivateUniqueResourceFilterSet):
    name = NonEmptiableCharFilter(field_name=Fields.NAME_INTERNAL,
                                  lookup_expr='icontains',
                                  field_name_user_friendly=Fields.NAME)
    parent = DescendantAwareFilter(queryset=Criteria.objects.all(),)

    class Meta:
        model = Criteria
        fields = [Fields.NAME, Fields.PARENT]
