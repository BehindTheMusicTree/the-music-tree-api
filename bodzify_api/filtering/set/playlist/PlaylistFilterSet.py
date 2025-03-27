from django.db.models.query import QuerySet

from bodzify_api.filtering.filter.char.NonEmptiableCharFilter import NonEmptiableCharFilter
from bodzify_api.filtering.filter.char.OptionalEnumCharFilter import OptionalEnumCharFilter
from bodzify_api.filtering.set.private_unique_resource.PrivateUniqueResourceFilterSet import (
    PrivateUniqueResourceFilterSet
)
from bodzify_api.model.criteria.type.CriteriaTypePks import CriteriaTypePks
from bodzify_api.model.playlist.children.criteria.CriterialessPlaylistNames import CriterialessPlaylistNames
from bodzify_api.model.playlist.Fields import Fields as ModelFields
from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.model.playlist.PlaylistTypesLabel import PlaylistTypesLabel

from .Fields import Fields


class PlaylistFilterSet(PrivateUniqueResourceFilterSet):
    name = NonEmptiableCharFilter(method='filter_by_name_and_type')
    type = OptionalEnumCharFilter(enum_class=PlaylistTypesLabel, method='filter_by_name_and_type')

    class Meta:
        model = Playlist
        fields = [
            Fields.NAME,
            Fields.TYPE_LABEL_PUBLIC,
            *PrivateUniqueResourceFilterSet.get_date_fields()
        ]

    def filter_by_name_and_type(self, queryset: QuerySet, name: str, value: str) -> QuerySet:
        name_value = self.data.get(Fields.NAME)
        type_label = self.data.get(Fields.TYPE_LABEL_PUBLIC)

        # Pre-filter the base queryset with common conditions
        base_queryset = queryset.order_by(ModelFields.CREATED_ON)

        result_querysets = []

        # Manual playlists
        if type_label is None or type_label.lower() == PlaylistTypesLabel.MANUAL.lower():
            manual_qs = base_queryset.filter(
                manual_playlist__isnull=False,
                manual_playlist__name__icontains=name_value if name == Fields.NAME else ''
            )
            result_querysets.append(manual_qs)

        # Criteria playlists (Genre and Tag)
        if type_label is None or type_label.lower() in [PlaylistTypesLabel.GENRE.lower(),
                                                        PlaylistTypesLabel.TAG.lower()]:
            criteria_qs = base_queryset.filter(
                criteria_playlist__isnull=False,
                criteria_playlist__type__label__icontains=type_label.upper() if type_label else '',
                criteria_playlist__criteria__name__icontains=name_value if name == Fields.NAME else ''
            )
            result_querysets.append(criteria_qs)

        # Genreless playlists
        if ((not name_value or name_value.lower() in CriterialessPlaylistNames.GENRE.lower()) and
                type_label in [None, PlaylistTypesLabel.GENRE]):
            genreless_qs = base_queryset.filter(
                criteria_playlist__isnull=False,
                criteria_playlist__criteria__isnull=True,
                criteria_playlist__type_id=CriteriaTypePks.GENRE
            )
            result_querysets.append(genreless_qs)

        # Tagless playlists
        if ((not name_value or name_value.lower() in CriterialessPlaylistNames.TAG.lower()) and
                type_label in [None, PlaylistTypesLabel.TAG]):
            tagless_qs = base_queryset.filter(
                criteria_playlist__isnull=False,
                criteria_playlist__criteria__isnull=True,
                criteria_playlist__type_id=CriteriaTypePks.TAG
            )
            result_querysets.append(tagless_qs)

        # Start with an empty queryset
        if not result_querysets:
            return Playlist.objects.none()

        # Combine all querysets using reduce and union
        from functools import reduce
        from operator import or_
        return reduce(or_, result_querysets)
