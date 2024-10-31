
from django_filters import rest_framework as filters
from bodzify_api.model.playlist.BasePlaylist import BasePlaylist, Fields as ModelFields
from bodzify_api.filter.set.AppFilterSet import AppFilterSet


class PlaylistParamFilterSet(AppFilterSet):
    name = filters.CharFilter()
    type = filters.CharFilter()

    class Meta:
        model = BasePlaylist
        fields = [ModelFields.NAME, ModelFields.TYPE]
