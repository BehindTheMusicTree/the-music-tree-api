#!/usr/bin/env python

from urllib.parse import urlencode

from django.http import JsonResponse
from django.urls import reverse
from rest_framework import status

from bodzify_api import AudioMetadataManager
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.test.AppTestCase import AppTestCase
from bodzify_api.serializer.track.input.endpoint.LibTrackExtractSerializer \
    import FIELDS as LIB_TRACK_EXTRACT_FIELDS
from bodzify_api.serializer.track.input.endpoint.LibTrackPostSerializer import FIELDS as LIB_TRACK_POST_FIELDS
from bodzify_api.serializer.track.output.LibTrackDetailedSerializer import FIELDS as LIB_TRACK_GET_FIELDS


class TrackTestCase(AppTestCase):

    class LIB_TRACK_GENERIC_SAMPLES_FILENAMES_WITHOUT_EXTENSION:
        ONE_STAR = "1 star"
        TAGS_NONE = "tags none"
        TAGS_ALBUM_KOKO_WITHOUT_ALBUM_ARTISTS = "tags album koko without album artists"
        TAGS_ALBUM_ARTISTS_KOKO_WITHOUT_ALBUM = "tags album artists koko without album"
        TAGS_MAX_LENGTH_WITH_LETTER_A = "tags max length with letter a"

    class LIB_TRACK_GENERIC_SAMPLES_TAGS_NONE_SIZE_IN_MO:
        WAV = 79 / 1024
        MP3 = 14 / 1024
        FLAC = 51 / 1024

    class SAMPLE_MINE_TRACK_URLS:
        WAV = "http://www.canadianmusicartists.com/sample/fx02.wav"
        MP3 = "https://lasonotheque.org/UPLOAD/mp3/0001.mp3"

    SAMPLE_MINE_TRACK_DEFAULT_URL = SAMPLE_MINE_TRACK_URLS.MP3
    SAMPLE_MINE_TRACK_DEFAULT_EXTENSION = SAMPLE_MINE_TRACK_DEFAULT_URL.split('.')[-1]

    SAMPLE_LIB_TRACK_WAV_DURATION = 0.5453541666666667
    SAMPLE_LIB_TRACK_MP3_DURATION = 0.6
    SAMPLE_LIB_TRACK_FLAC_DURATION = 0.5453541666666667

    saved_lib_track: LibraryTrack
    saved_lib_track_metadata: dict

    def _set_saved_lib_track_attribute(self, response):
        lib_track_uuid = response.json()[LIB_TRACK_GET_FIELDS.UUID]
        self.saved_lib_track = LibraryTrack.objects.get(uuid=lib_track_uuid)
        if self.saved_lib_track.file_obj:
            self.saved_lib_track_metadata = AudioMetadataManager.get_metadata_dict_from_file(
                file=self.saved_lib_track.file_obj.file)

    def extract(self, data_dict):
        data_url_encoded = urlencode(self._replace_none_values_by_empty_string(data_dict), doseq=True)
        response = self.api_client.post(path=reverse('librarytrack-extract'),
                                        data=data_url_encoded,
                                        content_type='application/x-www-form-urlencoded')

        if response.status_code == status.HTTP_201_CREATED:
            self._set_saved_lib_track_attribute(response)
        return response

    def extract_default_mine_track(self, extension=None, data_dict=None):
        if extension is None:
            url = self.SAMPLE_MINE_TRACK_DEFAULT_URL
        elif extension == 'wav':
            url = self.SAMPLE_MINE_TRACK_URLS.WAV
        elif extension == 'mp3':
            url = self.SAMPLE_MINE_TRACK_URLS.MP3
        else:
            raise ValueError(f"Unknown extension: {extension}")

        extract_data_dict = {LIB_TRACK_EXTRACT_FIELDS.URL: url}

        if data_dict is not None:
            extract_data_dict = self._merge_two_dicts(extract_data_dict, data_dict)

        response = self.extract(self._replace_none_values_by_empty_string(extract_data_dict))
        return response

    def post_lib_track_without_file(self, data_dict=None):
        return self.api_client.post(path=reverse('librarytrack-list'),
                                    data=self._replace_none_values_by_empty_string(data_dict),
                                    format='json')

    def post_lib_track(self, file_abs_path, data_dict=None) -> JsonResponse:
        with open(file_abs_path, "rb") as sample_file:
            file_field_dict = {LIB_TRACK_POST_FIELDS.FILE_OBJ: sample_file}
            if data_dict is not None:
                data_dict = self._merge_two_dicts(file_field_dict, self._replace_none_values_by_empty_string(data_dict))
            else:
                data_dict = file_field_dict
            response = self.api_client.post(path=reverse('librarytrack-list'), data=data_dict, format='multipart')
            if response.status_code == status.HTTP_201_CREATED:
                self._set_saved_lib_track_attribute(response)
            return response  # type: ignore

    def _post_lib_track_with_generic_sample(self,
                                            generic_sample_filename_without_extension,
                                            generic_sample_file_extension,
                                            data_dict=None):
        filename_with_extension = generic_sample_filename_without_extension + '.' + generic_sample_file_extension
        generic_sample_abs_path = self.generic_sample_dir_abs_path / filename_with_extension
        return self.post_lib_track(file_abs_path=generic_sample_abs_path, data_dict=data_dict)

    def post_lib_track_with_generic_sample_no_tags(self, extension='mp3', data_dict=None):
        filename_without_extension = self.LIB_TRACK_GENERIC_SAMPLES_FILENAMES_WITHOUT_EXTENSION.TAGS_NONE
        return self._post_lib_track_with_generic_sample(
            generic_sample_filename_without_extension=filename_without_extension,
            generic_sample_file_extension=extension,
            data_dict=data_dict)

    def post_lib_track_with_generic_sample_tag_album_koko_without_album_artists(self, extension='mp3', data_dict=None):
        filename_without_extension = \
            self.LIB_TRACK_GENERIC_SAMPLES_FILENAMES_WITHOUT_EXTENSION.TAGS_ALBUM_KOKO_WITHOUT_ALBUM_ARTISTS
        return self._post_lib_track_with_generic_sample(
            generic_sample_filename_without_extension=filename_without_extension,
            generic_sample_file_extension=extension,
            data_dict=data_dict)

    def post_lib_track_with_generic_sample_tag_album_artists_koko_without_album(self, data_dict=None):
        filename_without_extension = \
            self.LIB_TRACK_GENERIC_SAMPLES_FILENAMES_WITHOUT_EXTENSION.TAGS_ALBUM_ARTISTS_KOKO_WITHOUT_ALBUM
        return self._post_lib_track_with_generic_sample(
            generic_sample_filename_without_extension=filename_without_extension,
            generic_sample_file_extension='mp3',
            data_dict=data_dict)

    def post_lib_track_with_generic_sample_tags_max_length_of_a(self, extension='mp3', data_dict=None):
        filename_without_extension = \
            self.LIB_TRACK_GENERIC_SAMPLES_FILENAMES_WITHOUT_EXTENSION.TAGS_MAX_LENGTH_WITH_LETTER_A
        return self._post_lib_track_with_generic_sample(
            generic_sample_filename_without_extension=filename_without_extension,
            generic_sample_file_extension=extension,
            data_dict=data_dict)

    def post_lib_track_with_generic_sample_1_star(self, extension='mp3', data_dict=None):
        filename_without_extension = self.LIB_TRACK_GENERIC_SAMPLES_FILENAMES_WITHOUT_EXTENSION.ONE_STAR
        return self._post_lib_track_with_generic_sample(
            generic_sample_filename_without_extension=filename_without_extension,
            generic_sample_file_extension=extension,
            data_dict=data_dict)

    def post_lib_track_with_specific_sample(self, specific_sample_filename=None, data_dict=None):
        if specific_sample_filename is None:
            return self.post_lib_track(file_abs_path=None, data_dict=data_dict)
        else:
            file_abs_path = self.specific_sample_dir_abs_path / specific_sample_filename
            return self.post_lib_track(file_abs_path=file_abs_path, data_dict=data_dict)

    def put_lib_track(self, lib_track_uuid, data_dict):
        response = self.api_client.put(
            path=reverse('librarytrack-detail', kwargs={'pk': lib_track_uuid}),
            data=self._replace_none_values_by_empty_string(data_dict),
            format='json')
        if response.status_code == status.HTTP_200_OK:
            self._set_saved_lib_track_attribute(response)
        return response

    def download_lib_track(self, lib_track_uuid):
        return self.api_client.get(path=reverse('librarytrack-download', kwargs={'pk': lib_track_uuid}))

    def delete_lib_track(self, lib_track_uuid):
        return self.api_client.delete(path=reverse('librarytrack-detail', kwargs={'pk': lib_track_uuid}))
