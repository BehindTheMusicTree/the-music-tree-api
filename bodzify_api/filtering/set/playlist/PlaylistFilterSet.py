from django_filters import rest_framework as filters

from bodzify_api.filtering.filter.char.NonEmptiableCharFilter import NonEmptiableCharFilter
from bodzify_api.filtering.set.private_unique_resource.PrivateUniqueResourceFilterSet \
    import PrivateUniqueResourceFilterSet
from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.model.playlist.Fields import Fields as ModelFields
from bodzify_api.model.playlist.PlaylistTypesLabel import PlaylistTypesLabel
from bodzify_api.model.playlist.children.criteria.CriterialessPlaylistNames import CriterialessPlaylistNames
from bodzify_api.model.criteria.type.CriteriaTypePks import CriteriaTypePks
from .Fields import Fields


class PlaylistFilterSet(PrivateUniqueResourceFilterSet):
    name = NonEmptiableCharFilter()
    type_label = filters.CharFilter()

    class Meta:
        model = Playlist
        fields = [Fields.NAME, Fields.TYPE_LABEL]

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)

        name = self.data.get(Fields.NAME, '')
        type_label = self.data.get(Fields.TYPE_LABEL)

        manual_playlist_queryset = Playlist.objects.none()
        if type_label is None or type_label.lower() == PlaylistTypesLabel.MANUAL.lower():
            manual_playlist_queryset = queryset.filter(
                manual_playlist__isnull=False,
                manual_playlist__name__icontains=name
            )

        criteria_playlist_queryset = Playlist.objects.none()
        if type_label is None or type_label.lower() in [PlaylistTypesLabel.GENRE.lower(),
                                                        PlaylistTypesLabel.TAG.lower()]:
            criteria_playlist_queryset = queryset.filter(
                criteria_playlist__isnull=False,
                criteria_playlist__type__label__icontains=type_label.upper() if type_label else '',
                criteria_playlist__criteria__name__icontains=name
            )

        genreless_playlist = Playlist.objects.none()
        if (not name or name.lower() in CriterialessPlaylistNames.GENRE.lower()) \
                and type_label in [None, PlaylistTypesLabel.GENRE]:
            genreless_playlist = queryset.filter(
                criteria_playlist__isnull=False,
                criteria_playlist__criteria__isnull=True,
                criteria_playlist__type_id=CriteriaTypePks.GENRE
            )

        tagless_playlist = Playlist.objects.none()
        if (not name or name.lower() in CriterialessPlaylistNames.TAG.lower()) \
                and type_label in [None, PlaylistTypesLabel.TAG]:
            tagless_playlist = queryset.filter(
                criteria_playlist__isnull=False,
                criteria_playlist__criteria__isnull=True,
                criteria_playlist__type_id=CriteriaTypePks.TAG
            )

        return manual_playlist_queryset.union(criteria_playlist_queryset).union(genreless_playlist).union(
            tagless_playlist).order_by(ModelFields.CREATED_ON)
