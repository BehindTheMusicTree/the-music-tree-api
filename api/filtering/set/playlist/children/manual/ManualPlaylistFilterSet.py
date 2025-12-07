
from api.filtering.filter.char.NonEmptiableCharFilter import NonEmptiableCharFilter
from api.filtering.set.private_unique_resource.PrivateUniqueResourceFilterSet import PrivateUniqueResourceFilterSet
from api.model.playlist.children.manual.ManualPlaylist import ManualPlaylist

from .Fields import Fields


class ManualPlaylistFilterSet(PrivateUniqueResourceFilterSet):
    name = NonEmptiableCharFilter(lookup_expr='icontains')

    class Meta:
        model = ManualPlaylist
        fields = [Fields.NAME_PUBLIC, *PrivateUniqueResourceFilterSet.get_date_fields()]
