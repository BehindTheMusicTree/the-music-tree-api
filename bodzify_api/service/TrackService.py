
import os
import random
import stat
import string
import requests
import tempfile

from bodzify_api.model.user.User import User
from django.core.files.base import File as DjangoFile
from django.db.models import F
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request

from bodzify_api import settings
from bodzify_api.utils.audio_metadata.NormalizedMetadataKeys import NormalizedMetadataKeys
from bodzify_api.utils import audio_metadata, utils
from bodzify_api.utils.app_django_file import AppDjangoFile
from bodzify_api.service.Service import Service
from bodzify_api.model.album.Album import Album
from bodzify_api.model.artist.Artist import Artist
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.criteria.CriteriaType import CriteriaTypesId
from bodzify_api.model.LibTrackPlaylistPositionRel import LibTrackPlaylistPositionRel, \
    Fields as LibTrackPlaylistRelFields
from bodzify_api.model.track.lib.Fields import Fields as ModelFields
from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack
from bodzify_api.serializer.schema.track.input.endpoint.post import Fields as PostFields, LibTrackPostSerializer
from bodzify_api.serializer.schema.track.input.endpoint.put import LibTrackPutSerializer
from bodzify_api.serializer.schema.track.input.endpoint.extract import Fields as ExtractFields
from bodzify_api.serializer.schema.track.input.model import Fields as SaveModelFields, TrackModelSerializer
from bodzify_api.serializer.schema.track.input.schema import Fields as SaveSchemaFields, LibTrackSchemaSerializer


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
    def _decrease_position_of_next_tracks_in_old_track_playlists(user: User, playlists_with_old_position: list):
        for playlist_uuid, old_position in playlists_with_old_position:
            lib_track_position_relations_to_update = LibTrackPlaylistPositionRel.objects.filter(
                user=user, base_playlist=playlist_uuid, position__gt=old_position)
            lib_track_position_relations_to_update.update(
                position=F(LibTrackPlaylistRelFields.POSITION) - 1)

    @staticmethod
    def _update_model_data_with_genre_uuid_if_genre_in_schema_data(user: User, model_data: dict, schema_data: dict):
        if SaveSchemaFields.GENRE_UUID in schema_data:
            genre_uuid = schema_data[SaveSchemaFields.GENRE_UUID]

            if genre_uuid == "":
                genre_uuid = None
        else:
            genre_uuid = None
            if SaveSchemaFields.GENRE_NAME in schema_data:
                genre_name = schema_data[SaveSchemaFields.GENRE_NAME]

                if not genre_name or genre_name == "":
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

    def _get_schema_serializer(self, oldinstance, schema_data: dict, request: Request):
        return LibTrackSchemaSerializer(data=schema_data, context={'request': request})

    def _get_model_serializer(self, oldinstance, model_data: dict, partial: bool, request: Request):
        return TrackModelSerializer(instance=oldinstance,
                                    data=model_data,
                                    context={'request': request},
                                    partial=partial)

    def _get_schema_data_from_post_data(self, post_data: dict) -> dict:
        file = post_data[PostFields.FILE]
        schema_data_from_file = self._get_schema_data_from_file(file=file)

        schema_data = schema_data_from_file.copy()
        keys = [SaveSchemaFields.FILE,
                SaveSchemaFields.TRACK_FILE_FINGERPRINT_MUST_BE_UNIQUE,
                SaveSchemaFields.TITLE,
                SaveSchemaFields.ARTISTS_NAMES,
                SaveSchemaFields.ALBUM_NAME,
                SaveSchemaFields.ALBUM_ARTISTS_NAMES,
                SaveSchemaFields.POSITION_IN_ALBUM,
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

    def _get_schema_data_from_put_data(self, put_data: dict, oldinstance=None) -> dict:
        schema_data = put_data.copy()
        Service._update_data1_converting_str_to_int_value_if_set(key=SaveSchemaFields.RATING, data1=schema_data)
        return schema_data

    def _get_model_data_from_schema_data_not_including_user_field(self, user: User,
                                                                  schema_data: dict,
                                                                  oldinstance) -> dict:
        model_data = dict()

        for key in [SaveSchemaFields.TRACK_FILE_FINGERPRINT_MUST_BE_UNIQUE,
                    SaveModelFields.FILE,
                    SaveModelFields.TITLE,
                    SaveModelFields.RATING,
                    SaveModelFields.LANGUAGE,
                    SaveModelFields.ARCHIVED,
                    SaveModelFields.POSITION_IN_ALBUM]:
            self._update_data1_with_key_if_set_in_data2(key=key, data1=model_data, data2=schema_data)

        self._update_model_data_with_artists_uuids_if_artists_names_str_in_schema_data_or_empty_list(
            user=user, model_data=model_data, schema_data=schema_data)
        self._update_model_data_with_album_uuid_if_album_name_in_schema_data(user=user,
                                                                             model_data=model_data,
                                                                             schema_data=schema_data)
        self._update_model_data_with_genre_uuid_if_genre_in_schema_data(user=user,
                                                                        model_data=model_data,
                                                                        schema_data=schema_data)

        return model_data

    def _update_model_data_with_album_uuid_if_album_name_in_schema_data(self,
                                                                        user: User,
                                                                        model_data: dict,
                                                                        schema_data: dict):
        if SaveSchemaFields.ALBUM_NAME in schema_data:
            album_name = schema_data[SaveSchemaFields.ALBUM_NAME]

            if not album_name:
                return None

            if SaveSchemaFields.ALBUM_ARTISTS_NAMES in schema_data:
                album_artists_names_str = schema_data[SaveSchemaFields.ALBUM_ARTISTS_NAMES]
                if album_artists_names_str:
                    album_artists_name_list = Artist._get_artists_names_list_from_str(names_str=album_artists_names_str)
                else:
                    album_artists_name_list = []
            else:
                album_artists_name_list = []

            album = Album.get_album_from_name_and_album_artists_names_list_after_eventual_creations(
                user=user, album_name=album_name, album_artists_names_list=album_artists_name_list)

            model_data[SaveModelFields.ALBUM] = album.uuid if album else None

    def _get_post_data_from_extract_data(self, extract_data: dict):
        save_data = extract_data.copy()
        del save_data[ExtractFields.URL]
        return save_data

    def _get_track_filename_with_extension(self, mine_track_url: str, data: dict):
        file_extension = self._get_file_extension_from_url(mine_track_url)
        is_filename_randomly_generated = False
        if SaveSchemaFields.TITLE in data:
            title = data[SaveSchemaFields.TITLE]
            if SaveSchemaFields.ARTISTS_NAMES in data:
                artist_name = data[SaveSchemaFields.ARTISTS_NAMES]
                if artist_name is None or artist_name == "":
                    filename_without_extension = title
                else:
                    filename_without_extension = artist_name + " - " + title
            else:
                filename_without_extension = title
            filename_with_extension = filename_without_extension + "." + file_extension
        else:
            filename_with_extension = self._get_substring_after_last_slash(mine_track_url)
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
            raise ValidationError({ModelFields.TRACK_FILE_USER_FRIENDLY: [
                f"Error while extracting metadata from file: {error}"]})

        save_data_with_potential_none = self._get_copy_of_dict_including_only_specified_keys(
            dict=normalized_metadata,
            keys=[NormalizedMetadataKeys.TITLE,
                  NormalizedMetadataKeys.ARTISTS_NAMES,
                  NormalizedMetadataKeys.ALBUM_NAME,
                  NormalizedMetadataKeys.ALBUM_ARTISTS_NAMES,
                  NormalizedMetadataKeys.GENRE_NAME,
                  NormalizedMetadataKeys.RATING,
                  NormalizedMetadataKeys.LANGUAGE])

        save_data_clean = self._remove_none_or_empty_key_from_dict(save_data_with_potential_none)
        save_data_clean[SaveSchemaFields.FILE] = file

        return save_data_clean

    def _update_model_data_with_artists_uuids_if_artists_names_str_in_schema_data_or_empty_list(
            self, user: User, model_data: dict, schema_data: dict):
        if SaveSchemaFields.ARTISTS_NAMES in schema_data:
            artists_names_str = schema_data[SaveSchemaFields.ARTISTS_NAMES]
            if artists_names_str:
                artists = Artist.get_artists_list_from_names_str_after_eventual_creation(
                    user=user, artists_names_str=artists_names_str)
                artists_uuids = [artist.uuid for artist in artists]
            else:
                artists_uuids = []
        else:
            artists_uuids = []
        model_data[SaveModelFields.ARTISTS] = artists_uuids

    def extract(self, request: Request, extract_data_validated: dict):
        mine_track_url = extract_data_validated[ExtractFields.URL]
        track_filename, is_filename_randomly_generated = self._get_track_filename_with_extension(
            mine_track_url=mine_track_url, data=extract_data_validated)

        # stream=True makes it more effective for large files.
        track_file_streamed = requests.get(mine_track_url, stream=True)

        with tempfile.NamedTemporaryFile(delete=True, dir=settings.FILE_UPLOAD_TEMP_DIR) as track_temp_file:
            for block in track_file_streamed.iter_content(1024 * 8):
                if not block:
                    break
                track_temp_file.write(block)
            track_temp_file.flush()
            track_temp_file.seek(0)

            os.chmod(track_temp_file.name, stat.S_IRWXU | stat.S_IRWXG | stat.S_IROTH | stat.S_IXOTH)

            post_data = self._get_post_data_from_extract_data(extract_data_validated)
            post_data[PostFields.FILE] = AppDjangoFile(file=track_temp_file,
                                                       name=track_filename,
                                                       file_abs_path=track_temp_file.name)
            force_title_generation_str = str(is_filename_randomly_generated)
            post_data[SaveSchemaFields.FORCE_TITLE_GENERATION] = force_title_generation_str
            library_track = self.post(post_data_validated=post_data, request=request)

        return library_track

    def post(self, request: Request, post_data_validated: dict):
        user = request.user

        schema_data = self._get_schema_data_from_post_data(post_data=post_data_validated)
        schema_serializer = self._get_schema_serializer(oldinstance=None, schema_data=schema_data, request=request)
        schema_serializer.is_valid(raise_exception=True)

        model_data = self._get_model_data_from_schema_data_not_including_user_field(user=user,
                                                                                    schema_data=schema_data,
                                                                                    oldinstance=None)
        model_data[SaveModelFields.USER] = user.pk

        model_serializer = self._get_model_serializer(oldinstance=None,
                                                      model_data=model_data,
                                                      request=request,
                                                      partial=False,)
        model_serializer.is_valid(raise_exception=True)
        return model_serializer.save()

    def update(self, instance: LibraryTrack, put_data: dict, request: Request):
        user = request.user

        schema_data = self._get_schema_data_from_put_data(put_data=put_data, oldinstance=instance)
        schema_serializer = self._get_schema_serializer(oldinstance=instance, schema_data=schema_data, request=request)
        schema_serializer.is_valid(raise_exception=True)

        model_data = self._get_model_data_from_schema_data_not_including_user_field(
            user=user, schema_data=schema_data, oldinstance=instance)

        model_serializer = self._get_model_serializer(oldinstance=instance,
                                                      model_data=model_data,
                                                      request=request,
                                                      partial=True)
        model_serializer.is_valid(raise_exception=True)
        return model_serializer.save()
