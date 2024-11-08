from typing import List, TYPE_CHECKING, Optional

from django.db import transaction
from django.utils import timezone

from bodzify_api.model.public_standard_resource.PublicStandardResourceManager \
    import PublicStandardResourceManager
from bodzify_api.model.criteria.type.CriteriaTypePks import CriteriaTypesPks
from bodzify_api.model.playlist.BasePlaylist import BasePlaylist
from bodzify_api.model.artist.Artist import Artist
from bodzify_api.model.playlist.children.criteria.CriteriaPlaylistManager import CriteriaPlaylistManager
from .Fields import Fields as ModelFields


if TYPE_CHECKING:
    from bodzify_api.model.criteria.children.genre.Genre import Genre
    from .LibraryTrack import LibraryTrack


class LibraryTrackManager(PublicStandardResourceManager['LibraryTrack']):
    model: type['LibraryTrack']

    def _remove_from_genre_playlists(self, instance: 'LibraryTrack', old_genre: Optional['Genre'], genre_limit=None):
        from bodzify_api.model.lib_track_playlist_rel.LibTrackPlaylistRel import LibTrackPlaylistRel
        from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist

        update_date = timezone.now()
        if old_genre:
            old_genre_tree_item = old_genre
            while old_genre_tree_item != genre_limit:
                LibTrackPlaylistRel.objects.filter(base_playlist=old_genre_tree_item.criteria_playlist,
                                                   library_track=instance).delete()
                old_genre_tree_item.criteria_playlist.last_track_list_update_date = update_date
                old_genre_tree_item.criteria_playlist.save()
                if old_genre_tree_item.parent:
                    old_genre_tree_item = old_genre_tree_item.parent
        else:
            genreless_criteria_playlist: CriteriaPlaylist = \
                CriteriaPlaylist.objects.get(user=instance.user, type=CriteriaTypesPks.GENRE, criteria=None)
            genreless_criteria_playlist.last_track_list_update_date = update_date
            genreless_criteria_playlist.save()
            LibTrackPlaylistRel.objects.filter(
                base_playlist=genreless_criteria_playlist, library_track=instance).delete()

    def _add_to_genre_playlists(self, instance: 'LibraryTrack', genre_limit=None):
        from bodzify_api.model.lib_track_playlist_rel.LibTrackPlaylistRel import LibTrackPlaylistRel
        from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist

        update_date = timezone.now()
        if instance.genre:
            genre_tree_item: Genre = instance.genre
            while genre_tree_item != genre_limit:
                criteria_playlist: CriteriaPlaylist = CriteriaPlaylist.objects.get(user=instance.user,
                                                                                   criteria=genre_tree_item)
                LibTrackPlaylistRel.objects.create(user=instance.user,
                                                   base_playlist=criteria_playlist,
                                                   library_track=instance)
                CriteriaPlaylist.objects.update_single(instance=criteria_playlist,
                                                       last_track_list_update_date=update_date)

                # The loop will stop before genre_tree_item is None
                genre_tree_item = genre_tree_item.parent  # type: ignore
        else:
            genreless_criteria_playlist = CriteriaPlaylist.objects.get(user=instance.user,
                                                                       type=CriteriaTypesPks.GENRE,
                                                                       criteria=None)
            LibTrackPlaylistRel.objects.create(user=instance.user,
                                               base_playlist=genreless_criteria_playlist,
                                               library_track=instance)
            CriteriaPlaylist.objects.update_single(instance=genreless_criteria_playlist,
                                                   last_track_list_update_date=update_date)

    def update_genre_playlists(self, instance: 'LibraryTrack', old_genre: Optional['Genre']):
        common_genre = \
            Genre.objects.get_common_ascendant(instance.genre, old_genre) if old_genre and instance.genre else None

        self._add_to_genre_playlists(instance, genre_limit=common_genre)
        self._remove_from_genre_playlists(
            instance, old_genre=old_genre, genre_limit=common_genre)

    def create_single_with_track_file(self, track_file_data, library_track_data: dict):
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

    def save(self, instance: 'LibraryTrack', *args, **kwargs):
        try:
            old_track: LibraryTrack = self.get(user=instance.user, uuid=instance.uuid)
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
            self._add_to_genre_playlists(instance)
