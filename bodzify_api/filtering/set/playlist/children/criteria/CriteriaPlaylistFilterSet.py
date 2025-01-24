from django_filters import rest_framework as filters

from bodzify_api.filtering.filter.foreign_key.ForeignKeyFilter import ForeignKeyFilter
from bodzify_api.filtering.set.AppFilterSet import AppFilterSet
from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.model.playlist.children.criteria.Fields import Fields as ModelFields
from .Fields import Fields


class CriteriaPlaylistFilterSet(AppFilterSet):
    name = filters.CharFilter(field_name=f'{ModelFields.CRITERIA}__{ModelFields.NAME}',
                              field_name_user_friendly=Fields.NAME,
                              lookup_expr="icontains")
    parent = ForeignKeyFilter(field_name=f'{ModelFields.CRITERIA}__{ModelFields.PARENT}',
                              field_name_user_friendly=Fields.PARENT,)

    class Meta:
        model = CriteriaPlaylist
        fields = [Fields.NAME, Fields.PARENT]
