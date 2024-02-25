#!/usr/bin/env python

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
from bodzify_api.model.track.LibraryTrack import \
    LIB_TRACK_ATTRIBUTES_LABEL as LIB_TRACK_ATTRIBUTES_LABEL
from bodzify_api.model.track.MineTrack import \
    ATTRIBUTES_LABEL as MINE_TRACK_ATTRIBUTES_LABEL
from bodzify_api.serializer.track.input.schema.LibTrackSchemaPostSerializer import LibTrackSchemaPostSerializer
from bodzify_api.serializer.track.input.schema.LibTrackSchemaSaveSerializer import FIELDS as SCHEMA_SAVE_FIELDS
from bodzify_api.serializer.track.input.schema.LibTrackSchemaPutSerializer import LibTrackPutSchemaSerializer
from bodzify_api.serializer.track.input.TrackSaveModelSerializer import TrackSaveModelSerializer
from bodzify_api.service.criteria.GenreService import GenreService
from bodzify_api.service.Service import Service


class TrackService(Service):

    def _get_post_schema_serializer(self, post_schema_data: QueryDict) -> Serializer:
        return LibTrackSchemaPostSerializer(data=post_schema_data)  # type: ignore

    def _get_put_schema_serializer(self, old_instance, put_schema_data: QueryDict) -> Serializer:
        return LibTrackPutSchemaSerializer(instance=old_instance, data=put_schema_data)  # type: ignore

    def _get_save_model_serializer(self, old_instance, save_model_data: QueryDict, partial: bool) -> Serializer:
        return TrackSaveModelSerializer(instance=old_instance, data=save_model_data, partial=True)  # type: ignore

    def _get_save_schema_data_from_post_schema_data(self, post_schema_data: QueryDict) -> QueryDict:
        file = post_schema_data[LIB_TRACK_ATTRIBUTES_LABEL.FILE]
        save_schema_data_from_file = self._get_save_schema_data_from_file(
            file=file)
        save_schema_data = self._get_dict1_overriden_with_dict2_when_key_is_provided(
            dict1=save_schema_data_from_file, dict2=post_schema_data)

        if LIB_TRACK_ATTRIBUTES_LABEL.TITLE not in save_schema_data:
            filename = os.path.basename(file.name).split('.')[0]
            if SCHEMA_SAVE_FIELDS.FORCE_TITLE_GENERATION in post_schema_data:
                force_title_generation = post_schema_data[SCHEMA_SAVE_FIELDS.FORCE_TITLE_GENERATION]
            else:
                force_title_generation = False

            if len(filename) > settings.LIB_TRACK_FILENAME_LENGTH_MAX or force_title_generation:
                title = settings.LIB_TRACK_GENERATED_TITLE_PREFIXE + \
                    self.generate_short_uu(settings.LIB_TRACK_GENERATED_TITLE_LENGTH -
                                           len(settings.LIB_TRACK_GENERATED_TITLE_PREFIXE))
            else:
                title = filename
            save_schema_data[LIB_TRACK_ATTRIBUTES_LABEL.TITLE] = title

        return save_schema_data

    def _get_save_model_data_from_save_schema_data(self, user: User, save_schema_data: QueryDict) -> QueryDict:
        save_model_data = QueryDict(mutable=True)
        save_model_data[LIB_TRACK_ATTRIBUTES_LABEL.USER] = user.id

        save_model_data = self.get_querydict1_updated_with_querydict2_key_if_set(
            key=LIB_TRACK_ATTRIBUTES_LABEL.FILE,
            querydict1=save_model_data,
            querydict2=save_schema_data)

        save_model_data = self.get_querydict1_updated_with_querydict2_key_if_set(
            key=LIB_TRACK_ATTRIBUTES_LABEL.TITLE,
            querydict1=save_model_data,
            querydict2=save_schema_data)

        save_model_data = self._get_dict1_updated_with_artist_uuid_if_artist_name_in_dict2(
            user=user, dict1=save_model_data, dict2=save_schema_data)

        save_model_data = self._get_dict1_updated_with_album_uuid_if_album_name_in_dict2(
            user=user, dict1=save_model_data, dict2=save_schema_data)

        save_model_data = self._get_dict1_updated_with_genre_uuid_if_genre_name_in_dict2(
            user=user, dict1=save_model_data, dict2=save_schema_data)

        save_model_data = self.get_querydict1_updated_with_querydict2_key_if_set(
            key=LIB_TRACK_ATTRIBUTES_LABEL.DURATION,
            querydict1=save_model_data,
            querydict2=save_schema_data)

        save_model_data = self.get_querydict1_updated_with_querydict2_key_if_set(
            key=LIB_TRACK_ATTRIBUTES_LABEL.RATING,
            querydict1=save_model_data,
            querydict2=save_schema_data)

        save_model_data = self.get_querydict1_updated_with_querydict2_key_if_set(
            key=LIB_TRACK_ATTRIBUTES_LABEL.LANGUAGE,
            querydict1=save_model_data,
            querydict2=save_schema_data)

        return save_model_data

    def extract(self, user: User, extract_schema_data: QueryDict):
        mine_track_url_label = extract_schema_data[MINE_TRACK_ATTRIBUTES_LABEL.URL]
        track_in_memory_file = requests.get(mine_track_url_label, stream=True)
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
                mine_track_url_label, extract_schema_data)
            post_schema_data[LIB_TRACK_ATTRIBUTES_LABEL.FILE] = File(
                track_temp_file, name=track_filename)
            force_title_generation_str = str(is_filename_randomly_generated)
            post_schema_data[SCHEMA_SAVE_FIELDS.FORCE_TITLE_GENERATION] = force_title_generation_str
            library_track = self.create(
                user=user, post_schema_data=post_schema_data)

        return library_track

    def delete(self, user: User, instance):
        instance.delete_with_checking_album_and_artist_potential_deletion()

    def _get_save_schema_data_from_file(self, file):
        metadata_dict = AudioMetadataManager.get_metadata_dict_from_file(
            file=file, normalized_rating_max_value=settings.LIB_TRACK_RATING_VALUE_MAX)

        save_data = self._remove_none_or_empty_key_from_dict(metadata_dict)
        save_data[LIB_TRACK_ATTRIBUTES_LABEL.FILE] = file

        return save_data

    def _get_dict1_updated_with_artist_uuid_if_artist_name_in_dict2(self,
                                                                    user: User, dict1: QueryDict, dict2: QueryDict):
        artist_name_key = SCHEMA_SAVE_FIELDS.ARTIST_NAME
        if artist_name_key in dict2:
            artist_name = dict2[artist_name_key]
            artist = Artist.get_artist_from_name_after_eventual_creation(
                user=user, artist_name=artist_name)
            artist_key = LIB_TRACK_ATTRIBUTES_LABEL.ARTIST
            if artist is not None:
                dict1[artist_key] = artist.uuid
            else:
                dict1[artist_key] = None
        return dict1

    def _get_dict1_updated_with_album_uuid_if_album_name_in_dict2(self,
                                                                  user: User, dict1: QueryDict, dict2: QueryDict):
        album_name_key = SCHEMA_SAVE_FIELDS.ALBUM_NAME

        if album_name_key in dict2:
            album_name = dict2[album_name_key]

            artists_names_key = SCHEMA_SAVE_FIELDS.ALBUM_ARTISTS_NAMES_STRING
            if artists_names_key in dict2:
                album_artists_name_string = dict2[artists_names_key]
                if album_artists_name_string is not None:
                    album_artists_name_list = self._get_artists_name_list_from_string(
                        album_artists_name_string)
                else:
                    album_artists_name_list = None
            else:
                album_artists_name_list = None
            album = Album.get_album_from_name_and_album_artists_name_list_after_eventual_creations(
                user=user, album_name=album_name, album_artists_name_list=album_artists_name_list)

            album_key = LIB_TRACK_ATTRIBUTES_LABEL.ALBUM
            if album is not None:
                dict1[album_key] = album.uuid
            else:
                dict1[album_key] = None
        return dict1

    def _get_dict1_updated_with_genre_uuid_if_genre_name_in_dict2(self,
                                                                  user: User, dict1: QueryDict, dict2: QueryDict):
        genre_name_key = SCHEMA_SAVE_FIELDS.GENRE_NAME
        if genre_name_key in dict2:
            genre_name = dict2[genre_name_key]

            if genre_name in ["", None]:
                genre_uuid = None
            else:
                genreService = GenreService()
                genre_uuid = genreService.get_criteria_from_name_after_having_eventually_created_it(
                    user=user, criteria_name=genre_name).uuid
            dict1[LIB_TRACK_ATTRIBUTES_LABEL.GENRE] = genre_uuid
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

    def _get_dict1_overriden_with_dict2_when_key_is_provided(self, dict1: QueryDict, dict2: QueryDict) -> QueryDict:
        overriden_dict1 = dict1.copy()
        for key in [LIB_TRACK_ATTRIBUTES_LABEL.FILE,
                    LIB_TRACK_ATTRIBUTES_LABEL.TITLE,
                    SCHEMA_SAVE_FIELDS.ARTIST_NAME,
                    SCHEMA_SAVE_FIELDS.ALBUM_NAME,
                    SCHEMA_SAVE_FIELDS.ALBUM_ARTISTS_NAMES_STRING,
                    SCHEMA_SAVE_FIELDS.GENRE_NAME,
                    LIB_TRACK_ATTRIBUTES_LABEL.RATING,
                    LIB_TRACK_ATTRIBUTES_LABEL.LANGUAGE]:
            overriden_dict1 = self.get_querydict1_updated_with_querydict2_key_if_set(
                key=key,
                querydict1=overriden_dict1,
                querydict2=dict2)
        return overriden_dict1

    def _get_post_schema_data_from_extract_schema_data(self, requestData: QueryDict):
        save_data = requestData.copy()
        del save_data[MINE_TRACK_ATTRIBUTES_LABEL.URL]
        return save_data

    def _get_track_filename_with_extension(self, mine_track_url: str, requestData: QueryDict):
        file_extension = self.get_file_extension_from_url(mine_track_url)
        is_filename_randomly_generated = False
        title_key = LIB_TRACK_ATTRIBUTES_LABEL.TITLE
        if title_key in requestData:
            title = requestData[title_key]
            artist_name_key = SCHEMA_SAVE_FIELDS.ARTIST_NAME
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
