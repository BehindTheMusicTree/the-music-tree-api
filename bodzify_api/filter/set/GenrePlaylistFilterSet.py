from django_filters import rest_framework as filters  # type: ignore

from bodzify_api.filter.ForeignKeyFilter import ForeignKeyFilter
from bodzify_api.filter.set.AppFilterSet import AppFilterSet
from bodzify_api.model.criteria.Criteria import Fields as ModelFields
from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist, Fields as ModelFields
from bodzify_api.model.criteria.CriteriaType import CriteriaTypesId


class Fields:
    NAME = ModelFields.NAME
    PARENT = ModelFields.PARENT


class GenrePlaylistFilterSet(AppFilterSet):
    name = filters.CharFilter(field_name=f'{ModelFields.CRITERIA}__{ModelFields.NAME}', lookup_expr="icontains")
    parent = ForeignKeyFilter(field_name=f'{ModelFields.CRITERIA}__{ModelFields.PARENT}')

    class Meta:
        model = CriteriaPlaylist
        fields = [Fields.NAME, Fields.PARENT]

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        return queryset.filter(type_id=CriteriaTypesId.GENRE)
