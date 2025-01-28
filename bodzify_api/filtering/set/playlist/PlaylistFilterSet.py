from django_filters import rest_framework as filters

from bodzify_api.filtering.set.private_unique_resource.PrivateUniqueResourceFilterSet \
    import PrivateUniqueResourceFilterSet
from bodzify_api.model.playlist.Playlist import Playlist
from .Fields import Fields


class PlaylistFilterSet(PrivateUniqueResourceFilterSet):
    name = filters.CharFilter()
    type_label = filters.CharFilter()

    class Meta:
        model = Playlist
        fields = [Fields.NAME, Fields.TYPE_LABEL]
