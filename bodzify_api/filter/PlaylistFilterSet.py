from django_filters import CharFilter

from bodzify_api.filter.AppFilterSet import AppFilterSet
from bodzify_api.model.playlist.BasePlaylist import Fields


class PlaylistFilterSet(AppFilterSet):
    name = CharFilter(field_name=Fields.NAME, lookup_expr='icontains')
    type = CharFilter(field_name=Fields.TYPE, lookup_expr='icontains')

    class Meta:
        fields = [Fields.NAME, Fields.TYPE]