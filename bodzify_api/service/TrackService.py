#!/usr/bin/env python

import logging
import os
import random
import string
from tempfile import NamedTemporaryFile

import requests
from django.contrib.auth.models import User
from django.core.files.base import File
from django.http import QueryDict
from django.http.request import QueryDict
from rest_framework.serializers import Serializer

import bodzify_api.AudioMetadataManager as AudioMetadataManager
import bodzify_api.settings as settings
from bodzify_api.model.Album import Album
from bodzify_api.model.Artist import Artist
from bodzify_api.serializer.track.input.schema.LibTrackPostSchemaSerializer \
    import LibTrackPostSchemaSerializer, FIELDS as POST_FIELDS
from bodzify_api.serializer.track.input.LibTrackSaveModelSerializer import FIELDS as SAVE_MODEL_FIELDS
from bodzify_api.serializer.track.input.schema.LibTrackSaveSchemaSerializer import FIELDS as SAVE_SCHEMA_FIELDS
from bodzify_api.serializer.track.input.schema.LibTrackPutSchemaSerializer import LibTrackPutSchemaSerializer
from bodzify_api.serializer.track.input.LibTrackSaveModelSerializer import TrackSaveModelSerializer
from bodzify_api.serializer.mine.track.MineTrackSerializer import FIELDS as MINE_TRACK_FIELDS
from bodzify_api.service.criteria.GenreService import GenreService
from bodzify_api.service.Service import Service

logger = logging.getLogger('bodzify_api')


class TrackService(Service):

    def _get_post_schema_serializer(self, post_schema_data: QueryDict) -> Serializer:
        return LibTrackPostSchemaSerializer(data=post_schema_data)  # type: ignore

    def _get_put_schema_serializer(self, old_instance, put_schema_data: QueryDict) -> Serializer:
        return LibTrackPutSchemaSerializer(instance=old_instance, data=put_schema_data)  # type: ignore

    def _get_save_model_serializer(self, old_instance, save_model_data: QueryDict, partial: bool) -> Serializer:
        return TrackSaveModelSerializer(instance=old_instance, data=save_model_data, partial=True)  # type: ignore

    def _get_save_schema_data_from_post_schema_data(self, post_schema_data: QueryDict) -> QueryDict:
        file = post_schema_data[POST_FIELDS.FILE]
        save_schema_data_from_file = self._get_save_schema_data_from_file(file=file)
        keys = [SAVE_SCHEMA_FIELDS.FILE,
                SAVE_SCHEMA_FIELDS.TITLE,
                SAVE_SCHEMA_FIELDS.ARTIST_NAME,
                SAVE_SCHEMA_FIELDS.ALBUM_NAME,
                SAVE_SCHEMA_FIELDS.ALBUM_ARTISTS_NAMES_STRING,
                SAVE_SCHEMA_FIELDS.GENRE_NAME,
                SAVE_SCHEMA_FIELDS.RATING,
                SAVE_SCHEMA_FIELDS.LANGUAGE]
        save_schema_data = self._get_dict1_overriden_with_dict2_for_each_key_provided_in_dict2(
            dict1=save_schema_data_from_file, dict2=post_schema_data, keys=keys)

        if SAVE_SCHEMA_FIELDS.TITLE not in save_schema_data:
            filename = os.path.basename(file.name).split('.')[0]  # type: ignore
            if SAVE_SCHEMA_FIELDS.FORCE_TITLE_GENERATION in post_schema_data:
                force_title_generation = post_schema_data[SAVE_SCHEMA_FIELDS.FORCE_TITLE_GENERATION]
            else:
                force_title_generation = False

            if len(filename) > settings.LIB_TRACK_FILENAME_LENGTH_MAX or force_title_generation:
                title = settings.LIB_TRACK_GENERATED_TITLE_PREFIXE + \
                    self.generate_short_uu(settings.LIB_TRACK_GENERATED_TITLE_LENGTH -
                                           len(settings.LIB_TRACK_GENERATED_TITLE_PREFIXE))
            else:
                title = filename
            save_schema_data[SAVE_SCHEMA_FIELDS.TITLE] = title

        return save_schema_data

    def _get_save_model_data_from_save_schema_data(
            self, user: User, save_schema_data: QueryDict, old_instance) -> QueryDict:
        save_model_data = QueryDict(mutable=True)
        save_model_data[SAVE_MODEL_FIELDS.USER] = user.pk

        for key in [SAVE_MODEL_FIELDS.FILE,
                    SAVE_MODEL_FIELDS.TITLE,
                    SAVE_MODEL_FIELDS.DURATION,
                    SAVE_MODEL_FIELDS.RATING,
                    SAVE_MODEL_FIELDS.LANGUAGE]:
            save_model_data = self._get_querydict1_updated_with_querydict2_key_if_set(
                key=key,
                querydict1=save_model_data,
                querydict2=save_schema_data)

        save_model_data = self._get_dict1_updated_with_artist_uuid_if_artist_name_in_dict2(
            user=user,
            dict1=save_model_data,
            dict2=save_schema_data,
            dict2_artist_name_key=SAVE_SCHEMA_FIELDS.ARTIST_NAME,
            dict1_artist_key=SAVE_MODEL_FIELDS.ARTIST)

        save_model_data = self._get_dict1_updated_with_album_uuid_if_album_name_in_dict2(
            user=user,
            dict1=save_model_data,
            dict2=save_schema_data,
            dict1_album_key=SAVE_MODEL_FIELDS.ALBUM,
            dict2_album_name_key=SAVE_SCHEMA_FIELDS.ALBUM_NAME,
            dict2_artists_names_key=SAVE_SCHEMA_FIELDS.ALBUM_ARTISTS_NAMES_STRING)

        save_model_data = self._get_dict1_updated_with_genre_uuid_if_genre_name_in_dict2(
            user=user, dict1=save_model_data, dict2=save_schema_data)

        return save_model_data

    def extract(self, user: User, extract_schema_data: QueryDict):
        mine_track_url = extract_schema_data[MINE_TRACK_FIELDS.URL]
        try:
            track_in_memory_file = requests.get(mine_track_url, stream=True)
        except Exception as e:
            logger.error("Error while trying to get track from url: " + mine_track_url)
            logger.error(e)
            return None
        with NamedTemporaryFile(delete=True) as track_temp_file:
            for block in track_in_memory_file.iter_content(1024 * 8):
                if not block:
                    break
                track_temp_file.write(block)
            track_temp_file.flush()
            track_temp_file.seek(0)

            post_schema_data = self._get_post_schema_data_from_extract_schema_data(
                extract_schema_data)

            track_filename, is_filename_randomly_generated = self._get_track_filename_with_extension(
                mine_track_url, extract_schema_data)
            post_schema_data[POST_FIELDS.FILE] = File(track_temp_file, name=track_filename)  # type: ignore
            force_title_generation_str = str(is_filename_randomly_generated)
            post_schema_data[SAVE_SCHEMA_FIELDS.FORCE_TITLE_GENERATION] = force_title_generation_str
            library_track = self.create(
                user=user, post_schema_data=post_schema_data)

        return library_track

    def delete(self, user: User, instance):
        instance.delete_with_checking_album_and_artist_potential_deletion()

    def _get_save_schema_data_from_file(self, file):
        metadata_dict = AudioMetadataManager.get_metadata_dict_from_file(
            file=file, normalized_rating_max_value=settings.LIB_TRACK_RATING_VALUE_MAX)

        save_data = self._remove_none_or_empty_key_from_dict(metadata_dict)
        save_data[SAVE_SCHEMA_FIELDS.FILE] = file

        return save_data

    def _get_dict1_updated_with_artist_uuid_if_artist_name_in_dict2(self,
                                                                    user: User,
                                                                    dict1: QueryDict,
                                                                    dict2: QueryDict,
                                                                    dict2_artist_name_key: str,
                                                                    dict1_artist_key: str):
        if dict2_artist_name_key in dict2:
            artist_name = dict2[dict2_artist_name_key]
            artist = Artist.get_artist_from_name_after_eventual_creation(user=user, artist_name=artist_name)
            if artist is not None:
                dict1[dict1_artist_key] = artist.uuid
            else:
                dict1[dict1_artist_key] = None  # type: ignore
        return dict1

    def _get_dict1_updated_with_album_uuid_if_album_name_in_dict2(self,
                                                                  user: User,
                                                                  dict1: QueryDict,
                                                                  dict2: QueryDict,
                                                                  dict1_album_key: str,
                                                                  dict2_album_name_key: str,
                                                                  dict2_artists_names_key: str):
        if dict2_album_name_key in dict2:
            album_name = dict2[dict2_album_name_key]

            if dict2_artists_names_key in dict2:
                album_artists_name_string = dict2[dict2_artists_names_key]
                if album_artists_name_string is not None:
                    album_artists_name_list = self._get_artists_name_list_from_string(album_artists_name_string)
                else:
                    album_artists_name_list = None
            else:
                album_artists_name_list = None
            album = Album.get_album_from_name_and_album_artists_name_list_after_eventual_creations(
                user=user, album_name=album_name, album_artists_name_list=album_artists_name_list)

            if album is not None:
                dict1[dict1_album_key] = album.uuid
            else:
                dict1[dict1_album_key] = None  # type: ignore
        return dict1

    def _get_dict1_updated_with_genre_uuid_if_genre_name_in_dict2(self,
                                                                  user: User,
                                                                  dict1: QueryDict,
                                                                  dict2: QueryDict):
        genre_name_key = SAVE_SCHEMA_FIELDS.GENRE_NAME
        if genre_name_key in dict2:
            genre_name = dict2[genre_name_key]

            if genre_name in ["", None]:
                genre_uuid = None
            else:
                genreService = GenreService()
                genre_uuid = genreService.get_criteria_from_name_after_having_eventually_created_it(
                    user=user, criteria_name=genre_name).uuid
            dict1[SAVE_MODEL_FIELDS.GENRE] = genre_uuid  # type: ignore
        return dict1

    def _get_artists_name_list_from_string(self, names_string: str) -> list:
        names_with_eventual_spaces_around_and_duplicates = names_string.split(
            AudioMetadataManager.TAG_ARTISTS_SEPARATION_CHAR)
        names = list()
        for name_with_eventual_spaces_around in names_with_eventual_spaces_around_and_duplicates:
            name = name_with_eventual_spaces_around.strip()
            if name != "" and names.count(name) == 0:
                names.append(name)
        return names

    def _get_post_schema_data_from_extract_schema_data(self, requestData: QueryDict):
        save_data = requestData.copy()
        del save_data[MINE_TRACK_FIELDS.URL]
        return save_data

    def _get_track_filename_with_extension(self, mine_track_url: str, requestData: QueryDict):
        file_extension = self.get_file_extension_from_url(mine_track_url)
        is_filename_randomly_generated = False
        title_key = SAVE_SCHEMA_FIELDS.TITLE
        if title_key in requestData:
            title = requestData[title_key]
            artist_name_key = SAVE_SCHEMA_FIELDS.ARTIST_NAME
            if artist_name_key in requestData:
                artist_name = requestData[artist_name_key]
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
            if len(filename_with_extension) > settings.LIB_TRACK_FILENAME_LENGTH_MAX:
                filename_without_extension = self.generate_short_uu(
                    settings.LIB_TRACK_FILENAME_GENERATED_WITHOUT_EXTENSION_LENGTH - len(file_extension) - 1)
                filename_with_extension = filename_without_extension + "." + file_extension
                is_filename_randomly_generated = True
        return filename_with_extension, is_filename_randomly_generated

    @staticmethod
    def generate_short_uu(length: int):
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))

    @staticmethod
    def get_substring_after_last_slash(string: str):
        return string.split("/")[-1]

    @staticmethod
    def get_file_extension_from_url(url: str):
        return url.split(".")[-1]
