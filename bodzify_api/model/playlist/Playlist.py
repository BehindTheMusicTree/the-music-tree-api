from abc import abstractmethod
from typing import TYPE_CHECKING, cast

from django.db import models

from bodzify_api.model.lib_track_mixin.LibTrackMixin import LibTrackMixin
from bodzify_api.model.playlist.PlaylistManager import PlaylistManager
from bodzify_api.model.trackable_play_count.TrackablePlayCount import TrackablePlayCount

from .Fields import Fields


if TYPE_CHECKING:
    from bodzify_api.model.lib_track_playlist_rel.LibTrackPlaylistRel import LibTrackPlaylistRel
    from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack

    from .children.criteria.CriteriaPlaylist import CriteriaPlaylist
    from .children.manual.ManualPlaylist import ManualPlaylist


class Playlist(LibTrackMixin, TrackablePlayCount):

    objects: PlaylistManager = PlaylistManager()

    if TYPE_CHECKING:
        lib_track_playlist_rels: models.QuerySet['LibTrackPlaylistRel']
        manual_playlist: 'ManualPlaylist | None'
        criteria_playlist: 'CriteriaPlaylist | None'

    class Meta:
        verbose_name = 'Playlist'
        verbose_name_plural = 'Playlists'
        indexes = [models.Index(fields=[Fields.USER, Fields.UUID], name='playlist_user_uuid_idx')]

    def __str__(self) -> str:
        return f'{self.uuid} | {self.name}'

    @property
    def lib_tracks(self) -> models.QuerySet['LibraryTrack']:
        return getattr(self, Fields.LIB_TRACKS_RELATED_NAME)

    @property
    def type_label(self) -> str:
        if hasattr(self, Fields.MANUAL_PLAYLIST):
            if not self.manual_playlist:
                raise ValueError('Playlist has no manual playlist')
            return self.manual_playlist.type_label
        elif hasattr(self, Fields.CRITERIA_PLAYLIST):
            if not self.criteria_playlist:
                raise ValueError('Playlist has no criteria playlist')
            return self.criteria_playlist.type_label
        else:
            raise ValueError('Playlist has no type')

    @property
    def lib_tracks_not_archived_dict_by_position(self) -> dict[int | None, 'LibraryTrack']:
        """
        Returns a dictionary of LibraryTrack objects where dict[position] = lib_track.
        Includes both non-archived tracks (with position) and archived tracks (position is None).
        Archived tracks (null positions) are sorted last.
        Returns empty dict if no tracks.
        """
        return Playlist.get_ordered_relations_for_playlist(self)

    @classmethod
    def get_ordered_relations_for_playlist(cls, playlist: 'Playlist') -> dict[int | None, 'LibraryTrack']:
        """
        Returns a dictionary of LibraryTrack objects where dict[position] = lib_track.
        Includes both non-archived tracks (with position) and archived tracks (position is None).
        Archived tracks (null positions) are sorted last.
        Returns empty dict if no tracks.
        """
        from bodzify_api.model.lib_track_playlist_rel.LibTrackPlaylistRel import LibTrackPlaylistRel
        relations = LibTrackPlaylistRel.objects.get_ordered_relations_for_playlist(playlist)

        if not relations.exists():
            return {}

        result: dict[int | None, 'LibraryTrack'] = {}
        for relation in relations.filter(position__isnull=False):
            relation = cast(LibTrackPlaylistRel, relation)
            result[relation.position] = relation.lib_track
        for relation in relations.filter(position__isnull=True):
            relation = cast(LibTrackPlaylistRel, relation)
            result[len(result) + 1] = relation.lib_track

        return result

    @property
    @abstractmethod
    def name(self) -> str:
        if hasattr(self, Fields.MANUAL_PLAYLIST):
            if not self.manual_playlist:
                raise ValueError('Playlist has no manual playlist')
            return self.manual_playlist.name
        elif hasattr(self, Fields.CRITERIA_PLAYLIST):
            if not self.criteria_playlist:
                raise ValueError('Playlist has no criteria playlist')
            return self.criteria_playlist.name
        else:
            raise ValueError('Playlist has no name')
