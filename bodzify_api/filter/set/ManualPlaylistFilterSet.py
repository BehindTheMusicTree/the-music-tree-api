from django_filters import CharFilter

from bodzify_api.filter.set.AppFilterSet import AppFilterSet
from bodzify_api.model.playlist.children.ManualPlaylist import Fields


class ManualPlaylistFilterSet(AppFilterSet):
    name = CharFilter(field_name=Fields.NAME, lookup_expr='icontains')

    class Meta:
        fields = [Fields.NAME]
