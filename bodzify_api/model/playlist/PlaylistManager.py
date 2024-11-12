from bodzify_api.model.criteria.type.CriteriaTypePks import CriteriaTypePks
from bodzify_api.model.playlist.PlaylistTypesLabel import PlaylistTypesLabel
from bodzify_api.model.public_standard_resource.PublicStandardResourceManager import PublicStandardResourceManager
from .PlaylistQuerySet import PlaylistQuerySet
from .children.criteria.CriterialessPlaylistNames import CriterialessPlaylistNames
from .Fields import Fields


class PlaylistManager(PublicStandardResourceManager):

    def get_queryset(self):
        return PlaylistQuerySet(self.model, using=self._db)

    def filter(self, *args, **kwargs):
        type_filter = kwargs.pop('type', None)
        name_filter = kwargs.pop('name', None) or self.get_queryset()._get_queryset_str_filter_value_to_filter_nothing()

        queryset = super().filter(*args, **kwargs)

        manual_playlist_queryset = self.none()
        if type_filter is None or type_filter.lower() == PlaylistTypesLabel.MANUAL.lower():
            manual_playlist_queryset = queryset.filter(manual_playlist__isnull=False,
                                                       manual_playlist__name__icontains=name_filter)

        criteria_playlist_queryset = self.none()
        if type_filter is None or type_filter.lower() in [PlaylistTypesLabel.GENRE.lower(),
                                                          PlaylistTypesLabel.TAG.lower()]:
            criteria_playlist_queryset = queryset.filter(
                criteria_playlist__isnull=False,
                criteria_playlist__type__label__icontains=type_filter.upper() if type_filter else '',
                criteria_playlist__criteria__name__icontains=name_filter)

        genreless_playlist = self.none()
        if (not name_filter or name_filter.lower() in CriterialessPlaylistNames.GENRE.lower()) \
                and type_filter in [None, PlaylistTypesLabel.GENRE]:
            genreless_playlist = queryset.filter(criteria_playlist__isnull=False,
                                                 criteria_playlist__criteria__isnull=True,
                                                 criteria_playlist__type_id=CriteriaTypePks.GENRE)

        tagless_playlist = self.none()
        if (not name_filter or name_filter.lower() in CriterialessPlaylistNames.TAG.lower()) \
                and type_filter in [None, PlaylistTypesLabel.TAG]:
            tagless_playlist = queryset.filter(criteria_playlist__isnull=False,
                                               criteria_playlist__criteria__isnull=True,
                                               criteria_playlist__type_id=CriteriaTypePks.TAG)

        return manual_playlist_queryset.union(criteria_playlist_queryset).union(genreless_playlist).union(
            tagless_playlist).order_by(Fields.CREATED_ON)
