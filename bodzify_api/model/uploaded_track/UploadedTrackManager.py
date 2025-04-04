from typing import TYPE_CHECKING, Any, cast

from django.db import transaction
from django.db.models import F, QuerySet
from django.utils import timezone

from bodzify_api.model.artist.Artist import Artist
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.criteria.type.CriteriaTypePks import CriteriaTypePks
from bodzify_api.model.public_standard_resource.StandardResourceManager import StandardResourceManager
from bodzify_api.model.track.file.Fields import Fields as TrackFileFields
from bodzify_api.model.user.User import User
from bodzify_api.serializer.model.uploaded_track.input.Fields import InputFields as InputFields

from .Fields import Fields


if TYPE_CHECKING:
    from bodzify_api.model.criteria.children.genre.Genre import Genre

    from .UploadedTrack import UploadedTrack


class LibTrackManager(StandardResourceManager['LibraryTrack']):
    model: type['UploadedTrack']

    def _remove_from_genre_playlists(self, instance: 'UploadedTrack', old_genre: 'Genre | None', genre_limit=None):
        from bodzify_api.model.uploaded_track_playlist_rel.LibTrackPlaylistRel import LibTrackPlaylistRel
        from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist

        update_date = timezone.now()
        if old_genre:
            old_genre_tree_item: Criteria | None = old_genre
            while old_genre_tree_item != genre_limit:
                old_genre_tree_item = cast(Criteria, old_genre_tree_item)  # Cannot be None at that point
                LibTrackPlaylistRel.objects.delete_instance(
                    user=instance.user, playlist=old_genre_tree_item.criteria_playlist, uploaded_track=instance)

                # The loop will stop before genre_tree_item is None
                old_genre_tree_item = old_genre_tree_item.parent

        else:
            genreless_criteria_playlist: CriteriaPlaylist = CriteriaPlaylist.objects.get(
                user=instance.user, type=CriteriaTypePks.GENRE, criteria=None)
            LibTrackPlaylistRel.objects.filter(
                playlist=genreless_criteria_playlist, uploaded_track=instance).delete()

    def _add_to_genre_playlists(self, instance: 'UploadedTrack', genre_limit=None):
        from bodzify_api.model.uploaded_track_playlist_rel.LibTrackPlaylistRel import LibTrackPlaylistRel
        from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist

        update_date = timezone.now()
        if instance.genre:
            genre_tree_item: Genre = instance.genre
            while genre_tree_item != genre_limit:
                LibTrackPlaylistRel.objects.create(
                    user=instance.user, playlist=genre_tree_item.criteria_playlist, uploaded_track=instance)

                # The loop will stop before genre_tree_item is None
                genre_tree_item = genre_tree_item.parent  # type: ignore
        else:
            genreless_criteria_playlist: CriteriaPlaylist = CriteriaPlaylist.objects.get(user=instance.user,
                                                                                         type=CriteriaTypePks.GENRE,
                                                                                         criteria=None)
            LibTrackPlaylistRel.objects.create(
                user=instance.user, playlist=genreless_criteria_playlist, uploaded_track=instance)

    def _decrease_position_of_next_tracks_in_old_track_playlists(self, user: User, playlists_with_old_position: list):
        from bodzify_api.model.uploaded_track_playlist_rel.LibTrackPlaylistRel import Fields as LibTrackPlaylistRelFields
        from bodzify_api.model.uploaded_track_playlist_rel.LibTrackPlaylistRel import LibTrackPlaylistRel
        for playlist_uuid, old_position in playlists_with_old_position:
            uploaded_track_playlist_rels_to_update = LibTrackPlaylistRel.objects.filter(
                user=user, playlist=playlist_uuid, position__gt=old_position)
            uploaded_track_playlist_rels_to_update.update(position=F(LibTrackPlaylistRelFields.POSITION) - 1)

    def _update_genre_playlists(self, instance: 'UploadedTrack', old_genre: 'Genre | None'):
        from bodzify_api.model.criteria.children.genre.Genre import Genre
        common_genre = Genre.objects.get_common_ascendant(
            instance.genre, old_genre) if old_genre and instance.genre else None

        self._add_to_genre_playlists(instance=instance, genre_limit=common_genre)
        self._remove_from_genre_playlists(instance=instance, old_genre=old_genre, genre_limit=common_genre)

    def create(self, **kwargs) -> 'UploadedTrack':
        from ..file.TrackFile import TrackFile

        with transaction.atomic():
            artists = kwargs.pop(Fields.ARTISTS, None)
            track_file_model_data = dict()
            track_file_model_data[TrackFileFields.FILE] = kwargs.pop(Fields.TRACK_FILE_INTERNAL)

            instance: UploadedTrack = super().create(**kwargs)
            if artists:
                instance.artists.set(artists)

            track_file_model_data[TrackFileFields.USER] = instance.user
            track_file_model_data[TrackFileFields.LIB_TRACK] = instance

            TrackFile.objects.create(**track_file_model_data)

            self._add_to_genre_playlists(instance)
            instance.update_file_metadata_from_uploaded_track_instance_values()
            return instance

    def create_instance_with_track_file(
            self, track_file_data: dict[str, Any], library_track_data: dict[str, Any]) -> 'UploadedTrack':
        from ..file.TrackFile import TrackFile

        with transaction.atomic():
            artists = library_track_data.pop(Fields.ARTISTS, None)
            uploaded_track: UploadedTrack = self.model(**library_track_data)
            uploaded_track.save()
            if artists:
                uploaded_track.artists.set(artists)

            track_file_data[TrackFileFields.LIB_TRACK] = uploaded_track
            TrackFile.objects.create(**track_file_data)

        uploaded_track.update_file_metadata_from_uploaded_track_instance_values()

        return uploaded_track

    def update_instance(self, old_instance: 'UploadedTrack', **kwargs) -> 'UploadedTrack':
        from bodzify_api.model.album.Album import Album
        from bodzify_api.model.artist.Artist import Artist
        from bodzify_api.model.uploaded_track_playlist_rel.LibTrackPlaylistRel import LibTrackPlaylistRel

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

            updated_instance: UploadedTrack = super().update_instance(old_instance, **kwargs)
            updated_instance.update_file_metadata_from_uploaded_track_instance_values()

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
                    LibTrackPlaylistRel.objects.archive_instances_of_uploaded_track(uploaded_track=updated_instance)
                else:
                    LibTrackPlaylistRel.objects.unarchive_instances_of_uploaded_track(uploaded_track=updated_instance)

            return updated_instance

    def delete_instance(self, instance: 'UploadedTrack'):
        with transaction.atomic():
            old_playlists_with_positions = instance.playlists_with_positions
            user = instance.user
            self.delete_instance_with_checking_album_and_artists_potential_deletion(instance)
            self._decrease_position_of_next_tracks_in_old_track_playlists(
                user=user, playlists_with_old_position=old_playlists_with_positions)

    def delete_instance_with_checking_album_and_artists_potential_deletion(self, instance: 'UploadedTrack'):
        from bodzify_api.model.album.Album import Album
        from bodzify_api.model.artist.Artist import Artist
        artists: list[Artist] = list(instance.artists.all())  # list() makes a copy of the QuerySet before the deletion
        album = instance.album

        # The order of the deletions is important for deletion rollback testing. Be carefull before changing it.
        instance.delete()

        if album:
            Album.objects.delete_instance_if_no_track_linked_with_potential_album_artist_deletion(album)
        for artist in artists:
            Artist.objects.delete_instance_if_nothing_linked(artist)

    def delete_with_checking_artists_potential_deletion(self, instance: 'UploadedTrack'):
        track_artists: QuerySet[Artist] = instance.artists.all()
        instance.delete()
        for artist in track_artists:
            Artist.objects.delete_instance_if_nothing_linked(artist)
