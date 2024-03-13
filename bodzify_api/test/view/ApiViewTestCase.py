#!/usr/bin/env python

import json
import logging
from typing import Optional

from django.urls import reverse
from rest_framework import status

from bodzify_api import AudioMetadataManager
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.playlist.SimplePlaylist import SimplePlaylist
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.test.view.ViewTestCase import ViewTestCase
from bodzify_api.serializer.track.input.schema.LibTrackExtractSchemaSerializer import FIELDS as LIB_TRACK_EXTRACT_FIELDS
from bodzify_api.serializer.track.input.schema.LibTrackPostSchemaSerializer import FIELDS as LIB_TRACK_POST_FIELDS
from bodzify_api.serializer.track.output.LibTrackDetailedSerializer import FIELDS as LIB_TRACK_GET_FIELDS
from bodzify_api.serializer.playlist.simple.output.SimplePlaylistWithTracksSerializer \
    import FIELDS as SIMPLE_PLAYLIST_GET_FIELDS


logger = logging.getLogger('bodzify_api')


class ApiViewTestCase(ViewTestCase):

    class RESPONSE_FIELDS:
        COUNT = 'count'
        NEXT = 'next'
        PREVIOUS = 'previous'
        RESULTS = 'results'
        OVERALL_TOTAL = 'overallTotal'

    class SAMPLE_MINE_TRACK_URLS:
        WAV = "http://www.canadianmusicartists.com/sample/fx02.wav"
        MP3 = "https://lasonotheque.org/UPLOAD/mp3/0001.mp3"

    SAMPLE_MINE_TRACK_DEFAULT_URL = SAMPLE_MINE_TRACK_URLS.MP3
    SAMPLE_MINE_TRACK_DEFAULT_EXTENSION = SAMPLE_MINE_TRACK_DEFAULT_URL.split('.')[-1]

    saved_lib_track: LibraryTrack
    saved_lib_track_metadata: dict
    saved_genre: Criteria
    saved_simple_playlist: SimplePlaylist

    def setUp(self, methodes_names_to_implement: Optional[list[str]] = None):
        super().setUp()
        if methodes_names_to_implement is not None:
            for method_name in methodes_names_to_implement:
                if not hasattr(self, method_name) or not callable(getattr(self, method_name)):
                    raise NotImplementedError(f"Subclasses must implement the '{method_name}' method")

    @staticmethod
    def _merge_two_jsons(json1, json2):
        json1.update(json2)
        return json1

    @staticmethod
    def _replace_none_values_by_empty_string(data_dict):
        return {k: ('' if v is None else v) for k, v in data_dict.items()}

    def search(self, query):
        return self.api_client.get(path=reverse('search-list'), data={'query': query})

    def extract(self, data_dict):
        response = self.api_client.post(
            path=reverse('librarytrack-extract'),
            data=self._replace_none_values_by_empty_string(data_dict),
            format='json')

        if response.status_code == status.HTTP_201_CREATED:  # type: ignore
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
            extract_data_dict = self._merge_two_jsons(extract_data_dict, data_dict)

        return self.extract(self._replace_none_values_by_empty_string(data_dict))

    def post_lib_track(self, file_abs_path=None, data_dict=None):
        if file_abs_path is None:
            return self.api_client.post(
                path=reverse('librarytrack-list'),
                data={LIB_TRACK_POST_FIELDS.FILE: ''},
                format='json',)
        with open(file_abs_path, "rb") as sample_file:
            file_field_dict = {LIB_TRACK_POST_FIELDS.FILE: sample_file}
            if data_dict is not None:
                data_dict = self._merge_two_jsons(file_field_dict, data_dict)
            else:
                data_dict = file_field_dict
            response = self.api_client.post(
                path=reverse('librarytrack-list'),
                data=self._replace_none_values_by_empty_string(data_dict))
            if response.status_code == status.HTTP_201_CREATED:  # type: ignore
                self._set_saved_lib_track_attribute(response)
            return response

    def post_lib_track_with_generic_sample(self,
                                           generic_sample_filename_without_extension,
                                           generic_sample_file_extension,
                                           data_dict=None):
        filename_with_extension = generic_sample_filename_without_extension + '.' + generic_sample_file_extension
        generic_sample_abs_path = self.generic_sample_dir_abs_path / filename_with_extension
        return self.post_lib_track(file_abs_path=generic_sample_abs_path, data_dict=data_dict)

    def post_lib_track_with_generic_sample_no_tags(self, extension='mp3', data_dict=None):
        filename_without_extension = ViewTestCase.LIB_TRACK_GENERIC_SAMPLES_FILENAMES_WITHOUT_EXTENSION.TAGS_NONE
        return self.post_lib_track_with_generic_sample(
            generic_sample_filename_without_extension=filename_without_extension,
            generic_sample_file_extension=extension,
            data_dict=data_dict)

    def post_lib_track_with_generic_sample_tag_album_without_album_artists(self,
                                                                           extension='mp3',
                                                                           data_dict=None):
        filename_without_extension = \
            ViewTestCase.LIB_TRACK_GENERIC_SAMPLES_FILENAMES_WITHOUT_EXTENSION.TAGS_ALBUM_WITHOUT_ALBUM_ARTISTS
        return self.post_lib_track_with_generic_sample(
            generic_sample_filename_without_extension=filename_without_extension,
            generic_sample_file_extension=extension,
            data_dict=data_dict)

    def post_lib_track_with_generic_sample_tags_max_length_of_a(self, extension='mp3', data_dict=None):
        filename_without_extension = \
            ViewTestCase.LIB_TRACK_GENERIC_SAMPLES_FILENAMES_WITHOUT_EXTENSION.TAGS_MAX_LENGTH_WITH_LETTER_A
        return self.post_lib_track_with_generic_sample(
            generic_sample_filename_without_extension=filename_without_extension,
            generic_sample_file_extension=extension,
            data_dict=data_dict)

    def post_lib_track_with_generic_sample_1_star(self, extension, data_dict=None):
        filename_without_extension = ViewTestCase.LIB_TRACK_GENERIC_SAMPLES_FILENAMES_WITHOUT_EXTENSION.ONE_STAR
        return self.post_lib_track_with_generic_sample(
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
        if response.status_code == status.HTTP_200_OK:  # type: ignore
            self._set_saved_lib_track_attribute(response)
        return response

    def search_mine(self, source, query):
        data_dict = {
            'source': source,
            'query': query
        }
        return self.api_client.get(
            path=reverse('mine-track-list'),
            data=self._replace_none_values_by_empty_string(data_dict))

    def download_lib_track(self, lib_track_uuid):
        return self.api_client.get(path=reverse('librarytrack-download', kwargs={'pk': lib_track_uuid}))

    def delete_lib_track(self, lib_track_uuid):
        return self.api_client.delete(path=reverse('librarytrack-detail', kwargs={'pk': lib_track_uuid}))

    def get_genres(self):
        return self.api_client.get(path=reverse('genre-list'))

    def post_genre(self, data_dict):
        response = self.api_client.post(path=reverse('genre-list'),
                                        data=self._replace_none_values_by_empty_string(data_dict),
                                        format='json')
        if response.status_code == status.HTTP_201_CREATED:  # type: ignore
            self._set_saved_genre_attribute(response)
        return response

    def put_genre(self, genre_uuid, data_dict):
        response = self.api_client.put(
            path=reverse('genre-detail', kwargs={'pk': genre_uuid}),
            data=self._replace_none_values_by_empty_string(data_dict),
            format='json')
        if response.status_code == status.HTTP_200_OK:  # type: ignore
            self._set_saved_genre_attribute(response)
        return response

    def post_simple_playlist(self, data_dict):
        response = self.api_client.post(path=reverse('simple-playlist-list'),
                                        data=self._replace_none_values_by_empty_string(data_dict),
                                        format='json')
        if response.status_code == status.HTTP_201_CREATED:  # type: ignore
            self._set_saved_simple_playlist_attribute(response)
        return response

    def put_simple_playlist(self, simple_playlist_uuid: str, data_dict):
        response = self.api_client.put(
            path=reverse('simple-playlist-detail', kwargs={'pk': simple_playlist_uuid}),
            data=self._replace_none_values_by_empty_string(data_dict),
            format='json')
        if response.status_code == status.HTTP_200_OK:  # type: ignore
            self._set_saved_simple_playlist_attribute(response)
        return response

    def get_genre_playlist(self, playlist_uuid):
        return self.api_client.get(path=reverse('genre-playlist-detail', kwargs={'pk': playlist_uuid}))

    def get_genre_playlists(self, data_dict=None):
        return self.api_client.get(
            path=reverse('genre-playlist-list'),
            data=self._replace_none_values_by_empty_string(data_dict))

    def get_albums(self):
        return self.api_client.get(path=reverse('album-list'))

    def _set_saved_simple_playlist_attribute(self, response):
        uuid = response.json()[SIMPLE_PLAYLIST_GET_FIELDS.UUID]
        self.saved_simple_playlist = SimplePlaylist.objects.get(playlist__uuid=uuid)

    def _set_saved_genre_attribute(self, response):
        uuid = response.json()[SIMPLE_PLAYLIST_GET_FIELDS.UUID]
        self.saved_genre = Criteria.objects.get(uuid=uuid)

    def _set_saved_lib_track_attribute(self, response):
        lib_track_uuid = response.json()[LIB_TRACK_GET_FIELDS.UUID]
        self.saved_lib_track = LibraryTrack.objects.get(uuid=lib_track_uuid)
        if self.saved_lib_track.file_exists:
            self.saved_lib_track_metadata = AudioMetadataManager.get_metadata_data_from_file(
                file=self.saved_lib_track.file)
