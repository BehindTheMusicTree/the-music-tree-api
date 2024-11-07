from django_filters import rest_framework as filters
from bodzify_api.model.playlist.BasePlaylist import BasePlaylist
from bodzify_api.filter.set.AppFilterSet import AppFilterSet
from .Fields import Fields


class SearchParamFilterSet(AppFilterSet):
    query = filters.CharFilter()
    type = filters.CharFilter()

    class Meta:
        model = BasePlaylist
        fields = [Fields.QUERY, Fields.TYPE]
