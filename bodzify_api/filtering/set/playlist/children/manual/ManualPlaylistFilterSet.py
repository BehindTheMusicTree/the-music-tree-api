
from bodzify_api.filtering.filter.char.NonEmptiableCharFilter import NonEmptiableCharFilter
from bodzify_api.filtering.set.private_unique_resource.PrivateUniqueResourceFilterSet import PrivateUniqueResourceFilterSet

from .Fields import Fields


class ManualPlaylistFilterSet(PrivateUniqueResourceFilterSet):
    name = NonEmptiableCharFilter(lookup_expr='icontains')

    class Meta:
        fields = [Fields.NAME_PUBLIC, *PrivateUniqueResourceFilterSet.get_date_fields()]
