#!/usr/bin/env python

from typing import List, TYPE_CHECKING, Optional
from django.db import models, transaction
from django.utils import timezone
from django.db.models import Q

from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.criteria.CriteriaType import CriteriaTypesId
from bodzify_api.model.playlist.BasePlaylist import BasePlaylist
from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.model.track.lib.Fields import Fields as LibTrackFields
from bodzify_api.model.Artist import Artist
from bodzify_api.utils.audio_metadata.MetadataManager import METADATA_ARTISTS_SEPARATION_CHAR
from bodzify_api.utils.audio_metadata.NormalizedMetadataKeys import NormalizedMetadataKeys

if TYPE_CHECKING:
    from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack
    from bodzify_api.model.track.file.TrackFile import TrackFile, Fields as TrackFileFields


class LibraryTrackManager(models.Manager['LibraryTrack']):
    model: type['LibraryTrack']

    def create_with_track_file(self, track_file_data, library_track_data: dict):
        with transaction.atomic():
            artists = library_track_data.pop(LibTrackFields.ARTISTS, None)
            library_track: LibraryTrack = self.model(**library_track_data)
            library_track.save()
            if artists:
                library_track.artists.set(artists)

            track_file_data[TrackFileFields.LIBRARY_TRACK] = library_track
            TrackFile.objects.create(**track_file_data)

            return library_track

    def get_sorted_tracks(self, queryset):
        return queryset.annotate(
            null_position=Q(position_in_album__isnull=True)
        ).order_by('null_position', 'position_in_album', 'title')

    def update_genre_playlists(self, instance: 'LibraryTrack', old_genre: Optional[Criteria]):
        if old_genre and instance.genre:
            common_genre = Criteria.get_common_criteria(instance.genre, old_genre)
        else:
            common_genre = None

        self._add_track_to_genre_playlists_until_genre_limit(instance, genre_limit=common_genre)
        self._remove_track_from_old_genre_ascendants_playlists_until_genre_limit(
            instance, old_genre=old_genre, genre_limit=common_genre)

    def _remove_track_from_old_genre_ascendants_playlists_until_genre_limit(
            self, instance: 'LibraryTrack', old_genre: Optional[Criteria],
            genre_limit=None):
        from bodzify_api.model.LibTrackPlaylistPositionRel import LibTrackPlaylistPositionRel

        update_date = timezone.now()
        if old_genre:
            old_genre_tree_item = old_genre
            while old_genre_tree_item != genre_limit:
                genreless_criteria_playlist = CriteriaPlaylist.objects.get(
                    user=instance.user, criteria=old_genre_tree_item)
                base_playlist: BasePlaylist = genreless_criteria_playlist.base_playlist
                LibTrackPlaylistPositionRel.objects.get(base_playlist=base_playlist, library_track=instance).delete()
                base_playlist.last_track_list_update_date = update_date
                base_playlist.save()
                if old_genre_tree_item.parent:
                    old_genre_tree_item = old_genre_tree_item.parent
        else:
            genreless_criteria_playlist = CriteriaPlaylist.objects.get(
                user=instance.user,
                type_id=CriteriaTypesId.GENRE,
                criteria=None
            )
            base_playlist = genreless_criteria_playlist.base_playlist
            base_playlist.last_track_list_update_date = update_date
            base_playlist.save()
            LibTrackPlaylistPositionRel.objects.get(base_playlist=base_playlist, library_track=instance).delete()

    def _add_track_to_genre_playlists_until_genre_limit(self, instance: 'LibraryTrack', genre_limit=None):
        from bodzify_api.model.LibTrackPlaylistPositionRel import LibTrackPlaylistPositionRel

        update_date = timezone.now()
        if instance.genre:
            genre_tree_item: Criteria = instance.genre
            while genre_tree_item != genre_limit:
                criteria_playlist = CriteriaPlaylist.objects.get(user=instance.user, criteria=genre_tree_item)
                base_playlist: BasePlaylist = criteria_playlist.base_playlist
                LibTrackPlaylistPositionRel.objects.create(
                    user=instance.user,
                    base_playlist=criteria_playlist.base_playlist,
                    library_track=instance
                )
                base_playlist.last_track_list_update_date = update_date
                base_playlist.save()

                # The loop will stop before genre_tree_item is None
                genre_tree_item = genre_tree_item.parent  # type: ignore
        else:
            genreless_criteria_playlist = CriteriaPlaylist.objects.get(
                user=instance.user,
                type_id=CriteriaTypesId.GENRE,
                criteria=None
            )
            base_playlist: BasePlaylist = genreless_criteria_playlist.base_playlist
            LibTrackPlaylistPositionRel.objects.create(
                user=instance.user,
                base_playlist=base_playlist,
                library_track=instance
            )
            base_playlist.last_track_list_update_date = update_date
            base_playlist.save()

    def get_lib_track_playlists_with_positions(self, instance: 'LibraryTrack') -> list:
        from bodzify_api.model.LibTrackPlaylistPositionRel import LibTrackPlaylistPositionRel, \
            Fields as LibTrackPlaylistPositionRelFields
        lib_track_position_relations = LibTrackPlaylistPositionRel.objects.filter(
            user=instance.user,
            library_track=instance
        )
        return list(lib_track_position_relations.values_list(
            LibTrackPlaylistPositionRelFields.BASE_PLAYLIST + '__uuid',
            LibTrackPlaylistPositionRelFields.POSITION
        ))

    def update_file_tags(self, instance: 'LibraryTrack'):
        normalized_metadata = dict()
        normalized_metadata[NormalizedMetadataKeys.TITLE] = instance.title

        if instance.artists.count() > 0:
            artists_names_tag = ""
            artists_list: list[Artist] = list(instance.artists.all())
            for artist in artists_list:
                if artists_names_tag != "":
                    artists_names_tag = artists_names_tag + METADATA_ARTISTS_SEPARATION_CHAR
                artists_names_tag = artists_names_tag + artist.name
        else:
            artists_names_tag = ""
        normalized_metadata[NormalizedMetadataKeys.ARTISTS_NAMES] = artists_names_tag

        album_artists_tag = ""
        if instance.album:
            album_name_tag = instance.album.name
            album_artists_name_index = 0
            album_artists_list: list[Artist] = list(instance.album.album_artists.all())
            for album_artist in album_artists_list:
                if album_artists_name_index != 0:
                    album_artists_tag = album_artists_tag + METADATA_ARTISTS_SEPARATION_CHAR
                album_artists_tag = album_artists_tag + album_artist.name
                album_artists_name_index = album_artists_name_index + 1
        else:
            album_name_tag = ""

        normalized_metadata[NormalizedMetadataKeys.ALBUM_NAME] = album_name_tag
        normalized_metadata[NormalizedMetadataKeys.ALBUM_ARTISTS_NAMES] = album_artists_tag
        normalized_metadata[NormalizedMetadataKeys.GENRE_NAME] = instance.genre.name if instance.genre else ""
        normalized_metadata[NormalizedMetadataKeys.RATING] = instance.rating
        normalized_metadata[NormalizedMetadataKeys.LANGUAGE] = instance.language if instance.language else ""

        instance.track_file.update_file_tags(normalized_metadata=normalized_metadata)

    def save(self, instance: 'LibraryTrack', *args, **kwargs):
        try:
            old_track = self.get(user=instance.user, uuid=instance.uuid)
            old_album_artists_list: List[Artist] = []
            if old_track.album:
                old_album_artists_list = list(old_track.album.album_artists.all())
                old_album = old_track.album
            else:
                old_album = None

            instance.save(*args, **kwargs)

            if old_track.genre != instance.genre:
                self.update_genre_playlists(instance, old_genre=old_track.genre)

            if old_track.album and instance.album and old_album != instance.album:
                old_track.album.delete_if_no_track_linked_with_eventual_album_artist_deletion()
                for album_artist in old_album_artists_list:
                    album_artist.delete_if_nothing_linked()

            if old_track.artists.count() > 0:
                current_track_artists_list = list(instance.artists.all())
                old_track_artists_list: list[Artist] = list(old_track.artists.all())
                for old_track_artist in old_track_artists_list:
                    if old_track_artist not in current_track_artists_list:
                        old_track_artist.delete_if_nothing_linked()

        except self.model.DoesNotExist:
            instance.save(*args, **kwargs)
            self._add_track_to_genre_playlists_until_genre_limit(instance)

    def handle_pre_delete(self, instance: 'LibraryTrack'):
        now = timezone.now()
        base_playlists: List[BasePlaylist] = list(instance.base_playlists.all())
        for base_playlist in base_playlists:
            base_playlist.last_track_list_update_date = now
            base_playlist.save()
