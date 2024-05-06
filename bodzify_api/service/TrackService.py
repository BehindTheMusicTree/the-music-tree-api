#!/usr/bin/env python

import os
import random
import string
from tempfile import NamedTemporaryFile
import requests

from django.contrib.auth.models import User
from django.core.files.base import File as DjangoFile
from django.db.models import F
from django.core.exceptions import ValidationError

import bodzify_api.audiometadata as audiometadata
from bodzify_api.model.PlaylistLibTrackRelation \
    import PlaylistLibTrackRelation, ATTRIBUTES_LABEL as playlist_lib_track_relation_ATTRIBUTES_LABEL
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.criteria.CriteriaType import CRITERIA_TYPES_ID
import bodzify_api.settings as settings
from bodzify_api.model.Album import Album
from bodzify_api.model.Artist import Artist
from bodzify_api.serializer.track.input.endpoint.LibTrackPostSerializer \
    import LibTrackPostSerializer, FIELDS as POST_FIELDS
from bodzify_api.serializer.track.input.LibTrackModelSerializer \
    import FIELDS as SAVE_MODEL_FIELDS, TrackSaveModelSerializer
from bodzify_api.serializer.file.input.FileModelSerializer import FileModelSerializer, FIELDS as FILE_SAVE_MODEL_FIELDS
from bodzify_api.serializer.track.input.LibTrackSchemaSerializer \
    import FIELDS as SAVE_SCHEMA_FIELDS, LibTrackSaveSchemaSerializer
from bodzify_api.serializer.track.input.endpoint.LibTrackPutSerializer import LibTrackPutSerializer
from bodzify_api.serializer.mine.track.MineTrackSerializer import FIELDS as MINE_TRACK_FIELDS
from bodzify_api.service.Service import Service


class TrackService(Service):

    @staticmethod
    def generate_short_uu(length: int):
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))

    @staticmethod
    def get_substring_after_last_slash(string: str):
        return string.split("/")[-1]

    @staticmethod
    def get_file_extension_from_url(url: str):
        return url.split(".")[-1]

    @staticmethod
    def _get_generated_title_from_data(file: DjangoFile, data: dict):
        filename = os.path.basename(file.name).split('.')[0]
        if SAVE_SCHEMA_FIELDS.FORCE_TITLE_GENERATION in data:
            force_title_generation = data[SAVE_SCHEMA_FIELDS.FORCE_TITLE_GENERATION]
        else:
            force_title_generation = False

        if len(filename) > settings.LIB_TRACK_FILENAME_LEN_MAX or force_title_generation:
            title = settings.LIB_TRACK_GENERATED_TITLE_PREFIXE + \
                TrackService.generate_short_uu(settings.LIB_TRACK_GENERATED_TITLE_LENGTH -
                                               len(settings.LIB_TRACK_GENERATED_TITLE_PREFIXE))
        else:
            title = filename
        return title

    @staticmethod
    def _decrease_position_of_next_tracks_in_old_track_playlists(playlists_with_old_position: list):
        for playlist_uuid, old_position in playlists_with_old_position:
            playlist_lib_track_relation_relations_to_update = PlaylistLibTrackRelation.objects.filter(
                playlist__uuid=playlist_uuid, position__gt=old_position)
            playlist_lib_track_relation_relations_to_update.update(
                position=F(playlist_lib_track_relation_ATTRIBUTES_LABEL.POSITION) - 1)

    @staticmethod
    def _update_data1_with_file_obj_id_if_file_in_data2(user: User, data1: dict, data2: dict):
        file_key = SAVE_SCHEMA_FIELDS.FILE_OBJ
        if file_key in data2:
            file_model_data = dict()
            file_model_data[FILE_SAVE_MODEL_FIELDS.USER] = user.pk
            file_model_data[FILE_SAVE_MODEL_FIELDS.FILE] = data2[file_key]
            file_model_serializer = FileModelSerializer(data=file_model_data)
            file_model_serializer.is_valid(raise_exception=True)
            file_obj = file_model_serializer.save(user=user)
            data1[SAVE_MODEL_FIELDS.FILE_OBJ] = file_obj.pk

    @staticmethod
    def _update_data1_with_genre_uuid_if_genre_in_data2(user: User, data1: dict, data2: dict):
        genre_uuid_key = SAVE_SCHEMA_FIELDS.GENRE_UUID
        if genre_uuid_key in data2:
            genre_uuid = data2[genre_uuid_key]

            if genre_uuid in ["", None]:
                genre_uuid = None
        else:
            genre_name_key = SAVE_SCHEMA_FIELDS.GENRE_NAME
            genre_uuid = None
            if genre_name_key in data2:
                genre_name = data2[genre_name_key]

                if genre_name in ["", None]:
                    genre_uuid = None
                else:
                    criteria, _ = Criteria.objects.get_or_create(user=user,
                                                                 type_id=CRITERIA_TYPES_ID.GENRE,
                                                                 name=genre_name)
                    genre_uuid = criteria.uuid
            else:
                return

        data1[SAVE_MODEL_FIELDS.GENRE] = genre_uuid

        return

    def _get_post_serializer(self, post_data: dict):
        return LibTrackPostSerializer(data=post_data)

    def _get_put_serializer(self, old_instance, put_data: dict):
        return LibTrackPutSerializer(instance=old_instance, data=put_data)

    def _get_save_schema_serializer(self, old_instance, save_schema_data: dict, request):
        return LibTrackSaveSchemaSerializer(data=save_schema_data, context={'request': request})

    def _get_save_model_serializer(self, old_instance, save_model_data: dict, partial: bool):
        return TrackSaveModelSerializer(instance=old_instance, data=save_model_data, partial=True)

    def _get_save_schema_data_from_post_data(self, post_data: dict) -> dict:
        file = post_data[POST_FIELDS.FILE_OBJ]
        save_schema_data_from_file = self._get_save_schema_data_from_file(file=file)

        save_schema_data = save_schema_data_from_file.copy()
        keys = [SAVE_SCHEMA_FIELDS.FILE_OBJ,
                SAVE_SCHEMA_FIELDS.TITLE,
                SAVE_SCHEMA_FIELDS.ARTIST_NAME,
                SAVE_SCHEMA_FIELDS.ALBUM_NAME,
                SAVE_SCHEMA_FIELDS.ALBUM_ARTISTS_NAMES_STR,
                SAVE_SCHEMA_FIELDS.GENRE_UUID,
                SAVE_SCHEMA_FIELDS.RATING,
                SAVE_SCHEMA_FIELDS.LANGUAGE]
        self._override_data1_with_data2_values_for_each_key_in_data2(data1=save_schema_data, data2=post_data, keys=keys)

        if SAVE_SCHEMA_FIELDS.TITLE not in save_schema_data:
            save_schema_data[SAVE_SCHEMA_FIELDS.TITLE] = self._get_generated_title_from_data(file=file, data=post_data)
        if SAVE_SCHEMA_FIELDS.GENRE_UUID not in post_data:
            self._override_data1_with_data2_values_for_each_key_in_data2(data1=save_schema_data,
                                                                         data2=post_data,
                                                                         keys=[SAVE_SCHEMA_FIELDS.GENRE_NAME])

        Service._update_data1_converting_str_to_int_value_if_set(key=SAVE_SCHEMA_FIELDS.RATING, data1=save_schema_data)

        return save_schema_data

    def _get_save_schema_data_from_put_data(self, put_data: dict, old_instance=None) -> dict:
        save_schema_data = put_data.copy()
        Service._update_data1_converting_str_to_int_value_if_set(key=SAVE_SCHEMA_FIELDS.RATING, data1=save_schema_data)
        return save_schema_data

    def _get_save_model_data_from_save_schema_data_not_including_user_field(self, user: User,
                                                                            save_schema_data: dict,
                                                                            old_instance) -> dict:
        save_model_data = dict()

        for key in [SAVE_MODEL_FIELDS.TITLE, SAVE_MODEL_FIELDS.RATING, SAVE_MODEL_FIELDS.LANGUAGE]:
            self._update_data1_with_key_if_set_in_data2(key=key, data1=save_model_data, data2=save_schema_data)

        self._update_data1_with_artist_uuid_if_artist_name_in_data2(user=user,
                                                                    data1=save_model_data,
                                                                    data2=save_schema_data)
        self._update_data1_with_album_uuid_if_album_name_in_data2(user=user,
                                                                  data1=save_model_data,
                                                                  data2=save_schema_data)
        self._update_data1_with_genre_uuid_if_genre_in_data2(user=user, data1=save_model_data, data2=save_schema_data)
        self._update_data1_with_file_obj_id_if_file_in_data2(user=user, data1=save_model_data, data2=save_schema_data)

        return save_model_data

    def _update_data1_with_album_uuid_if_album_name_in_data2(self, user: User, data1: dict, data2: dict):
        data1_album_key = SAVE_MODEL_FIELDS.ALBUM
        data2_album_name_key = SAVE_SCHEMA_FIELDS.ALBUM_NAME
        data2_artists_names_key = SAVE_SCHEMA_FIELDS.ALBUM_ARTISTS_NAMES_STR

        if data2_album_name_key in data2:
            album_name = data2[data2_album_name_key]

            if data2_artists_names_key in data2:
                album_artists_name_string = data2[data2_artists_names_key]
                if album_artists_name_string is not None:
                    album_artists_name_list = self._get_artists_name_list_from_string(album_artists_name_string)
                else:
                    album_artists_name_list = None
            else:
                album_artists_name_list = None
            album = Album.get_album_from_name_and_album_artists_name_list_after_eventual_creations(
                user=user, album_name=album_name, album_artists_name_list=album_artists_name_list)

            if album is not None:
                data1[data1_album_key] = album.uuid
            else:
                data1[data1_album_key] = None

    def _get_artists_name_list_from_string(self, names_string: str) -> list:
        names_with_eventual_spaces_around_and_duplicates = names_string.split(
            audiometadata.METADATA_ARTISTS_SEPARATION_CHAR)
        names = list()
        for name_with_eventual_spaces_around in names_with_eventual_spaces_around_and_duplicates:
            name = name_with_eventual_spaces_around.strip()
            if name != "" and names.count(name) == 0:
                names.append(name)
        return names

    def _get_post_data_from_extract_data(self, extract_data: dict):
        save_data = extract_data.copy()
        del save_data[MINE_TRACK_FIELDS.URL]
        return save_data

    def _get_track_filename_with_extension(self, mine_track_url: str, data: dict):
        file_extension = self.get_file_extension_from_url(mine_track_url)
        is_filename_randomly_generated = False
        title_key = SAVE_SCHEMA_FIELDS.TITLE
        if title_key in data:
            title = data[title_key]
            artist_name_key = SAVE_SCHEMA_FIELDS.ARTIST_NAME
            if artist_name_key in data:
                artist_name = data[artist_name_key]
                if artist_name is None or artist_name == "":
                    filename_without_extension = title
                else:
                    filename_without_extension = artist_name + " - " + title
            else:
                filename_without_extension = title
            filename_with_extension = filename_without_extension + "." + file_extension
        else:
            filename_with_extension = self.get_substring_after_last_slash(
                mine_track_url)
            if len(filename_with_extension) > settings.LIB_TRACK_FILENAME_LEN_MAX:
                filename_without_extension = self.generate_short_uu(
                    settings.LIB_TRACK_FILENAME_GENERATED_WITHOUT_EXTENSION_LENGTH - len(file_extension) - 1)
                filename_with_extension = filename_without_extension + "." + file_extension
                is_filename_randomly_generated = True
        return filename_with_extension, is_filename_randomly_generated

    def _get_save_schema_data_from_file(self, file):
        try:
            normalized_metadata = audiometadata.get_normalized_metadata_from_file(
                file=file,
                normalized_rating_max_value=settings.LIB_TRACK_RATING_VALUE_MAX)
        except Exception as error:
            raise ValidationError(f"Error while extracting metadata from file: {error}")

        save_data_with_potential_none = self._get_copy_of_dict_including_only_specified_keys(
            dict=normalized_metadata,
            keys=[SAVE_SCHEMA_FIELDS.TITLE,
                  SAVE_SCHEMA_FIELDS.ARTIST_NAME,
                  SAVE_SCHEMA_FIELDS.ALBUM_NAME,
                  SAVE_SCHEMA_FIELDS.ALBUM_ARTISTS_NAMES_STR,
                  SAVE_SCHEMA_FIELDS.GENRE_NAME,
                  SAVE_SCHEMA_FIELDS.RATING,
                  SAVE_SCHEMA_FIELDS.LANGUAGE])
        save_data_clean = self._remove_none_or_empty_key_from_dict(save_data_with_potential_none)
        save_data_clean[SAVE_SCHEMA_FIELDS.FILE_OBJ] = file

        return save_data_clean

    def _update_data1_with_artist_uuid_if_artist_name_in_data2(self, user: User, data1: dict, data2: dict):
        data2_artist_name_key = SAVE_SCHEMA_FIELDS.ARTIST_NAME
        data1_artist_key = SAVE_MODEL_FIELDS.ARTIST
        if data2_artist_name_key in data2:
            artist_name = data2[data2_artist_name_key]
            artist = Artist.get_artist_from_name_after_eventual_creation(user=user, artist_name=artist_name)
            if artist is not None:
                data1[data1_artist_key] = artist.uuid
            else:
                data1[data1_artist_key] = None

    def extract(self, extract_data: dict, request):
        mine_track_url = extract_data[MINE_TRACK_FIELDS.URL]
        track_in_memory_file = requests.get(mine_track_url, stream=True)
        with NamedTemporaryFile(delete=True) as track_temp_file:
            for block in track_in_memory_file.iter_content(1024 * 8):
                if not block:
                    break
                track_temp_file.write(block)
            track_temp_file.flush()
            track_temp_file.seek(0)

            post_data = self._get_post_data_from_extract_data(extract_data)

            track_filename, is_filename_randomly_generated = self._get_track_filename_with_extension(
                mine_track_url=mine_track_url, data=extract_data)
            post_data[POST_FIELDS.FILE_OBJ] = DjangoFile(file=track_temp_file, name=track_filename)
            force_title_generation_str = str(is_filename_randomly_generated)
            post_data[SAVE_SCHEMA_FIELDS.FORCE_TITLE_GENERATION] = force_title_generation_str
            library_track = self.create(post_data=post_data, request=request)

        return library_track

    def delete(self, user: User, instance):
        old_lib_tracks_playlists_with_positions = instance._get_lib_track_playlists_with_positions()
        instance.delete_with_checking_album_and_artist_potential_deletion()
        TrackService._decrease_position_of_next_tracks_in_old_track_playlists(old_lib_tracks_playlists_with_positions)
