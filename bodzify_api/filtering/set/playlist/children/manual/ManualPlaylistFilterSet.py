
from bodzify_api.filtering.filter.char.NonEmptiableCharFilter import     NonEmptiableCharFilter
from bodzify_api.filtering.set.AppFilterSet import AppFilterSet

from .Fields import Fields


class ManualPlaylistFilterSet(AppFilterSet):
    name = NonEmptiableCharFilter(lookup_expr='icontains')

    class Meta:
        fields = [Fields.NAME_PUBLIC]
