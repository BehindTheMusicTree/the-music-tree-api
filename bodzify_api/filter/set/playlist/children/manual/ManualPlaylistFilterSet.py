from django_filters import CharFilter

from bodzify_api.filter.set.AppFilterSet import AppFilterSet
from .Fields import Fields


class ManualPlaylistFilterSet(AppFilterSet):
    name = CharFilter(field_name=Fields.NAME, lookup_expr='icontains')

    class Meta:
        fields = [Fields.NAME]
