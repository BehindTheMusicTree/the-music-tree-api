from typing import TYPE_CHECKING, Any, cast

from django.db import transaction
from django.db.models import F, QuerySet
from django.utils import timezone

from api.model.artist.Artist import Artist
from api.model.criteria.Criteria import Criteria
from api.model.criteria.type.CriteriaTypePks import CriteriaTypePks
from api.model.public_standard_resource.StandardResourceManager import StandardResourceManager
from api.model.user.User import User
from api.serializer.model.track.input.Fields import Fields as Fields

from .Fields import Fields


if TYPE_CHECKING:
    from api.model.criteria.children.genre.Genre import Genre

    from .Track import Track


class TrackManager(StandardResourceManager['Track']):
    model: type['Track']

    def _remove_from_genre_playlists(self, instance: 'Track', old_genre: 'Genre | None', genre_limit=None):
        from api.model.track_playlist_rel.TrackPlaylistRel import TrackPlaylistRel
        from api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist

        update_date = timezone.now()
        if old_genre:
            old_genre_tree_item: Criteria | None = old_genre
            while old_genre_tree_item != genre_limit:
                old_genre_tree_item = cast(Criteria, old_genre_tree_item)  # Cannot be None at that point
                TrackPlaylistRel.objects.delete_instance(
                    user=instance.user, playlist=old_genre_tree_item.criteria_playlist, track=instance)

                # The loop will stop before genre_tree_item is None
                old_genre_tree_item = old_genre_tree_item.parent

        else:
            genreless_criteria_playlist: CriteriaPlaylist = CriteriaPlaylist.objects.get(
                user=instance.user, type=CriteriaTypePks.GENRE, criteria=None)
            TrackPlaylistRel.objects.filter(
                playlist=genreless_criteria_playlist, track=instance).delete()

    def _add_to_genre_playlists(self, instance: 'Track', genre_limit=None):
        from api.model.track_playlist_rel.TrackPlaylistRel import TrackPlaylistRel
        from api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist

        update_date = timezone.now()
        if instance.genre:
            genre_tree_item: Genre = instance.genre
            while genre_tree_item != genre_limit:
                TrackPlaylistRel.objects.create(
                    user=instance.user, playlist=genre_tree_item.criteria_playlist, track=instance)

                # The loop will stop before genre_tree_item is None
                genre_tree_item = genre_tree_item.parent  # type: ignore
        else:
            genreless_criteria_playlist: CriteriaPlaylist = CriteriaPlaylist.objects.get(user=instance.user,
                                                                                         type=CriteriaTypePks.GENRE,
                                                                                         criteria=None)
            TrackPlaylistRel.objects.create(
                user=instance.user, playlist=genreless_criteria_playlist, track=instance)

    def _decrease_position_of_next_tracks_in_old_track_playlists(self, user: User, playlists_with_old_position: list):
        from api.model.track_playlist_rel.TrackPlaylistRel import Fields as TrackPlaylistRelFields
        from api.model.track_playlist_rel.TrackPlaylistRel import TrackPlaylistRel
        for playlist_uuid, old_position in playlists_with_old_position:
            track_playlist_rels_to_update = TrackPlaylistRel.objects.filter(
                user=user, playlist=playlist_uuid, position__gt=old_position)
            track_playlist_rels_to_update.update(position=F(TrackPlaylistRelFields.POSITION) - 1)

    def _update_genre_playlists(self, instance: 'Track', old_genre: 'Genre | None'):
        from api.model.criteria.children.genre.Genre import Genre
        common_genre = Genre.objects.get_common_ascendant(
            instance.genre, old_genre) if old_genre and instance.genre else None

        self._add_to_genre_playlists(instance=instance, genre_limit=common_genre)
        self._remove_from_genre_playlists(instance=instance, old_genre=old_genre, genre_limit=common_genre)

    def create(self, **kwargs) -> 'Track':
        with transaction.atomic():
            artists = kwargs.pop(Fields.ARTISTS, None)
            file = kwargs.pop(Fields.TRACK_FILE_INTERNAL, None)
            if file:
                kwargs[Fields.FILE] = file

            instance: Track = super().create(**kwargs)
            if artists:
                instance.artists.set(artists)

            self._add_to_genre_playlists(instance)

        return instance

    def create_instance_with_track_file(
            self, track_file_data: dict[str, Any], track_data: dict[str, Any]) -> 'Track':
        with transaction.atomic():
            artists = track_data.pop(Fields.ARTISTS, None)
            if 'file' in track_file_data:
                track_data[Fields.FILE] = track_file_data.pop('file')

            track: Track = self.model(**track_data)
            track.save()
            if artists:
                track.artists.set(artists)

        return track

    def update_instance(self, old_instance: 'Track', **kwargs) -> 'Track':
        from api.model.album.Album import Album
        from api.model.artist.Artist import Artist
        from api.model.track_playlist_rel.TrackPlaylistRel import TrackPlaylistRel

        with transaction.atomic():
            old_album_artists_list = []
            if old_instance.album:

                # list() makes a copy of the QuerySet before the deletion
                old_album_artists_list = list(old_instance.album.album_artists.all())
                old_album = old_instance.album
            else:
                old_album = None

            old_genre = old_instance.genre
            # list() makes a copy of the QuerySet before the deletion
            old_artists_list = list(old_instance.artists.all())

            old_archived_state = old_instance.archived

            updated_instance: Track = super().update_instance(old_instance, **kwargs)

            if old_genre != updated_instance.genre:
                self._update_genre_playlists(updated_instance, old_genre=old_genre)

            if old_album and updated_instance.album and old_album != updated_instance.album:
                Album.objects.delete_instance_if_no_track_linked_with_potential_album_artist_deletion(old_album)
                for album_artist in old_album_artists_list:
                    Artist.objects.delete_instance_if_nothing_linked(album_artist)

            if len(old_artists_list) > 0:
                current_track_artists_list = list(updated_instance.artists.all())
                old_track_artists_list: list[Artist] = list(old_artists_list)
                for old_track_artist in old_track_artists_list:
                    if old_track_artist not in current_track_artists_list:
                        Artist.objects.delete_instance_if_nothing_linked(old_track_artist)

            if old_archived_state != updated_instance.archived:
                if updated_instance.archived:
                    TrackPlaylistRel.objects.archive_instances_of_track(
                        track=updated_instance)
                else:
                    TrackPlaylistRel.objects.unarchive_instances_of_track(
                        track=updated_instance)

            return updated_instance

    def delete_instance(self, instance: 'Track'):
        with transaction.atomic():
            old_playlists_with_positions = instance.playlists_with_positions
            user = instance.user
            self.delete_instance_with_checking_album_and_artists_potential_deletion(instance)
            self._decrease_position_of_next_tracks_in_old_track_playlists(
                user=user, playlists_with_old_position=old_playlists_with_positions)

    def delete_instance_with_checking_album_and_artists_potential_deletion(self, instance: 'Track'):
        from api.model.album.Album import Album
        from api.model.artist.Artist import Artist
        artists: list[Artist] = list(instance.artists.all())  # list() makes a copy of the QuerySet before the deletion
        album = instance.album

        # The order of the deletions is important for deletion rollback testing. Be carefull before changing it.
        instance.delete()

        if album:
            Album.objects.delete_instance_if_no_track_linked_with_potential_album_artist_deletion(album)
        for artist in artists:
            Artist.objects.delete_instance_if_nothing_linked(artist)

    def delete_with_checking_artists_potential_deletion(self, instance: 'Track'):
        track_artists: QuerySet[Artist] = instance.artists.all()
        instance.delete()
        for artist in track_artists:
            Artist.objects.delete_instance_if_nothing_linked(artist)
