#!/usr/bin/env python

import binascii
import os
import stat
import random
import string
import requests
import tempfile

from django.contrib.auth.models import User
from django.db.models import F
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.uploadedfile import TemporaryUploadedFile
from django.core.files.base import File as DjangoFile
from rest_framework.exceptions import ValidationError

from bodzify_api import settings
from bodzify_api.service.MusicBrainzService import MusicBrainzService
from bodzify_api.utils import utils
from bodzify_api.utils.app_django_file import AppDjangoFile
from bodzify_api.utils import audio_fingerprinter_api_client
from bodzify_api.utils.audio_fingerprinter_api_client import AudioFingerprinterApiClient, AudioFingerprinterError
from bodzify_api.utils import audio_metadata
from bodzify_api.service.Service import Service
from bodzify_api.model.track_file.FingerprintingErrorCode import FingerprintingErrorCodes
from bodzify_api.model.Artist import Artist
from bodzify_api.model.PlaylistLibTrackRelation \
    import PlaylistLibTrackRelation, AttributesLabels as PlaylistLibTrackRelAttributesLabels
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.criteria.CriteriaType import CriteriaTypesId
from bodzify_api.model.Album import Album
from bodzify_api.model.track.LibraryTrack import AttributesLabels as LibTrackAttributesLabels
from bodzify_api.serializer.track.input.endpoint.post import LibTrackPostSerializer, Fields as PostFields
from bodzify_api.serializer.track.input.model import Fields as SaveModelFields, TrackModelSerializer
from bodzify_api.serializer.track_file.input.schema import TrackFileSchemaSerializer, Fields as TrackFIleSchemaFields
from bodzify_api.serializer.track_file.input.model import TrackFileModelSerializer, Fields as TrackFileModelFields
from bodzify_api.serializer.track.input.schema import Fields as SaveSchemaFields, LibTrackSchemaSerializer
from bodzify_api.serializer.track.input.endpoint.put import LibTrackPutSerializer
from bodzify_api.serializer.mine.track.detailed import Fields as MineTrackFields


class TrackService(Service):

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
    def _get_generated_title_from_data(file: DjangoFile, data: dict):
        filename = os.path.basename(file.name).rsplit('.', 1)[0]
        filename_without_expressions_to_exclude = utils.remove_substrings_from_string(
            string_a=filename, substrings=settings.LIB_TRACK_FILENAME_EXPRESSIONS_TO_EXCLUDE_GENERATING_TITLE)
        if SaveSchemaFields.FORCE_TITLE_GENERATION in data:
            force_title_generation = data[SaveSchemaFields.FORCE_TITLE_GENERATION]
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
                position=F(PlaylistLibTrackRelAttributesLabels.POSITION) - 1)

    @staticmethod
    def _get_fingerprint_and_duration_from_file(user_id: str, file, title: str) -> tuple[bytes, int]:
        if isinstance(file, InMemoryUploadedFile):
            with tempfile.NamedTemporaryFile(delete=False, dir=settings.FILE_UPLOAD_TEMP_DIR) as tmp_file:
                for chunk in file.chunks():
                    tmp_file.write(chunk)
                file_path = tmp_file.name
                filename = os.path.basename(file_path)
                fingerprint, duration_in_sec = \
                    AudioFingerprinterApiClient.post_fingerprint_audio(filename=filename, title=title, user_id=user_id)
                os.remove(file_path)
        elif isinstance(file, TemporaryUploadedFile):
            file_path = file.file.name
            filename = os.path.basename(file_path)
            fingerprint, duration_in_sec = AudioFingerprinterApiClient.post_fingerprint_audio(
                user_id=user_id, filename=filename, title=title)
        elif isinstance(file, AppDjangoFile):
            filename = os.path.basename(file.file_abs_path)
            fingerprint, duration_in_sec = AudioFingerprinterApiClient.post_fingerprint_audio(
                user_id=user_id, filename=filename, title=title)

        return fingerprint, int(duration_in_sec)

    @staticmethod
    def _update_model_data_with_track_file_id_and_duration_and_music_brainz_recording_id_if_file_in_schema_data(
            user: User, save_data: dict, schema_data: dict):
        schema_file_key = SaveSchemaFields.FILE
        if schema_file_key in schema_data:
            track_file = schema_data[schema_file_key]
            track_file_schema_data = dict()
            track_file_schema_data[TrackFIleSchemaFields.FILE] = track_file

            duration_in_sec = None
            fingerprinting_error_code_pk = None
            try:
                # It could have been done in the TrackFile model but as duration_in_sec is a fields from the LibraryTrack
                # model, doing it here enables to calculate it only once.
                fingerprint, duration_in_sec = TrackService._get_fingerprint_and_duration_from_file(
                    user_id=user.pk, file=track_file, title=schema_data.get(SaveSchemaFields.TITLE, None))
                save_data[SaveModelFields.DURATION_IN_SEC] = duration_in_sec

                track_file_schema_data[TrackFIleSchemaFields.FINGERPRINT_CHAR] = binascii.hexlify(
                    fingerprint).decode()

                schema_should_cancel_if_duplicate_fingerprint_key = \
                    SaveSchemaFields.SHOULD_CANCEL_IF_DUPLICATE_FINGERPRINT
                if schema_should_cancel_if_duplicate_fingerprint_key in schema_data:
                    track_file_schema_data[TrackFIleSchemaFields.SHOULD_CANCEL_IF_DUPLICATE_FINGERPRINT] = \
                        schema_data[SaveSchemaFields.SHOULD_CANCEL_IF_DUPLICATE_FINGERPRINT]

                MusicBrainzService.update_data_with_musicbrainz_recording_pk_from_fingerprint_and_duration_if_found(
                    data=save_data,
                    data_recording_key=SaveModelFields.MUSICBRAINZ_RECORDING,
                    data_lookup_error_key=SaveModelFields.MUSICBRAINZ_RECORDING_LOOKUP_ERROR_STR,
                    fingerprint=fingerprint,
                    duration_in_sec=duration_in_sec)

            except AudioFingerprinterError as e:
                fingerprint = None
                error_class = e.__class__
                if error_class == audio_fingerprinter_api_client.WrongFileExtension:
                    fingerprinting_error_code_pk = FingerprintingErrorCodes.WRONG_FILE_EXTENSION
                elif error_class == audio_fingerprinter_api_client.WrongFileType:
                    fingerprinting_error_code_pk = FingerprintingErrorCodes.WRONG_FILE_TYPE
                elif error_class == audio_fingerprinter_api_client.FileNotInPool:
                    fingerprinting_error_code_pk = FingerprintingErrorCodes.FILE_NOT_FOUND_IN_POOL
                elif error_class == audio_fingerprinter_api_client.BadRequestError:
                    fingerprinting_error_code_pk = FingerprintingErrorCodes.UNKNOWN_BAD_REQUEST
                elif error_class == audio_fingerprinter_api_client.InternalServerError:
                    fingerprinting_error_code_pk = FingerprintingErrorCodes.INTERNAL_ERROR
                elif error_class == audio_fingerprinter_api_client.TimeoutError:
                    fingerprinting_error_code_pk = FingerprintingErrorCodes.TIMEOUT_ERROR
                elif error_class == audio_fingerprinter_api_client.FpcalcStatusError:
                    fingerprinting_error_code_pk = FingerprintingErrorCodes.FPCALC_ERROR_WITH_STATUS_2
                elif error_class == audio_fingerprinter_api_client.UnknownUnprocessableEntityError:
                    fingerprinting_error_code_pk = FingerprintingErrorCodes.UNKNOWN_UNPROCESSABLE_ENTITY_ERROR
                elif error_class == audio_fingerprinter_api_client.ServiceNotFoundError:
                    fingerprinting_error_code_pk = FingerprintingErrorCodes.SERVICE_NOT_FOUND
                elif error_class == audio_fingerprinter_api_client.ConnectionError:
                    fingerprinting_error_code_pk = FingerprintingErrorCodes.UNKNOWN_CONNEXION_ERROR
                track_file_schema_data[TrackFIleSchemaFields.FINGERPRINTING_ERROR_CODE] = fingerprinting_error_code_pk

            track_file_schema_serializer = TrackFileSchemaSerializer(
                data=track_file_schema_data, context={'user': user})
            track_file_schema_serializer.is_valid(raise_exception=True)

            track_file_model_data = dict()
            track_file_model_data[TrackFileModelFields.USER] = user.pk
            track_file_model_data[TrackFileModelFields.FILE] = track_file_schema_data[TrackFIleSchemaFields.FILE]
            if fingerprint:
                track_file_model_data[TrackFileModelFields.FINGERPRINT] = fingerprint
            if fingerprinting_error_code_pk is not None:
                track_file_model_data[TrackFileModelFields.FINGERPRINTING_ERROR_CODE] = fingerprinting_error_code_pk

            track_file_model_serializer = TrackFileModelSerializer(data=track_file_model_data)
            track_file_model_serializer.is_valid(raise_exception=True)
            track_file = track_file_model_serializer.save(user=user)
            save_data[SaveModelFields.TRACK_FILE] = track_file.pk  # type: ignore

            if duration_in_sec:
                save_data[SaveModelFields.DURATION_IN_SEC] = duration_in_sec

    @ staticmethod
    def _update_model_data_with_genre_uuid_if_genre_in_schema_data(user: User, model_data: dict, schema_data: dict):
        genre_uuid_key = SaveSchemaFields.GENRE_UUID
        if genre_uuid_key in schema_data:
            genre_uuid = schema_data[genre_uuid_key]

            if genre_uuid in ["", None]:
                genre_uuid = None
        else:
            genre_name_key = SaveSchemaFields.GENRE_NAME
            genre_uuid = None
            if genre_name_key in schema_data:
                genre_name = schema_data[genre_name_key]

                if genre_name in ["", None]:
                    genre_uuid = None
                else:
                    criteria, _ = Criteria.objects.get_or_create(user=user,
                                                                 type_id=CriteriaTypesId.GENRE,
                                                                 name=genre_name)
                    genre_uuid = criteria.uuid
            else:
                return

        model_data[SaveModelFields.GENRE] = genre_uuid

        return

    def _get_post_serializer(self, post_data: dict):
        return LibTrackPostSerializer(data=post_data)

    def _get_put_serializer(self, old_instance, put_data: dict):
        return LibTrackPutSerializer(instance=old_instance, data=put_data)

    def _get_schema_serializer(self, old_instance, schema_data: dict, request):
        return LibTrackSchemaSerializer(data=schema_data, context={'request': request})

    def _get_model_serializer(self, old_instance, model_data: dict, partial: bool):
        return TrackModelSerializer(instance=old_instance, data=model_data, partial=True)

    def _get_schema_data_from_post_data(self, post_data: dict) -> dict:
        file = post_data[PostFields.TRACK_FILE]
        schema_data_from_file = self._get_schema_data_from_file(file=file)

        schema_data = schema_data_from_file.copy()
        keys = [SaveSchemaFields.FILE,
                SaveSchemaFields.SHOULD_CANCEL_IF_DUPLICATE_FINGERPRINT,
                SaveSchemaFields.TITLE,
                SaveSchemaFields.ARTIST_NAME,
                SaveSchemaFields.ALBUM_NAME,
                SaveSchemaFields.ALBUM_ARTISTS_NAMES_STR,
                SaveSchemaFields.GENRE_UUID,
                SaveSchemaFields.RATING,
                SaveSchemaFields.LANGUAGE]
        self._override_data1_with_data2_values_for_each_key_in_data2(data1=schema_data, data2=post_data, keys=keys)

        if SaveSchemaFields.TITLE not in schema_data:
            schema_data[SaveSchemaFields.TITLE] = self._get_generated_title_from_data(file=file, data=post_data)
        if SaveSchemaFields.GENRE_UUID not in post_data:
            self._override_data1_with_data2_values_for_each_key_in_data2(data1=schema_data,
                                                                         data2=post_data,
                                                                         keys=[SaveSchemaFields.GENRE_NAME])

        Service._update_data1_converting_str_to_int_value_if_set(key=SaveSchemaFields.RATING, data1=schema_data)
        return schema_data

    def _get_schema_data_from_put_data(self, put_data: dict, old_instance=None) -> dict:
        schema_data = put_data.copy()
        Service._update_data1_converting_str_to_int_value_if_set(key=SaveSchemaFields.RATING, data1=schema_data)
        return schema_data

    def _get_model_data_from_schema_data_not_including_user_field(self, user: User,
                                                                  schema_data: dict,
                                                                  old_instance) -> dict:
        model_data = dict()

        for key in [SaveSchemaFields.SHOULD_CANCEL_IF_DUPLICATE_FINGERPRINT,
                    SaveModelFields.TITLE,
                    SaveModelFields.RATING,
                    SaveModelFields.LANGUAGE,
                    SaveModelFields.ARCHIVED]:
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
        model_data_album_key = SaveModelFields.ALBUM
        schema_data_album_name_key = SaveSchemaFields.ALBUM_NAME
        model_data_artists_names_key = SaveSchemaFields.ALBUM_ARTISTS_NAMES_STR

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
        del save_data[MineTrackFields.URL]
        return save_data

    def _get_track_filename_with_extension(self, mine_track_url: str, data: dict):
        file_extension = self._get_file_extension_from_url(mine_track_url)
        is_filename_randomly_generated = False
        title_key = SaveSchemaFields.TITLE
        if title_key in data:
            title = data[title_key]
            artist_name_key = SaveSchemaFields.ARTIST_NAME
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
            raise ValidationError({LibTrackAttributesLabels.TRACK_FILE_USER_FRIENDLY: [
                f"Error while extracting metadata from file: {error}"]})

        save_data_with_potential_none = self._get_copy_of_dict_including_only_specified_keys(
            dict=normalized_metadata,
            keys=[SaveSchemaFields.TITLE,
                  SaveSchemaFields.ARTIST_NAME,
                  SaveSchemaFields.ALBUM_NAME,
                  SaveSchemaFields.ALBUM_ARTISTS_NAMES_STR,
                  SaveSchemaFields.GENRE_NAME,
                  SaveSchemaFields.RATING,
                  SaveSchemaFields.LANGUAGE])
        save_data_clean = self._remove_none_or_empty_key_from_dict(save_data_with_potential_none)
        save_data_clean[SaveSchemaFields.FILE] = file

        return save_data_clean

    def _update_model_data_with_artist_uuid_if_artist_name_in_schema_data(
            self, user: User, model_data: dict, schema_data: dict):
        data2_artist_name_key = SaveSchemaFields.ARTIST_NAME
        data1_artist_key = SaveModelFields.ARTIST
        if data2_artist_name_key in schema_data:
            artist_name = schema_data[data2_artist_name_key]
            artist = Artist.get_artist_from_name_after_eventual_creation(user=user, artist_name=artist_name)
            if artist is not None:
                model_data[data1_artist_key] = artist.uuid
            else:
                model_data[data1_artist_key] = None

    def extract(self, extract_data: dict, request):
        mine_track_url = extract_data[MineTrackFields.URL]
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
            post_data[PostFields.TRACK_FILE] = AppDjangoFile(file=track_temp_file,
                                                             name=track_filename,
                                                             file_abs_path=track_temp_file.name)
            force_title_generation_str = str(is_filename_randomly_generated)
            post_data[SaveSchemaFields.FORCE_TITLE_GENERATION] = force_title_generation_str
            library_track = self.create(post_data=post_data, request=request)

        return library_track

    def delete(self, user: User, instance):
        old_lib_tracks_playlists_with_positions = instance._get_lib_track_playlists_with_positions()
        instance.delete_with_checking_album_and_artist_potential_deletion()
        TrackService._decrease_position_of_next_tracks_in_old_track_playlists(old_lib_tracks_playlists_with_positions)
