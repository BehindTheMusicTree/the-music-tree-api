from django_filters import rest_framework as filters
from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.filtering.set.AppFilterSet import AppFilterSet
from .Fields import Fields


class SearchParamFilterSet(AppFilterSet):
    query = filters.CharFilter()
    type = filters.CharFilter()

    class Meta:
        model = Playlist
        fields = [Fields.QUERY, Fields.TYPE]
