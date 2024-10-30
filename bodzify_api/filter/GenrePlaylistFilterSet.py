from django_filters import rest_framework as filters  # type: ignore

from bodzify_api.filter.AppFilterSet import AppFilterSet
from bodzify_api.model.criteria.Criteria import Fields as CriteriaFields
from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist, Fields as ModelFields
from bodzify_api.model.criteria.CriteriaType import CriteriaTypesId


class Fields:
    NAME = ModelFields.NAME
    PARENT = ModelFields.PARENT


class GenrePlaylistFilterSet(AppFilterSet):
    name = filters.CharFilter(
        field_name=f'{ModelFields.CRITERIA}__{CriteriaFields.NAME}',
        lookup_expr="icontains"
    )
    parent = filters.UUIDFilter(
        field_name=f'{ModelFields.CRITERIA}__{CriteriaFields.PARENT}__{CriteriaFields.UUID}',
    )

    class Meta:
        model = CriteriaPlaylist
        fields = [Fields.NAME, Fields.PARENT]

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        return queryset.filter(type_id=CriteriaTypesId.GENRE).order_by(f'{ModelFields.CRITERIA}__{CriteriaFields.NAME}')
