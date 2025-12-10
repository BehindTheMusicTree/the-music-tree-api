from typing import TYPE_CHECKING, Any, cast

from django.db.models import QuerySet

from api.model.criteria.type.CriteriaTypePks import CriteriaTypePks
from api.model.playlist.PlaylistTypesLabel import PlaylistTypesLabel
from api.model.public_standard_resource.StandardResourceManager import StandardResourceManager

from .children.criteria.CriterialessPlaylistNames import CriterialessPlaylistNames
from .Fields import Fields
from .PlaylistQuerySet import PlaylistQuerySet

if TYPE_CHECKING:
    from api.model.playlist.Playlist import Playlist
    from api.model.track.Track import Track


class PlaylistManager(StandardResourceManager):
    def get_queryset(self) -> PlaylistQuerySet:
        return cast(PlaylistQuerySet, PlaylistQuerySet(self.model, using=self._db))

    def filter(self, *args: Any, **kwargs: Any) -> QuerySet:
        type_filter = kwargs.pop(Fields.TYPE_LABEL_PUBLIC, None)
        name_filter = kwargs.pop(Fields.NAME_PUBLIC, None)

        queryset = super().filter(*args, **kwargs)

        if type_filter or name_filter:
            manual_playlist_queryset = self.none()
            if type_filter is None or type_filter.lower() == PlaylistTypesLabel.MANUAL.lower():
                manual_playlist_queryset = queryset.filter(
                    manual_playlist__isnull=False,
                    manual_playlist__name__icontains=name_filter
                )

            criteria_playlist_queryset = self.none()
            if type_filter is None or type_filter.lower() in [PlaylistTypesLabel.GENRE.lower(),
                                                              PlaylistTypesLabel.TAG.lower()]:
                criteria_playlist_queryset = queryset.filter(
                    criteria_playlist__isnull=False,
                    criteria_playlist__type__label__icontains=type_filter.upper() if type_filter else '',
                    criteria_playlist__criteria__name__icontains=name_filter
                )

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

            queryset = manual_playlist_queryset.union(
                criteria_playlist_queryset).union(
                genreless_playlist).union(tagless_playlist)

        return queryset

    def get_ordered_relations_for_playlist(self, playlist: 'Playlist') -> dict[int | None, 'Track']:
        """
        Returns a dictionary of Track objects where dict[position] = track.
        Includes both non-archived tracks (with position) and archived tracks (position is None).
        Archived tracks (null positions) are sorted last.
        Returns empty dict if no tracks.
        """
        from api.model.track_playlist_rel.TrackPlaylistRel import TrackPlaylistRel
        relations = TrackPlaylistRel.objects.get_ordered_relations_for_playlist(playlist)

        if not relations.exists():
            return {}

        result: dict[int | None, 'Track'] = {}
        for relation in relations.filter(position__isnull=False):
            relation = cast(TrackPlaylistRel, relation)
            result[relation.position] = relation.track
        for relation in relations.filter(position__isnull=True):
            relation = cast(TrackPlaylistRel, relation)
            result[len(result) + 1] = relation.track

        return result
