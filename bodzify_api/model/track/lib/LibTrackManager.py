
import os
import tempfile
from typing import TYPE_CHECKING, Any

import requests
from django.core.files.base import File as DjangoFile
from django.db import transaction
from django.db.models import F, QuerySet
from django.utils import timezone

from bodzify_api import settings
from bodzify_api.exception.validation.app.AppValidationException import AppValidationException
from bodzify_api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.model.artist.Artist import Artist
from bodzify_api.model.criteria.type.CriteriaTypePks import CriteriaTypePks
from bodzify_api.model.playlist.Fields import Fields as PlayListFields
from bodzify_api.model.public_standard_resource.StandardResourceManager import StandardResourceManager
from bodzify_api.model.track.file.Fields import Fields as TrackFileFields
from bodzify_api.model.user.User import User
from bodzify_api.serializer.model.lib_track.input.extract.Fields import Fields as ExtractFields
from bodzify_api.serializer.model.lib_track.input.post.Fields import Fields as PostFields
from bodzify_api.serializer.model.lib_track.input.schema.Fields import Fields as SchemaFields
from bodzify_api.utils import audio_metadata, data_transformer, utils
from bodzify_api.utils.AppDjangoFIle import AppDjangoFile
from bodzify_api.utils.audio_metadata.exceptions import FileCorruptedError
from bodzify_api.utils.audio_metadata.utils.AppMetadataKey import AppMetadataKey
from bodzify_api.utils.AudioFile import AudioFile
from bodzify_api.view.viewset.model.lib_track.LibTrackCreationType import LibTrackCreationType

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

    def _get_generated_title_from_data(self, file: DjangoFile, data: dict):
        filename = os.path.basename(file.name).rsplit('.', 1)[0]
        filename_without_expressions_to_exclude = data_transformer.remove_substrings_from_string(
            string_a=filename, substrings=settings.LIB_TRACK_FILENAME_EXPRESSIONS_TO_EXCLUDE_GENERATING_TITLE)
        if SchemaFields.FORCE_TITLE_GENERATION in data:
            force_title_generation = data[SchemaFields.FORCE_TITLE_GENERATION]
        else:
            force_title_generation = False

        if len(filename_without_expressions_to_exclude) > settings.LIB_TRACK_FILENAME_LEN_MAX or force_title_generation:
            title = settings.LIB_TRACK_GENERATED_TITLE_PREFIXE + \
                utils.generate_short_uu(
                    settings.LIB_TRACK_GENERATED_TITLE_LENGTH - len(settings.LIB_TRACK_GENERATED_TITLE_PREFIXE))
        else:
            title = filename_without_expressions_to_exclude
        return title

    def _update_model_data_with_genre_if_in_schema_data(self, model_data: dict, schema_data: dict):
        from bodzify_api.model.criteria.children.genre.Genre import Genre

        if SchemaFields.GENRE_UUID in schema_data:
            genre = schema_data[SchemaFields.GENRE_UUID]
        elif SchemaFields.GENRE_NAME in schema_data:
            genre_name = schema_data[SchemaFields.GENRE_NAME]
            genre = None if not genre_name else Genre.objects.get_or_create(
                name=genre_name,
                user=schema_data[Fields.USER]
            )[0]
        else:
            return

        model_data[Fields.GENRE] = genre

    def _get_schema_data_from_file(self, file):
        try:
            normalized_metadata = audio_metadata.get_merged_normalized_metadata(
                file=file, normalized_rating_max_value=settings.LIB_TRACK_RATING_VALUE_MAX)
        except FileCorruptedError as exc:
            raise AppValidationException(
                field_name=Fields.TRACK_FILE_PUBLIC,
                message=str(exc),
                field_validation_error_code=FieldValidationErrorCode.FILE_CORRUPTED)

        schema_data_with_potential_none = data_transformer.get_copy_of_dict_including_only_specified_keys(
            data_dict=normalized_metadata,
            keys=[AppMetadataKey.TITLE,
                  AppMetadataKey.ALBUM_NAME,
                  AppMetadataKey.GENRE_NAME,
                  AppMetadataKey.RATING,
                  AppMetadataKey.LANGUAGE])

        for artists_names_keys in [
            [AppMetadataKey.ARTISTS_NAMES_STR, SchemaFields.ARTISTS_NAMES],
            [AppMetadataKey.ALBUM_ARTISTS_NAMES_STR, SchemaFields.ALBUM_ARTISTS_NAMES]
        ]:
            app_metadata_key, schema_key = artists_names_keys
            if app_metadata_key in normalized_metadata:
                artists_names_str: str = normalized_metadata[app_metadata_key]  # type: ignore
                if artists_names_str is not None and artists_names_str != "":
                    artists_names_list = \
                        Artist.objects.get_artists_names_list_from_metadata_str(names_str=artists_names_str)
                    schema_data_with_potential_none[schema_key] = artists_names_list

        schema_data_clean = data_transformer.remove_none_or_empty_key_from_dict(schema_data_with_potential_none)
        schema_data_clean[SchemaFields.TRACK_FILE_PUBLIC] = file

        return schema_data_clean

    def _update_model_data_with_album_if_name_in_schema_data(self, model_data: dict, schema_data: dict):
        from bodzify_api.model.album.Album import Album
        if SchemaFields.ALBUM_NAME in schema_data:
            album_name = schema_data[SchemaFields.ALBUM_NAME]

            if not album_name:
                return None

            album_artists_names_list = []
            if SchemaFields.ALBUM_ARTISTS_NAMES in schema_data:
                album_artists_names_list = schema_data[SchemaFields.ALBUM_ARTISTS_NAMES]

            album = Album.objects.get_album_from_name_and_album_artists_names_list_after_eventual_creations(
                user=schema_data[Fields.USER],
                name=album_name,
                album_artists_names_list=album_artists_names_list)

            model_data[Fields.ALBUM] = album

    def _update_model_data_with_artists_if_names_in_schema_data_otherwise_empty_list(
            self, model_data: dict, schema_data: dict) -> None:
        if SchemaFields.ARTISTS_NAMES in schema_data:
            artists_names_list = schema_data[SchemaFields.ARTISTS_NAMES]
            if artists_names_list:
                artists = Artist.objects.get_artists_list_from_names_after_eventual_creation(
                    user=schema_data[Fields.USER],
                    artists_names_list=artists_names_list)
            else:
                artists = []
        else:
            artists = []
        model_data[Fields.ARTISTS] = artists

    def _get_track_filename_with_extension(self, mine_track_url: str, data: dict):
        file_extension = utils.get_file_extension_from_url(mine_track_url)
        is_filename_randomly_generated = False
        if Fields.TITLE in data:
            title = data[Fields.TITLE]
            if SchemaFields.ARTISTS_NAMES in data:
                artists_names_list = data[SchemaFields.ARTISTS_NAMES]
                artists_names = ", ".join(artists_names_list)
                if artists_names is None or artists_names == "":
                    filename_without_extension = title
                else:
                    filename_without_extension = artists_names + " - " + title
            else:
                filename_without_extension = title
            filename_with_extension = filename_without_extension + "." + file_extension
        else:
            filename_with_extension = utils.get_substring_after_last_slash(mine_track_url)
            if len(filename_with_extension) > settings.LIB_TRACK_FILENAME_LEN_MAX:
                filename_without_extension = utils.generate_short_uu(
                    settings.LIB_TRACK_FILENAME_GENERATED_WITHOUT_EXTENSION_LENGTH - len(file_extension) - 1)
                filename_with_extension = filename_without_extension + "." + file_extension
                is_filename_randomly_generated = True
        return filename_with_extension, is_filename_randomly_generated

    def _get_model_data_from_post_and_extract_common_schema_data(self, schema_data: dict[str, str]) -> dict:
        model_data = dict()

        for key in [Fields.USER,
                    Fields.TRACK_FILE_FINGERPRINT_MUST_BE_UNIQUE,
                    Fields.TRACK_FILE,
                    Fields.TITLE,
                    Fields.RATING,
                    Fields.LANGUAGE,
                    Fields.ARCHIVED,
                    Fields.TRACK_NUMBER]:
            data_transformer.update_dict1_with_key_if_set_in_dict2(key=key, dict1=model_data, dict=schema_data)

        self._update_model_data_with_artists_if_names_in_schema_data_otherwise_empty_list(
            model_data=model_data, schema_data=schema_data)
        self._update_model_data_with_album_if_name_in_schema_data(model_data=model_data, schema_data=schema_data)
        self._update_model_data_with_genre_if_in_schema_data(model_data=model_data, schema_data=schema_data)

        return model_data

    def _get_schema_data_from_update_data(self, update_data: dict) -> dict:
        schema_data = update_data.copy()
        data_transformer.update_dict_converting_str_to_int_value_if_set(key=Fields.RATING, data_dict=schema_data)
        return schema_data

    def _get_schema_data_from_post_data(self, post_data: dict[str, Any]) -> dict[str, Any]:
        file = post_data[PostFields.TRACK_FILE_PUBLIC]
        schema_data_from_file = self._get_schema_data_from_file(file=file)

        schema_data = schema_data_from_file.copy()
        keys = [Fields.USER,
                SchemaFields.TRACK_FILE_PUBLIC,
                SchemaFields.TRACK_FILE_FINGERPRINT_MUST_BE_UNIQUE,
                SchemaFields.TITLE,
                SchemaFields.ALBUM_NAME,
                SchemaFields.TRACK_NUMBER,
                SchemaFields.GENRE_UUID,
                SchemaFields.RATING,
                SchemaFields.LANGUAGE]
        data_transformer.override_dict1_with_dict2_values_for_each_key_in_dict2(
            dict1=schema_data, dict2=post_data, keys=keys)

        for key in [SchemaFields.ARTISTS_NAMES, SchemaFields.ALBUM_ARTISTS_NAMES]:
            if key in post_data:
                schema_data[key] = post_data[key]
            elif key in schema_data_from_file:
                schema_data[key] = schema_data_from_file[key]

        if SchemaFields.TITLE not in schema_data:
            schema_data[Fields.TITLE] = self._get_generated_title_from_data(file=file, data=post_data)
        if SchemaFields.GENRE_UUID not in post_data:
            data_transformer.override_dict1_with_dict2_values_for_each_key_in_dict2(dict1=schema_data,
                                                                                    dict2=post_data,
                                                                                    keys=[SchemaFields.GENRE_NAME])

        data_transformer.update_dict_converting_str_to_int_value_if_set(key=Fields.RATING, data_dict=schema_data)
        return schema_data

    def _get_model_data_from_post_data(self, post_data: dict[str, Any]) -> dict[str, Any]:
        schema_data = self._get_schema_data_from_post_data(post_data)
        model_data = self._get_model_data_from_post_and_extract_common_schema_data(schema_data)
        model_data[Fields.TRACK_FILE] = schema_data[SchemaFields.TRACK_FILE_PUBLIC]
        return model_data

    def _get_post_data_from_extract_data(self, **kwargs):
        post_data = kwargs.copy()
        del post_data[ExtractFields.URL]
        return post_data

    def _get_model_data_from_extract_data(self, **kwargs):
        mine_track_url = kwargs[ExtractFields.URL]
        track_filename, is_filename_randomly_generated = \
            self._get_track_filename_with_extension(mine_track_url=mine_track_url, data=kwargs)

        # stream=True makes it more effective for large files.
        track_file_streamed = requests.get(mine_track_url, stream=True)

        with tempfile.NamedTemporaryFile(delete=True, dir=settings.FILE_UPLOAD_TEMP_DIR) as track_temp_file:
            for block in track_file_streamed.iter_content(1024 * 8):
                if not block:
                    break
                track_temp_file.write(block)
            track_temp_file.flush()
            track_temp_file.seek(0)

            os.chmod(track_temp_file.name, os.stat.S_IRWXU | os.stat.S_IRWXG | os.stat.S_IROTH | os.stat.S_IXOTH)

            post_data = self._get_post_data_from_extract_data(**kwargs)
            post_data[PostFields.TRACK_FILE_PUBLIC] = AppDjangoFile(file=track_temp_file,
                                                                    name=track_filename,
                                                                    file_abs_path=track_temp_file.name)
            force_title_generation_str = str(is_filename_randomly_generated)
            post_data[PostFields.FORCE_TITLE_GENERATION] = force_title_generation_str
            return self._get_model_data_from_post_data(post_data=post_data)

    def _get_model_data_from_update_data(self, update_data: dict[str, str]):
        schema_data = self._get_schema_data_from_update_data(update_data=update_data)
        return self._get_model_data_from_post_and_extract_common_schema_data(schema_data=schema_data)

    def decrease_position_of_next_tracks_in_old_track_playlists(self, user: User, playlists_with_old_position: list):
        from bodzify_api.model.lib_track_playlist_rel.LibTrackPlaylistRel import Fields as LibTrackPlaylistRelFields
        from bodzify_api.model.lib_track_playlist_rel.LibTrackPlaylistRel import LibTrackPlaylistRel
        for playlist_uuid, old_position in playlists_with_old_position:
            lib_track_playlist_rels_to_update = LibTrackPlaylistRel.objects.filter(
                user=user, playlist=playlist_uuid, position__gt=old_position)
            lib_track_playlist_rels_to_update.update(position=F(LibTrackPlaylistRelFields.POSITION) - 1)

    def update_genre_playlists(self, instance: 'LibraryTrack', old_genre: 'Genre | None'):
        from bodzify_api.model.criteria.children.genre.Genre import Genre
        common_genre = Genre.objects.get_common_ascendant(
            instance.genre, old_genre) if old_genre and instance.genre else None

        self._add_to_genre_playlists(instance=instance, genre_limit=common_genre)
        self._remove_from_genre_playlists(instance=instance, old_genre=old_genre, genre_limit=common_genre)

    def create(self, creation_type: str, **kwargs) -> 'LibraryTrack':
        from ..file.TrackFile import TrackFile

        model_data: dict
        if creation_type == LibTrackCreationType.POST:
            model_data = self._get_model_data_from_post_data(post_data=kwargs)
        elif creation_type == LibTrackCreationType.EXTRACT:
            model_data = self._get_model_data_from_extract_data(extract_data=kwargs)
        else:
            raise NotImplementedError(f"Creation type {creation_type} is not implemented")

        artists = model_data.pop(Fields.ARTISTS, None)
        track_file_model_data = dict()
        track_file_model_data[TrackFileFields.FILE] = model_data.pop(Fields.TRACK_FILE)

        instance: LibraryTrack = super().create(**model_data)
        if artists:
            instance.artists.set(artists)

        track_file_model_data[TrackFileFields.USER] = instance.user
        track_file_model_data[TrackFileFields.LIB_TRACK] = instance

        file_extension = AudioFile(track_file_model_data[TrackFileFields.FILE]).file_extension
        if file_extension == 'flac':
            from ..file.flac.FlacTrackFile import FlacTrackFile
            FlacTrackFile.objects.create(**track_file_model_data)
        else:
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

        model_data = self._get_model_data_from_update_data(update_data=kwargs)
        updated_instance: LibraryTrack = super().update_instance(old_instance, **model_data)

        if old_genre != updated_instance.genre:
            self.update_genre_playlists(updated_instance, old_genre=old_genre)

        if old_album and updated_instance.album and old_album != updated_instance.album:
            Album.objects.delete_instance_if_no_track_linked_with_eventual_album_artist_deletion(old_album)
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
        self.decrease_position_of_next_tracks_in_old_track_playlists(
            user=user, playlists_with_old_position=old_playlists_with_positions)

    def delete_instance_with_checking_album_and_artists_potential_deletion(self, instance: 'LibraryTrack'):
        from bodzify_api.model.album.Album import Album
        from bodzify_api.model.artist.Artist import Artist
        artists: list[Artist] = list(instance.artists.all())  # list() makes a copy of the QuerySet before the deletion
        album = instance.album

        # The order of the deletions is important for deletion rollback testing. Be carefull before changing it.
        instance.delete()

        if album:
            Album.objects.delete_instance_if_no_track_linked_with_eventual_album_artist_deletion(album)
        for artist in artists:
            Artist.objects.delete_instance_if_nothing_linked(artist)

    def delete_with_checking_artists_potential_deletion(self, instance: 'LibraryTrack'):
        track_artists: QuerySet[Artist] = instance.artists.all()
        instance.delete()
        for artist in track_artists:
            Artist.objects.delete_instance_if_nothing_linked(artist)
