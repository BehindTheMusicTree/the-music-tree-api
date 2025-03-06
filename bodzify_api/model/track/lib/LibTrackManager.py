
from typing import TYPE_CHECKING, Any

from django.db import transaction
from django.db.models import F, QuerySet
from django.utils import timezone

from bodzify_api.model.artist.Artist import Artist
from bodzify_api.model.criteria.type.CriteriaTypePks import CriteriaTypePks
from bodzify_api.model.playlist.Fields import Fields as PlayListFields
from bodzify_api.model.public_standard_resource.StandardResourceManager import StandardResourceManager
from bodzify_api.model.track.file.Fields import Fields as TrackFileFields
from bodzify_api.model.user.User import User
from bodzify_api.serializer.model.lib_track.input.schema.Fields import Fields as SchemaFields
from bodzify_api.utils import data_transformer

from .Fields import Fields


if TYPE_CHECKING:
    from bodzify_api.model.criteria.children.genre.Genre import Genre

    from .LibraryTrack import LibraryTrack


class LibTrackManager(StandardResourceManager['LibraryTrack']):
    model: type['LibraryTrack']

    def _remove_from_genre_playlists(self, instance: 'LibraryTrack', old_genre: 'Genre | None', genre_limit=None):
        from bodzify_api.model.lib_track_playlist_rel.LibTrackPlaylistRel import LibTrackPlaylistRel
        from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist

        update_date = timezone.now()
        if old_genre:
            old_genre_tree_item: Genre = old_genre
            while old_genre_tree_item != genre_limit:
                LibTrackPlaylistRel.objects.filter(
                    playlist=old_genre_tree_item.criteria_playlist, lib_track=instance).delete()
                old_genre_tree_item.criteria_playlist.last_track_list_update_date = update_date
                old_genre_tree_item.criteria_playlist.save(update_fields=[PlayListFields.LAST_TRACK_LIST_UPDATE_DATE])

                # The loop will stop before genre_tree_item is None
                old_genre_tree_item = old_genre_tree_item.parent  # type: ignore

        else:
            genreless_criteria_playlist: CriteriaPlaylist = \
                CriteriaPlaylist.objects.get(user=instance.user, type=CriteriaTypePks.GENRE, criteria=None)
            genreless_criteria_playlist.last_track_list_update_date = update_date
            genreless_criteria_playlist.save(update_fields=[PlayListFields.LAST_TRACK_LIST_UPDATE_DATE])
            LibTrackPlaylistRel.objects.filter(
                playlist=genreless_criteria_playlist, lib_track=instance).delete()

    def _add_to_genre_playlists(self, instance: 'LibraryTrack', genre_limit=None):
        from bodzify_api.model.lib_track_playlist_rel.LibTrackPlaylistRel import LibTrackPlaylistRel
        from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist

        update_date = timezone.now()
        if instance.genre:
            genre_tree_item: Genre = instance.genre
            while genre_tree_item != genre_limit:
                LibTrackPlaylistRel.objects.create(
                    user=instance.user, playlist=genre_tree_item.criteria_playlist, lib_track=instance)
                genre_tree_item.criteria_playlist.last_track_list_update_date = update_date
                genre_tree_item.criteria_playlist.save(update_fields=[PlayListFields.LAST_TRACK_LIST_UPDATE_DATE])

                # The loop will stop before genre_tree_item is None
                genre_tree_item = genre_tree_item.parent  # type: ignore
        else:
            genreless_criteria_playlist: CriteriaPlaylist = CriteriaPlaylist.objects.get(user=instance.user,
                                                                                         type=CriteriaTypePks.GENRE,
                                                                                         criteria=None)
            LibTrackPlaylistRel.objects.create(
                user=instance.user, playlist=genreless_criteria_playlist, lib_track=instance)
            genreless_criteria_playlist.last_track_list_update_date = update_date
            genreless_criteria_playlist.save(update_fields=[PlayListFields.LAST_TRACK_LIST_UPDATE_DATE])

    def _update_model_data_with_album_if_name_in_schema_data(self, model_data: dict, schema_data: dict):
        from bodzify_api.model.album.Album import Album
        if SchemaFields.ALBUM_NAME in schema_data:
            album_name = schema_data[SchemaFields.ALBUM_NAME]

            if not album_name:
                return None

            album_artists_names = []
            if SchemaFields.ALBUM_ARTISTS_NAMES in schema_data:
                album_artists_names = schema_data[SchemaFields.ALBUM_ARTISTS_NAMES]

            album = Album.objects.get_album_from_name_and_album_artists_names_after_potential_creations(
                user=schema_data[Fields.USER], name=album_name, album_artists_names=album_artists_names)

            model_data[Fields.ALBUM] = album

    def _update_model_data_with_artists_if_names_in_schema_data_otherwise_empty_list(
            self, model_data: dict, schema_data: dict) -> None:
        if SchemaFields.ARTISTS_NAMES in schema_data:
            artists_names = schema_data[SchemaFields.ARTISTS_NAMES]
            if artists_names:
                artists = Artist.objects.get_artists_list_from_names_after_potential_creation(
                    user=schema_data[Fields.USER], artists_names=artists_names)
            else:
                artists = []
        else:
            artists = []
        model_data[Fields.ARTISTS] = artists

    def _decrease_position_of_next_tracks_in_old_track_playlists(self, user: User, playlists_with_old_position: list):
        from bodzify_api.model.lib_track_playlist_rel.LibTrackPlaylistRel import Fields as LibTrackPlaylistRelFields
        from bodzify_api.model.lib_track_playlist_rel.LibTrackPlaylistRel import LibTrackPlaylistRel
        for playlist_uuid, old_position in playlists_with_old_position:
            lib_track_playlist_rels_to_update = LibTrackPlaylistRel.objects.filter(
                user=user, playlist=playlist_uuid, position__gt=old_position)
            lib_track_playlist_rels_to_update.update(position=F(LibTrackPlaylistRelFields.POSITION) - 1)

    def _update_genre_playlists(self, instance: 'LibraryTrack', old_genre: 'Genre | None'):
        from bodzify_api.model.criteria.children.genre.Genre import Genre
        common_genre = Genre.objects.get_common_ascendant(
            instance.genre, old_genre) if old_genre and instance.genre else None

        self._add_to_genre_playlists(instance=instance, genre_limit=common_genre)
        self._remove_from_genre_playlists(instance=instance, old_genre=old_genre, genre_limit=common_genre)

    def _get_model_data_from_input_schema_data(self, **kwargs) -> dict:
        model_data = dict()
        for key in [Fields.USER,
                    Fields.TITLE,
                    Fields.TRACK_NUMBER,
                    Fields.GENRE,
                    Fields.RATING,
                    Fields.LANGUAGE,
                    Fields.ARCHIVED]:
            data_transformer.update_dict1_with_key_if_set_in_dict2(key=key, dict1=model_data, dict2=kwargs)

        data_transformer.update_dict_converting_str_to_int_value_if_set(key=Fields.RATING, data_dict=kwargs)

        self._update_model_data_with_artists_if_names_in_schema_data_otherwise_empty_list(
            model_data=model_data, schema_data=kwargs)
        self._update_model_data_with_album_if_name_in_schema_data(model_data=model_data, schema_data=kwargs)

        return model_data

    def create(self, **kwargs) -> 'LibraryTrack':
        from ..file.TrackFile import TrackFile

        model_data = self._get_model_data_from_input_schema_data(**kwargs)

        artists = model_data.pop(Fields.ARTISTS, None)
        track_file_model_data = dict()
        track_file_model_data[TrackFileFields.FILE] = model_data.pop(Fields.TRACK_FILE)

        instance: LibraryTrack = super().create(**model_data)
        if artists:
            instance.artists.set(artists)

        track_file_model_data[TrackFileFields.USER] = instance.user
        track_file_model_data[TrackFileFields.LIB_TRACK] = instance

        TrackFile.objects.create(**track_file_model_data)

        self._add_to_genre_playlists(instance)
        instance.update_file_tags_from_lib_track_instance_values()
        return instance

    def create_instance_with_track_file(
            self, track_file_data: dict[str, Any], library_track_data: dict[str, Any]) -> 'LibraryTrack':
        from ..file.TrackFile import TrackFile

        with transaction.atomic():
            artists = library_track_data.pop(Fields.ARTISTS, None)
            lib_track: LibraryTrack = self.model(**library_track_data)
            lib_track.save()
            if artists:
                lib_track.artists.set(artists)

            track_file_data[TrackFileFields.LIB_TRACK] = lib_track
            TrackFile.objects.create(**track_file_data)

        lib_track.update_file_tags_from_lib_track_instance_values()

        return lib_track

    def update_instance(self, old_instance: 'LibraryTrack', **kwargs) -> 'LibraryTrack':
        from bodzify_api.model.album.Album import Album
        from bodzify_api.model.artist.Artist import Artist

        old_album_artists = []
        if old_instance.album:
            old_album_artists = old_instance.album.album_artists.all()
            old_album = old_instance.album
        else:
            old_album = None

        old_genre = old_instance.genre
        old_artists = old_instance.artists.all()

        model_data = self._get_model_data_from_input_schema_data(**kwargs)

        updated_instance: LibraryTrack = super().update_instance(old_instance, **model_data)

        if old_genre != updated_instance.genre:
            self._update_genre_playlists(updated_instance, old_genre=old_genre)

        if old_album and updated_instance.album and old_album != updated_instance.album:
            Album.objects.delete_instance_if_no_track_linked_with_potential_album_artist_deletion(old_album)
            for album_artist in old_album_artists:
                Artist.objects.delete_instance_if_nothing_linked(album_artist)

        if old_artists.count() > 0:
            current_track_artists_list = list(updated_instance.artists.all())
            old_track_artists_list: list[Artist] = list(old_artists)
            for old_track_artist in old_track_artists_list:
                if old_track_artist not in current_track_artists_list:
                    Artist.objects.delete_instance_if_nothing_linked(old_track_artist)

        return updated_instance

    def delete_instance(self, instance: 'LibraryTrack'):
        old_playlists_with_positions = instance.playlists_with_positions
        user = instance.user
        self.delete_instance_with_checking_album_and_artists_potential_deletion(instance)
        self._decrease_position_of_next_tracks_in_old_track_playlists(
            user=user, playlists_with_old_position=old_playlists_with_positions)

    def delete_instance_with_checking_album_and_artists_potential_deletion(self, instance: 'LibraryTrack'):
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

    def delete_with_checking_artists_potential_deletion(self, instance: 'LibraryTrack'):
        track_artists: QuerySet[Artist] = instance.artists.all()
        instance.delete()
        for artist in track_artists:
            Artist.objects.delete_instance_if_nothing_linked(artist)
