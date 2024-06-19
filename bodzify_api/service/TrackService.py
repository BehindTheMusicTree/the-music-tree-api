#!/usr/bin/env python

import binascii
from calendar import monthrange
import os
import stat
import random
from typing import Optional
import acoustid
import string
import requests
import tempfile
import datetime

from django.contrib.auth.models import User
from django.db.models import F
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.uploadedfile import TemporaryUploadedFile
from django.core.files.base import File as DjangoFile
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError

from bodzify_api.exception.musicbrainz import MusicbrainzException
from bodzify_api.model.Artist import Artist
from bodzify_api.model.musicbrainz.MusicbrainzArtist \
    import MusicbrainzArtist, ATTRIBUTES_LABEL as MUSICBRAINZ_ARTIST_ATTRIBUTES_LABEL
from bodzify_api.model.musicbrainz.MusicbrainzRecording import MusicbrainzRecording
from bodzify_api.settings import settings
from bodzify_api.utils.audio_fingerprinter_api_client \
    import AudioFingerprintGeneratorApiClient, AudioFingerprintGeneratorError
import bodzify_api.utils.audio_metadata as audio_metadata
from bodzify_api.service.Service import Service
from bodzify_api.model.PlaylistLibTrackRelation \
    import PlaylistLibTrackRelation, ATTRIBUTES_LABEL as PLAYLIST_LIB_TRACK_REL_ATTRIBUTES_LABEL
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.criteria.CriteriaType import CRITERIA_TYPES_ID
from bodzify_api.model.Album import Album
from bodzify_api.model.track.LibraryTrack import ATTRIBUTES_LABEL as LIB_TRACK_ATTRIBUTE_LABEL
from bodzify_api.serializer.track.input.endpoint.post \
    import LibTrackPostSerializer, FIELDS as POST_FIELDS
from bodzify_api.serializer.track.input.model \
    import FIELDS as SAVE_MODEL_FIELDS, TrackModelSerializer
from bodzify_api.serializer.track_file.input.schema \
    import TrackFileSchemaSerialazer, FIELDS as TRACK_FILE_SCHEMA_FIELDS
from bodzify_api.serializer.track_file.input.model \
    import TrackFileModelSerializer, FIELDS as TRACK_FILE_MODEL_FIELDS
from bodzify_api.serializer.track.input.schema \
    import FIELDS as SAVE_SCHEMA_FIELDS, LibTrackSchemaSerializer
from bodzify_api.serializer.track.input.endpoint.put import LibTrackPutSerializer
from bodzify_api.serializer.mine.track.detailed import FIELDS as MINE_TRACK_FIELDS
from bodzify_api.utils.utils import AppDjangoFile


class TrackService(Service):

    class MUSICBRAINZ_API:
        class FIELDS:
            RESULTS = 'results'
            RECORDINGS = 'recordings'
            ID = 'id'
            SCORE = 'score'
            ARTISTS = 'artists'
            NAME = 'name'
            TITLE = 'title'
            DATE = 'date'
            DURATION_IN_SEC = 'duration'
            RELEASEGROUPS = 'releasegroups'
            RELEASES = 'releases'
            DATE = 'date'
            DAY = 'day'
            MONTH = 'month'
            YEAR = 'year'
            ERROR = 'error'
            STATUS = 'status'
            CODE = 'code'
            MESSAGE = 'message'

        class VALUES:
            class STATUS:
                OK = 'ok'
                ERROR = 'error'

    @staticmethod
    def _generate_short_uu(length: int):
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))

    @staticmethod
    def _get_substring_after_last_slash(string: str):
        return string.split("/")[-1]

    @staticmethod
    def _get_file_extension_from_url(url: str):
        return url.split(".")[-1]

    @staticmethod
    def remove_substrings_from_string(string_a: str, substrings: list) -> str:
        for substring in substrings:
            string_a = string_a.replace(substring, '')
        return string_a

    @staticmethod
    def _get_generated_title_from_data(file: DjangoFile, data: dict):
        filename = os.path.basename(file.name).rsplit('.', 1)[0]
        filename_without_expressions_to_exclude = TrackService.remove_substrings_from_string(
            string_a=filename, substrings=settings.LIB_TRACK_FILENAME_EXPRESSIONS_TO_EXCLUDE_GENERATING_TITLE)
        if SAVE_SCHEMA_FIELDS.FORCE_TITLE_GENERATION in data:
            force_title_generation = data[SAVE_SCHEMA_FIELDS.FORCE_TITLE_GENERATION]
        else:
            force_title_generation = False

        if len(filename_without_expressions_to_exclude) > settings.LIB_TRACK_FILENAME_LEN_MAX or force_title_generation:
            title = settings.LIB_TRACK_GENERATED_TITLE_PREFIXE + \
                TrackService._generate_short_uu(settings.LIB_TRACK_GENERATED_TITLE_LENGTH -
                                                len(settings.LIB_TRACK_GENERATED_TITLE_PREFIXE))
        else:
            title = filename_without_expressions_to_exclude
        return title

    @staticmethod
    def _decrease_position_of_next_tracks_in_old_track_playlists(playlists_with_old_position: list):
        for playlist_uuid, old_position in playlists_with_old_position:
            playlist_lib_track_relations_to_update = PlaylistLibTrackRelation.objects.filter(
                base_playlist__uuid=playlist_uuid, position__gt=old_position)
            playlist_lib_track_relations_to_update.update(
                position=F(PLAYLIST_LIB_TRACK_REL_ATTRIBUTES_LABEL.POSITION) - 1)

    @staticmethod
    def _get_fingerprint_and_duration_from_file(file) -> tuple[bytes, int]:
        if isinstance(file, InMemoryUploadedFile):
            with tempfile.NamedTemporaryFile(delete=False, dir=settings.FILE_UPLOAD_TEMP_DIR) as tmp_file:
                for chunk in file.chunks():
                    tmp_file.write(chunk)
                file_path = tmp_file.name
                filename = os.path.basename(file_path)
                fingerprint, duration_in_sec = \
                    AudioFingerprintGeneratorApiClient.post_fingerprint_audio(filename=filename)
                os.remove(file_path)
        elif isinstance(file, TemporaryUploadedFile):
            file_path = file.file.name
            filename = os.path.basename(file_path)
            fingerprint, duration_in_sec = \
                AudioFingerprintGeneratorApiClient.post_fingerprint_audio(filename=filename)
        elif isinstance(file, AppDjangoFile):
            filename = os.path.basename(file.file_abs_path)
            fingerprint, duration_in_sec = AudioFingerprintGeneratorApiClient.post_fingerprint_audio(
                filename=filename)

        return fingerprint, int(duration_in_sec)

    @staticmethod
    def _update_model_data_with_track_file_id_and_duration_and_music_brainz_recording_id_if_file_in_schema_data(
            user: User, save_data: dict, schema_data: dict):
        schema_file_key = SAVE_SCHEMA_FIELDS.FILE
        if schema_file_key in schema_data:
            file = schema_data[schema_file_key]
            file_schema_data = dict()
            file_schema_data[TRACK_FILE_SCHEMA_FIELDS.FILE] = file

            duration_in_sec = None
            try:
                # It could have been done in the TrackFile model but as duration_in_sec is a fields from the LibraryTrack
                # model, doing it here enables to calculate it only once.
                fingerprint, duration_in_sec = TrackService._get_fingerprint_and_duration_from_file(file=file)
                save_data[SAVE_MODEL_FIELDS.DURATION_IN_SEC] = duration_in_sec

                file_schema_data[TRACK_FILE_SCHEMA_FIELDS.FINGERPRINT_CHAR] = binascii.hexlify(fingerprint).decode()

                schema_should_cancel_if_duplicate_fingerprint_key = SAVE_SCHEMA_FIELDS.SHOULD_CANCEL_IF_DUPLICATE_FINGERPRINT
                if schema_should_cancel_if_duplicate_fingerprint_key in schema_data:
                    file_schema_data[TRACK_FILE_SCHEMA_FIELDS.SHOULD_CANCEL_IF_DUPLICATE_FINGERPRINT] = \
                        schema_data[SAVE_SCHEMA_FIELDS.SHOULD_CANCEL_IF_DUPLICATE_FINGERPRINT]

                TrackService._update_data_with_musicbrainz_recording_pk_from_fingerprint_and_duration_if_found(
                    data=save_data, fingerprint=fingerprint, duration_in_sec=duration_in_sec)
            except AudioFingerprintGeneratorError as audio_fingerprint_generation_error:
                fingerprint = None

            file_schema_serializer = TrackFileSchemaSerialazer(data=file_schema_data)
            file_schema_serializer.is_valid(raise_exception=True)

            file_model_data = dict()
            file_model_data[TRACK_FILE_MODEL_FIELDS.USER] = user.pk
            file_model_data[TRACK_FILE_MODEL_FIELDS.FILE] = file_schema_data[TRACK_FILE_SCHEMA_FIELDS.FILE]
            file_model_data[TRACK_FILE_MODEL_FIELDS.FINGERPRINT] = fingerprint

            file_model_serializer = TrackFileModelSerializer(data=file_model_data)
            file_model_serializer.is_valid(raise_exception=True)
            file = file_model_serializer.save(user=user)
            save_data[SAVE_MODEL_FIELDS.TRACK_FILE] = file.pk  # type: ignore

            if duration_in_sec:
                save_data[SAVE_MODEL_FIELDS.DURATION_IN_SEC] = duration_in_sec

    @ staticmethod
    def _update_model_data_with_genre_uuid_if_genre_in_schema_data(user: User, model_data: dict, schema_data: dict):
        genre_uuid_key = SAVE_SCHEMA_FIELDS.GENRE_UUID
        if genre_uuid_key in schema_data:
            genre_uuid = schema_data[genre_uuid_key]

            if genre_uuid in ["", None]:
                genre_uuid = None
        else:
            genre_name_key = SAVE_SCHEMA_FIELDS.GENRE_NAME
            genre_uuid = None
            if genre_name_key in schema_data:
                genre_name = schema_data[genre_name_key]

                if genre_name in ["", None]:
                    genre_uuid = None
                else:
                    criteria, _ = Criteria.objects.get_or_create(user=user,
                                                                 type_id=CRITERIA_TYPES_ID.GENRE,
                                                                 name=genre_name)
                    genre_uuid = criteria.uuid
            else:
                return

        model_data[SAVE_MODEL_FIELDS.GENRE] = genre_uuid

        return

    @ staticmethod
    def get_best_recording_dict_with_score(recordings_grouped_by_score, duration_in_sec):
        def rate_groupe_of_recordings_by_score(group_of_recordings):
            return group_of_recordings[TrackService.MUSICBRAINZ_API.FIELDS.SCORE]

        def rate_recording_by_similar_duration_and_by_number_of_fields(recording):
            DURATION_FAKE_VALUE_IF_NOT_SET_IN_ORDER_TO_RANK_LAST = 1000000000
            duration_difference = abs(
                recording.get(
                    TrackService.MUSICBRAINZ_API.FIELDS.DURATION_IN_SEC,
                    DURATION_FAKE_VALUE_IF_NOT_SET_IN_ORDER_TO_RANK_LAST) - duration_in_sec)
            fields_count = len(recording)
            release_groups_count = len(recording.get(TrackService.MUSICBRAINZ_API.FIELDS.RELEASEGROUPS, []))
            return duration_difference, -fields_count, -release_groups_count

        best_group_of_recordings = max(recordings_grouped_by_score, key=rate_groupe_of_recordings_by_score)
        best_recordings = best_group_of_recordings[TrackService.MUSICBRAINZ_API.FIELDS.RECORDINGS]
        best_recording = min((recording for recording in best_recordings),
                             key=rate_recording_by_similar_duration_and_by_number_of_fields)
        best_recording[TrackService.MUSICBRAINZ_API.FIELDS.SCORE] = best_group_of_recordings[TrackService.MUSICBRAINZ_API.FIELDS.SCORE]
        return best_recording

    @ staticmethod
    def _get_musicbrainz_best_recording_dict_from_fingerprint_and_duration(fingerprint: str,
                                                                           duration_in_sec: float) -> Optional[dict]:
        try:
            lookup = acoustid.lookup(apikey=settings.ACOUSTID_API_KEY,
                                     fingerprint=fingerprint,
                                     duration=duration_in_sec,
                                     meta=['recordings', 'releasegroups', 'releases', 'compress', 'tracks'])
            if lookup[TrackService.MUSICBRAINZ_API.FIELDS.STATUS] == TrackService.MUSICBRAINZ_API.VALUES.STATUS.OK:
                recordings_grouped_by_score = lookup[TrackService.MUSICBRAINZ_API.FIELDS.RESULTS]
                if len(recordings_grouped_by_score) > 0:
                    return TrackService.get_best_recording_dict_with_score(
                        recordings_grouped_by_score=recordings_grouped_by_score, duration_in_sec=duration_in_sec)
                else:
                    return None
            elif lookup[TrackService.MUSICBRAINZ_API.FIELDS.STATUS] == TrackService.MUSICBRAINZ_API.VALUES.STATUS.ERROR:
                error_dict = lookup[TrackService.MUSICBRAINZ_API.FIELDS.ERROR]
                error_code = error_dict[TrackService.MUSICBRAINZ_API.FIELDS.CODE]
                error_message = error_dict[TrackService.MUSICBRAINZ_API.FIELDS.MESSAGE]
                exception_message = f"Error while getting musicbrainz recording ID: {error_code} - {error_message}"
                print(exception_message)
                raise MusicbrainzException(exception_message)
            else:
                raise MusicbrainzException("Unknown error while getting musicbrainz recording ID")
        except Exception as exception:
            raise MusicbrainzException(str(exception))

    @ staticmethod
    def __get_earliest_release_date_from_musicbrainz_recording_dict(musicbrainz_recording_dict):
        earliest_comparison_date = None
        earliest_release_date = None
        for releasegroup in musicbrainz_recording_dict.get(TrackService.MUSICBRAINZ_API.FIELDS.RELEASEGROUPS, []):
            for release in releasegroup.get(TrackService.MUSICBRAINZ_API.FIELDS.RELEASES, []):
                current_release_date = release.get(TrackService.MUSICBRAINZ_API.FIELDS.DATE, None)
                if current_release_date:
                    year = current_release_date.get(TrackService.MUSICBRAINZ_API.FIELDS.YEAR)
                    month_or_12 = current_release_date.get(TrackService.MUSICBRAINZ_API.FIELDS.MONTH, 12)
                    month_or_1 = current_release_date.get(TrackService.MUSICBRAINZ_API.FIELDS.MONTH, 1)
                    _, last_day = monthrange(year, month_or_12)
                    day_or_last_of_month = current_release_date.get(
                        TrackService.MUSICBRAINZ_API.FIELDS.DAY, last_day)
                    day_or_first = current_release_date.get(TrackService.MUSICBRAINZ_API.FIELDS.DAY, 1)

                    comparison_date_obj = datetime.date(year=year, month=month_or_12, day=day_or_last_of_month)

                    if not earliest_comparison_date or comparison_date_obj < earliest_comparison_date:
                        earliest_comparison_date = comparison_date_obj
                        earliest_release_date = datetime.date(year=year, month=month_or_1, day=day_or_first)
        return earliest_release_date

    @staticmethod
    def __create_musicbrainz_recording_instance_from_dict(musicbrainz_recording_uuid: str,
                                                          musicbrainz_recording_dict: dict) -> MusicbrainzRecording:
        musicbrainz_artists_dict = musicbrainz_recording_dict[TrackService.MUSICBRAINZ_API.FIELDS.ARTISTS]
        musicbrainz_artists = list()
        for artist_dict in musicbrainz_artists_dict:
            artist, _ = MusicbrainzArtist.objects.get_or_create(
                uuid=artist_dict[TrackService.MUSICBRAINZ_API.FIELDS.ID],
                defaults={
                    MUSICBRAINZ_ARTIST_ATTRIBUTES_LABEL.NAME: artist_dict[TrackService.MUSICBRAINZ_API.FIELDS.NAME],
                })
            musicbrainz_artists.append(artist)

        earliest_release_date = \
            TrackService.__get_earliest_release_date_from_musicbrainz_recording_dict(musicbrainz_recording_dict)

        musicbrainz_recording = MusicbrainzRecording.objects.create(
            uuid=musicbrainz_recording_uuid,
            score=musicbrainz_recording_dict[TrackService.MUSICBRAINZ_API.FIELDS.SCORE],
            title=musicbrainz_recording_dict[TrackService.MUSICBRAINZ_API.FIELDS.TITLE],
            duration_in_sec=musicbrainz_recording_dict[TrackService.MUSICBRAINZ_API.FIELDS.DURATION_IN_SEC],
            release_date=earliest_release_date)
        musicbrainz_recording.musicbrainz_artists.set(musicbrainz_artists)
        return musicbrainz_recording

    @staticmethod
    def _update_data_with_musicbrainz_recording_pk_from_fingerprint_and_duration_if_found(data: dict,
                                                                                          fingerprint: bytes,
                                                                                          duration_in_sec: float):
        try:
            musicbrainz_recording_dict = TrackService._get_musicbrainz_best_recording_dict_from_fingerprint_and_duration(
                fingerprint=fingerprint, duration_in_sec=duration_in_sec)  # type: ignore
            if musicbrainz_recording_dict:
                musicbrainz_recording_uuid = musicbrainz_recording_dict[TrackService.MUSICBRAINZ_API.FIELDS.ID]
                try:
                    musicbrainz_recording_pk = MusicbrainzRecording.objects.get(uuid=musicbrainz_recording_uuid).pk
                except ObjectDoesNotExist:
                    musicbrainz_recording = TrackService.__create_musicbrainz_recording_instance_from_dict(
                        musicbrainz_recording_uuid=musicbrainz_recording_uuid,
                        musicbrainz_recording_dict=musicbrainz_recording_dict)
                    musicbrainz_recording_pk = musicbrainz_recording.pk

                data[SAVE_MODEL_FIELDS.MUSICBRAINZ_RECORDING] = musicbrainz_recording_pk
            data[SAVE_MODEL_FIELDS.MUSICBRAINZ_RECORDING_LOOKUP_HAS_FAILED_WITH_ERRORS] = False

        except MusicbrainzException:
            data[SAVE_MODEL_FIELDS.MUSICBRAINZ_RECORDING_LOOKUP_HAS_FAILED_WITH_ERRORS] = True

    def _get_post_serializer(self, post_data: dict):
        return LibTrackPostSerializer(data=post_data)

    def _get_put_serializer(self, old_instance, put_data: dict):
        return LibTrackPutSerializer(instance=old_instance, data=put_data)

    def _get_schema_serializer(self, old_instance, schema_data: dict, request):
        return LibTrackSchemaSerializer(data=schema_data, context={'request': request})

    def _get_model_serializer(self, old_instance, model_data: dict, partial: bool):
        return TrackModelSerializer(instance=old_instance, data=model_data, partial=True)

    def _get_schema_data_from_post_data(self, post_data: dict) -> dict:
        file = post_data[POST_FIELDS.TRACK_FILE]
        schema_data_from_file = self._get_schema_data_from_file(file=file)

        schema_data = schema_data_from_file.copy()
        keys = [SAVE_SCHEMA_FIELDS.FILE,
                SAVE_SCHEMA_FIELDS.SHOULD_CANCEL_IF_DUPLICATE_FINGERPRINT,
                SAVE_SCHEMA_FIELDS.TITLE,
                SAVE_SCHEMA_FIELDS.ARTIST_NAME,
                SAVE_SCHEMA_FIELDS.ALBUM_NAME,
                SAVE_SCHEMA_FIELDS.ALBUM_ARTISTS_NAMES_STR,
                SAVE_SCHEMA_FIELDS.GENRE_UUID,
                SAVE_SCHEMA_FIELDS.RATING,
                SAVE_SCHEMA_FIELDS.LANGUAGE]
        self._override_data1_with_data2_values_for_each_key_in_data2(data1=schema_data, data2=post_data, keys=keys)

        if SAVE_SCHEMA_FIELDS.TITLE not in schema_data:
            schema_data[SAVE_SCHEMA_FIELDS.TITLE] = self._get_generated_title_from_data(file=file, data=post_data)
        if SAVE_SCHEMA_FIELDS.GENRE_UUID not in post_data:
            self._override_data1_with_data2_values_for_each_key_in_data2(data1=schema_data,
                                                                         data2=post_data,
                                                                         keys=[SAVE_SCHEMA_FIELDS.GENRE_NAME])

        Service._update_data1_converting_str_to_int_value_if_set(key=SAVE_SCHEMA_FIELDS.RATING, data1=schema_data)
        return schema_data

    def _get_schema_data_from_put_data(self, put_data: dict, old_instance=None) -> dict:
        schema_data = put_data.copy()
        Service._update_data1_converting_str_to_int_value_if_set(key=SAVE_SCHEMA_FIELDS.RATING, data1=schema_data)
        return schema_data

    def _get_model_data_from_schema_data_not_including_user_field(self, user: User,
                                                                  schema_data: dict,
                                                                  old_instance) -> dict:
        model_data = dict()

        for key in [SAVE_SCHEMA_FIELDS.SHOULD_CANCEL_IF_DUPLICATE_FINGERPRINT,
                    SAVE_MODEL_FIELDS.TITLE,
                    SAVE_MODEL_FIELDS.RATING,
                    SAVE_MODEL_FIELDS.LANGUAGE]:
            self._update_data1_with_key_if_set_in_data2(key=key, data1=model_data, data2=schema_data)

        self._update_model_data_with_artist_uuid_if_artist_name_in_schema_data(user=user,
                                                                               model_data=model_data,
                                                                               schema_data=schema_data)
        self._update_model_data_with_album_uuid_if_album_name_in_schema_data(user=user,
                                                                             model_data=model_data,
                                                                             schema_data=schema_data)
        self._update_model_data_with_genre_uuid_if_genre_in_schema_data(user=user,
                                                                        model_data=model_data,
                                                                        schema_data=schema_data)
        self._update_model_data_with_track_file_id_and_duration_and_music_brainz_recording_id_if_file_in_schema_data(
            user=user, save_data=model_data, schema_data=schema_data)
        return model_data

    def _update_model_data_with_album_uuid_if_album_name_in_schema_data(self,
                                                                        user: User,
                                                                        model_data: dict,
                                                                        schema_data: dict):
        model_data_album_key = SAVE_MODEL_FIELDS.ALBUM
        schema_data_album_name_key = SAVE_SCHEMA_FIELDS.ALBUM_NAME
        model_data_artists_names_key = SAVE_SCHEMA_FIELDS.ALBUM_ARTISTS_NAMES_STR

        if schema_data_album_name_key in schema_data:
            album_name = schema_data[schema_data_album_name_key]

            if model_data_artists_names_key in schema_data:
                album_artists_name_string = schema_data[model_data_artists_names_key]
                if album_artists_name_string is not None:
                    album_artists_name_list = self._get_artists_name_list_from_string(album_artists_name_string)
                else:
                    album_artists_name_list = None
            else:
                album_artists_name_list = None
            album = Album.get_album_from_name_and_album_artists_name_list_after_eventual_creations(
                user=user, album_name=album_name, album_artists_name_list=album_artists_name_list)

            if album is not None:
                model_data[model_data_album_key] = album.uuid
            else:
                model_data[model_data_album_key] = None

    def _get_artists_name_list_from_string(self, names_string: str) -> list:
        names_with_eventual_spaces_around_and_duplicates = names_string.split(
            audio_metadata.METADATA_ARTISTS_SEPARATION_CHAR)
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
        file_extension = self._get_file_extension_from_url(mine_track_url)
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
            filename_with_extension = self._get_substring_after_last_slash(
                mine_track_url)
            if len(filename_with_extension) > settings.LIB_TRACK_FILENAME_LEN_MAX:
                filename_without_extension = self._generate_short_uu(
                    settings.LIB_TRACK_FILENAME_GENERATED_WITHOUT_EXTENSION_LENGTH - len(file_extension) - 1)
                filename_with_extension = filename_without_extension + "." + file_extension
                is_filename_randomly_generated = True
        return filename_with_extension, is_filename_randomly_generated

    def _get_schema_data_from_file(self, file):
        try:
            normalized_metadata = audio_metadata.get_normalized_metadata_from_file(
                file=file,
                normalized_rating_max_value=settings.LIB_TRACK_RATING_VALUE_MAX)
        except Exception as error:
            raise ValidationError({LIB_TRACK_ATTRIBUTE_LABEL.TRACK_FILE_USER_FRIENDLY: [
                f"Error while extracting metadata from file: {error}"]})

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
        save_data_clean[SAVE_SCHEMA_FIELDS.FILE] = file

        return save_data_clean

    def _update_model_data_with_artist_uuid_if_artist_name_in_schema_data(
            self, user: User, model_data: dict, schema_data: dict):
        data2_artist_name_key = SAVE_SCHEMA_FIELDS.ARTIST_NAME
        data1_artist_key = SAVE_MODEL_FIELDS.ARTIST
        if data2_artist_name_key in schema_data:
            artist_name = schema_data[data2_artist_name_key]
            artist = Artist.get_artist_from_name_after_eventual_creation(user=user, artist_name=artist_name)
            if artist is not None:
                model_data[data1_artist_key] = artist.uuid
            else:
                model_data[data1_artist_key] = None

    def extract(self, extract_data: dict, request):
        mine_track_url = extract_data[MINE_TRACK_FIELDS.URL]
        track_filename, is_filename_randomly_generated = self._get_track_filename_with_extension(
            mine_track_url=mine_track_url, data=extract_data)

        # stream=True more effective for large files
        track_file_streamed = requests.get(mine_track_url, stream=True)

        with tempfile.NamedTemporaryFile(delete=True, dir=settings.FILE_UPLOAD_TEMP_DIR) as track_temp_file:
            for block in track_file_streamed.iter_content(1024 * 8):
                if not block:
                    break
                track_temp_file.write(block)
            track_temp_file.flush()
            track_temp_file.seek(0)

            os.chmod(track_temp_file.name, stat.S_IRWXU | stat.S_IRWXG | stat.S_IROTH | stat.S_IXOTH)

            post_data = self._get_post_data_from_extract_data(extract_data)
            post_data[POST_FIELDS.TRACK_FILE] = AppDjangoFile(file=track_temp_file,
                                                              name=track_filename,
                                                              file_abs_path=track_temp_file.name)
            force_title_generation_str = str(is_filename_randomly_generated)
            post_data[SAVE_SCHEMA_FIELDS.FORCE_TITLE_GENERATION] = force_title_generation_str
            library_track = self.create(post_data=post_data, request=request)

        return library_track

    def delete(self, user: User, instance):
        old_lib_tracks_playlists_with_positions = instance._get_lib_track_playlists_with_positions()
        instance.delete_with_checking_album_and_artist_potential_deletion()
        TrackService._decrease_position_of_next_tracks_in_old_track_playlists(old_lib_tracks_playlists_with_positions)
