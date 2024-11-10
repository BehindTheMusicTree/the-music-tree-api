import os
import tempfile
from typing import List, TYPE_CHECKING, Optional

from django.db import transaction
from django.db.models import F
from django.utils import timezone
from django.core.files.base import File as DjangoFile
import requests
from rest_framework.exceptions import ValidationError

from bodzify_api import settings
from bodzify_api.model.public_standard_resource.PublicStandardResourceManager import PublicStandardResourceManager
from bodzify_api.model.criteria.type.CriteriaTypePks import CriteriaTypesPks
from bodzify_api.model.artist.Artist import Artist
from bodzify_api.model.user.User import User
from bodzify_api.utils import audio_metadata, utils
from bodzify_api.utils.app_django_file import AppDjangoFile
from bodzify_api.utils.audio_metadata.NormalizedMetadataKeys import NormalizedMetadataKeys
from bodzify_api.view.viewset.model.lib_track.LibTrackCreationType import LibTrackCreationType
from bodzify_api.serializer.schema.lib_track.input.Fields import Fields as SchemaFields
from bodzify_api.serializer.schema.lib_track.input.endpoint.post import Fields as PostFields
from bodzify_api.serializer.schema.lib_track.input.endpoint.extract import Fields as ExtractFields
from .Fields import Fields


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
                CriteriaPlaylist.objects.update_instance(instance=criteria_playlist,
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
            CriteriaPlaylist.objects.update_instance(instance=genreless_criteria_playlist,
                                                     last_track_list_update_date=update_date)

    def decrease_position_of_next_tracks_in_old_track_playlists(self, user: User, playlists_with_old_position: list):
        from bodzify_api.model.lib_track_playlist_rel.LibTrackPlaylistRel import LibTrackPlaylistRel
        from bodzify_api.model.lib_track_playlist_rel.LibTrackPlaylistRel import Fields as LibTrackPlaylistRelFields
        for playlist_uuid, old_position in playlists_with_old_position:
            lib_track_playlist_rels_to_update = \
                LibTrackPlaylistRel.objects.filter(user=user, base_playlist=playlist_uuid, position__gt=old_position)
            lib_track_playlist_rels_to_update.update(position=F(LibTrackPlaylistRelFields.POSITION) - 1)

    def _get_generated_title_from_data(self, file: DjangoFile, data: dict):
        filename = os.path.basename(file.name).rsplit('.', 1)[0]
        filename_without_expressions_to_exclude = utils.remove_substrings_from_string(
            string_a=filename, substrings=settings.LIB_TRACK_FILENAME_EXPRESSIONS_TO_EXCLUDE_GENERATING_TITLE)
        if SchemaFields.FORCE_TITLE_GENERATION in data:
            force_title_generation = data[SchemaFields.FORCE_TITLE_GENERATION]
        else:
            force_title_generation = False

        if len(filename_without_expressions_to_exclude) > settings.LIB_TRACK_FILENAME_LEN_MAX or force_title_generation:
            title = settings.LIB_TRACK_GENERATED_TITLE_PREFIXE + \
                utils.generate_short_uu(settings.LIB_TRACK_GENERATED_TITLE_LENGTH -
                                        len(settings.LIB_TRACK_GENERATED_TITLE_PREFIXE))
        else:
            title = filename_without_expressions_to_exclude
        return title

    def _update_model_data_with_genre_uuid_if_genre_in_schema_data(
            self, user: User, model_data: dict, schema_data: dict):
        from bodzify_api.model.criteria.children.genre.Genre import Genre
        if SchemaFields.GENRE_UUID in schema_data:
            genre_uuid = schema_data[SchemaFields.GENRE_UUID]

            if genre_uuid == "":
                genre_uuid = None
        else:
            genre_uuid = None
            if SchemaFields.GENRE_NAME in schema_data:
                genre_name = schema_data[SchemaFields.GENRE_NAME]

                if not genre_name or genre_name == "":
                    genre_uuid = None
                else:
                    genre: Genre
                    genre, _ = Genre.objects.get_or_create(user=user, name=genre_name)
                    genre_uuid = genre.uuid
            else:
                return

        model_data[Fields.GENRE] = genre_uuid
        return

    def _get_schema_data_from_file(self, file):
        try:
            normalized_metadata = audio_metadata.get_normalized_metadata_from_file(
                file=file,
                normalized_rating_max_value=settings.LIB_TRACK_RATING_VALUE_MAX)
        except Exception as error:
            raise ValidationError({Fields.TRACK_FILE_USER_FRIENDLY: [
                f"Error while extracting metadata from file: {error}"]})

        save_data_with_potential_none = utils.get_copy_of_dict_including_only_specified_keys(
            dict=normalized_metadata,
            keys=[NormalizedMetadataKeys.TITLE,
                  NormalizedMetadataKeys.ARTISTS_NAMES,
                  NormalizedMetadataKeys.ALBUM_NAME,
                  NormalizedMetadataKeys.ALBUM_ARTISTS_NAMES,
                  NormalizedMetadataKeys.GENRE_NAME,
                  NormalizedMetadataKeys.RATING,
                  NormalizedMetadataKeys.LANGUAGE])

        schema_data_clean = utils.remove_none_or_empty_key_from_dict(save_data_with_potential_none)
        schema_data_clean[SchemaFields.FILE] = file

        return schema_data_clean

    def _update_model_data_with_album_uuid_if_album_name_in_schema_data(self,
                                                                        user: User,
                                                                        model_data: dict,
                                                                        schema_data: dict):
        from bodzify_api.model.album.Album import Album
        if SchemaFields.ALBUM_NAME in schema_data:
            album_name = schema_data[SchemaFields.ALBUM_NAME]

            if not album_name:
                return None

            if SchemaFields.ALBUM_ARTISTS_NAMES in schema_data:
                album_artists_names_str = schema_data[SchemaFields.ALBUM_ARTISTS_NAMES]
                if album_artists_names_str:
                    album_artists_name_list = \
                        Artist.objects.get_artists_names_list_from_str(names_str=album_artists_names_str)
                else:
                    album_artists_name_list = []
            else:
                album_artists_name_list = []

            album = Album.objects.get_album_from_name_and_album_artists_names_list_after_eventual_creations(
                user=user, album_name=album_name, album_artists_names_list=album_artists_name_list)

            model_data[Fields.ALBUM] = album.uuid if album else None

    def _update_model_data_with_artists_uuids_if_artists_names_str_in_schema_data_or_empty_list(
            self, user: User, model_data: dict, schema_data: dict):
        if SchemaFields.ARTISTS_NAMES in schema_data:
            artists_names_str = schema_data[SchemaFields.ARTISTS_NAMES]
            if artists_names_str:
                artists = Artist.objects.get_artists_list_from_names_str_after_eventual_creation(
                    user=user, artists_names_str=artists_names_str)
                artists_uuids = [artist.uuid for artist in artists]
            else:
                artists_uuids = []
        else:
            artists_uuids = []
        model_data[Fields.ARTISTS] = artists_uuids

    def _get_track_filename_with_extension(self, mine_track_url: str, data: dict):
        file_extension = utils.get_file_extension_from_url(mine_track_url)
        is_filename_randomly_generated = False
        if Fields.TITLE in data:
            title = data[Fields.TITLE]
            if SchemaFields.ARTISTS_NAMES in data:
                artist_name = data[SchemaFields.ARTISTS_NAMES]
                if artist_name is None or artist_name == "":
                    filename_without_extension = title
                else:
                    filename_without_extension = artist_name + " - " + title
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

    def _get_model_data_from_schema_data(self, user: User, **kwargs) -> dict:
        model_data = dict()

        for key in [Fields.TRACK_FILE_FINGERPRINT_MUST_BE_UNIQUE,
                    Fields.TRACK_FILE,
                    Fields.TITLE,
                    Fields.RATING,
                    Fields.LANGUAGE,
                    Fields.ARCHIVED,
                    Fields.POSITION_IN_ALBUM]:
            utils.update_data1_with_key_if_set_in_data2(key=key, data1=model_data, data2=kwargs)

        self._update_model_data_with_artists_uuids_if_artists_names_str_in_schema_data_or_empty_list(
            user=user, model_data=model_data, schema_data=kwargs)
        self._update_model_data_with_album_uuid_if_album_name_in_schema_data(user=user,
                                                                             model_data=model_data,
                                                                             schema_data=kwargs)
        self._update_model_data_with_genre_uuid_if_genre_in_schema_data(user=user,
                                                                        model_data=model_data,
                                                                        schema_data=kwargs)

        return model_data

    def _get_schema_data_from_put_data(self, put_data: dict, oldinstance=None) -> dict:
        schema_data = put_data.copy()
        utils.update_data1_converting_str_to_int_value_if_set(key=Fields.RATING, data1=schema_data)
        return schema_data

    def _get_schema_data_from_post_data(self, **kwargs) -> dict:
        file = kwargs[PostFields.FILE]
        schema_data_from_file = self._get_schema_data_from_file(file=file)

        schema_data = schema_data_from_file.copy()
        keys = [SchemaFields.FILE,
                SchemaFields.TRACK_FILE_FINGERPRINT_MUST_BE_UNIQUE,
                SchemaFields.TITLE,
                SchemaFields.ARTISTS_NAMES,
                SchemaFields.ALBUM_NAME,
                SchemaFields.ALBUM_ARTISTS_NAMES,
                SchemaFields.POSITION_IN_ALBUM,
                SchemaFields.GENRE_UUID,
                SchemaFields.RATING,
                SchemaFields.LANGUAGE]
        utils.override_data1_with_data2_values_for_each_key_in_data2(data1=schema_data, data2=kwargs, keys=keys)

        if SchemaFields.TITLE not in schema_data:
            schema_data[Fields.TITLE] = self._get_generated_title_from_data(file=file, **kwargs)
        if SchemaFields.GENRE_UUID not in kwargs:
            utils.override_data1_with_data2_values_for_each_key_in_data2(data1=schema_data,
                                                                         data2=kwargs,
                                                                         keys=[SchemaFields.GENRE_NAME])

        utils.update_data1_converting_str_to_int_value_if_set(key=Fields.RATING, data1=schema_data)
        return schema_data

    def _get_model_data_from_post_data(self, **kwargs):
        kwargs = self._get_schema_data_from_post_data(**kwargs)
        return self._get_model_data_from_schema_data(**kwargs)

    def _get_post_data_from_extract_data(self, **kwargs):
        save_data = kwargs.copy()
        del save_data[ExtractFields.URL]
        return save_data

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
            post_data[PostFields.FILE] = AppDjangoFile(file=track_temp_file,
                                                       name=track_filename,
                                                       file_abs_path=track_temp_file.name)
            force_title_generation_str = str(is_filename_randomly_generated)
            post_data[PostFields.FORCE_TITLE_GENERATION] = force_title_generation_str
            return self._get_model_data_from_post_data(data_validated=post_data)

    def _get_model_data_from_update_data(self, instance: 'LibraryTrack', **kwargs):
        schema_data = self._get_schema_data_from_put_data(oldinstance=instance, **kwargs)
        return self._get_model_data_from_schema_data(oldinstance=instance, **schema_data)

    def update_genre_playlists(self, instance: 'LibraryTrack', old_genre: Optional['Genre']):
        common_genre = \
            Genre.objects.get_common_ascendant(instance.genre, old_genre) if old_genre and instance.genre else None

        self._add_to_genre_playlists(instance, genre_limit=common_genre)
        self._remove_from_genre_playlists(
            instance, old_genre=old_genre, genre_limit=common_genre)

    def create(self, creation_type: str, **kwargs) -> 'LibraryTrack':
        model_data: dict
        if creation_type == LibTrackCreationType.POST:
            model_data = self._get_model_data_from_post_data(**kwargs)
        elif creation_type == LibTrackCreationType.EXTRACT:
            model_data = self._get_model_data_from_extract_data(data=kwargs)
        else:
            raise NotImplementedError(f"Creation type {creation_type} is not implemented")

        instance = super().create(**model_data)
        self._add_to_genre_playlists(instance)
        return instance

    def create_instance_with_track_file(self, track_file_data, library_track_data: dict):
        from bodzify_api.model.track.file.TrackFile import TrackFile, Fields as TrackFileFields

        with transaction.atomic():
            artists = library_track_data.pop(Fields.ARTISTS, None)
            library_track: LibraryTrack = self.model(**library_track_data)
            library_track.save()
            if artists:
                library_track.artists.set(artists)

            track_file_data[TrackFileFields.LIBRARY_TRACK] = library_track
            TrackFile.objects.create(**track_file_data)

        library_track.update_file_tags_from_lib_track_instance_values()

        return library_track

    def update_instance(self, old_instance: 'LibraryTrack', **kwargs) -> 'LibraryTrack':
        old_album_artists_list: List[Artist] = []
        if old_instance.album:
            old_album_artists_list = list(old_instance.album.album_artists.all())
            old_album = old_instance.album
        else:
            old_album = None

        updated_instance: LibraryTrack = super().update_instance(old_instance, **kwargs)

        if old_instance.genre != updated_instance.genre:
            self.update_genre_playlists(updated_instance, old_genre=old_instance.genre)

        if old_instance.album and updated_instance.album and old_album != updated_instance.album:
            old_instance.album.delete_if_no_track_linked_with_eventual_album_artist_deletion()
            for album_artist in old_album_artists_list:
                album_artist.delete_if_nothing_linked()

        if old_instance.artists.count() > 0:
            current_track_artists_list = list(updated_instance.artists.all())
            old_track_artists_list: list[Artist] = list(old_instance.artists.all())
            for old_track_artist in old_track_artists_list:
                if old_track_artist not in current_track_artists_list:
                    old_track_artist.delete_if_nothing_linked()

        return updated_instance

    def delete_instance(self, instance: 'LibraryTrack'):
        old_lib_tracks_playlists_with_positions = instance.get_lib_track_playlists_with_positions()
        user = instance.user
        instance.delete_with_checking_album_and_artists_potential_deletion()
        self.decrease_position_of_next_tracks_in_old_track_playlists(
            user=user,
            playlists_with_old_position=old_lib_tracks_playlists_with_positions)
