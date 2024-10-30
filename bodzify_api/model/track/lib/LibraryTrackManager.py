#!/usr/bin/env python

from typing import List, TYPE_CHECKING, Optional
from django.db import transaction
from django.utils import timezone
from bodzify_api.model.base.utils.public_standard_resource.PublicStandardResourceManager \
    import PublicStandardResourceManager
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.criteria.CriteriaType import CriteriaTypesId
from bodzify_api.model.playlist.BasePlaylist import BasePlaylist
from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.model.track.lib.Fields import Fields as ModelFields
from bodzify_api.model.Artist import Artist


if TYPE_CHECKING:
    from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack


class LibraryTrackManager(PublicStandardResourceManager['LibraryTrack']):
    model: type['LibraryTrack']

    def _remove_track_from_old_genre_ascendants_playlists_until_genre_limit(self,
                                                                            instance: 'LibraryTrack',
                                                                            old_genre: Optional[Criteria],
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

    def create_with_track_file(self, track_file_data, library_track_data: dict):
        from bodzify_api.model.track.file.TrackFile import TrackFile, Fields as TrackFileFields

        with transaction.atomic():
            artists = library_track_data.pop(ModelFields.ARTISTS, None)
            library_track: LibraryTrack = self.model(**library_track_data)
            library_track.save()
            if artists:
                library_track.artists.set(artists)

            track_file_data[TrackFileFields.LIBRARY_TRACK] = library_track
            TrackFile.objects.create(**track_file_data)

        library_track.update_file_tags_from_lib_track_instance_values()

        return library_track

    def update_genre_playlists(self, instance: 'LibraryTrack', old_genre: Optional[Criteria]):
        if old_genre and instance.genre:
            common_genre = Criteria.get_common_criteria(instance.genre, old_genre)
        else:
            common_genre = None

        self._add_track_to_genre_playlists_until_genre_limit(instance, genre_limit=common_genre)
        self._remove_track_from_old_genre_ascendants_playlists_until_genre_limit(
            instance, old_genre=old_genre, genre_limit=common_genre)

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
