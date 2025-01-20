from bodzify_api.filtering.filter.ForeignKeyFilter import ForeignKeyFilter
from bodzify_api.filtering.filter.char.NonEmptiableCharFilter import NonEmptiableCharFilter
from bodzify_api.filtering.set.private_unique_resource.PrivateUniqueResourceFilterSet import \
    PrivateUniqueResourceFilterSet
from bodzify_api.filtering.set.private_unique_resource.Fields import Fields as PrivateUniqueResourceFields
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.serializer.field.DescendantAwareField import DescendantAwareField
from .Fields import Fields


class CriteriaFilterSet(PrivateUniqueResourceFilterSet):
    name = NonEmptiableCharFilter(field_name=Fields.NAME_INTERNAL,
                                  lookup_expr='icontains',
                                  field_name_user_friendly=Fields.NAME)
    parent = DescendantAwareField(queryset=Criteria.objects.all(),)

    class Meta:
        model = Criteria
        fields = [Fields.NAME, Fields.PARENT]
