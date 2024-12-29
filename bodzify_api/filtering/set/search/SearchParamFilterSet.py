from django_filters import rest_framework as filters

from bodzify_api.filtering.set.private_unique_resource.PrivateUniqueResourceFilterSet import PrivateUniqueResourceFilterSet
from bodzify_api.model.playlist.Playlist import Playlist
from .Fields import Fields


class SearchParamFilterSet(PrivateUniqueResourceFilterSet):
    query = filters.CharFilter()
    type = filters.CharFilter()

    class Meta:
        model = Playlist
        fields = [Fields.QUERY, Fields.TYPE]
