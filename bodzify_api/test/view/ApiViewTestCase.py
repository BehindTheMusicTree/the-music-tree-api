#!/usr/bin/env python

import logging

from django.urls import reverse
from rest_framework import status

import AudioMetadataManager as AudioMetadataManager
from model.criteria.Criteria import Criteria
from model.track.LibraryTrack import LibraryTrack
from test.view.ViewTestCase import ViewTestCase
from bodzify_api.serializer.track.input.schema.LibTrackSchemaExtractSerializer import FIELDS as LIB_TRACK_EXTRACT_FIELDS
from bodzify_api.serializer.track.input.schema.LibTrackSchemaPostSerializer import FIELDS as LIB_TRACK_POST_FIELDS
from serializer.track.output.libTrackDetailedSerializer import FIELDS as LIB_TRACK_GET_FIELDS
from serializer.criteria.output.CriteriaDetailedSerializer import FIELDS as CRITERIA_GET_FIELDS


logger = logging.getLogger('bodzify_api')


class RESPONSE_KEYS:
    COUNT = 'count'
    NEXT = 'next'
    PREVIOUS = 'previous'
    RESULTS = 'results'
    OVERALL_TOTAL = 'overall_total'


class ApiViewTestCase(ViewTestCase):

    MINE_TRACK_URL = "https://lasonotheque.org/UPLOAD/wav/0001.wav"

    saved_lib_track: LibraryTrack
    saved_lib_track_metadata: dict
    saved_genre: Criteria

    @staticmethod
    def _merge_two_jsons(json1, json2):
        json1.update(json2)
        return json1

    def search(self, query):
        return self.api_client.get(path=reverse('search-list'), data={'query': query})

    def extract(self, json_data):
        response = self.api_client.post(
            path=reverse('librarytrack-extract'),
            data=json_data,
            format='json')

        if response.status_code == status.HTTP_201_CREATED:
            self._set_saved_lib_track_attribute(response)
        return response

    def extract_default_mine_track(self, json_data):
        return self.extract(self._merge_two_jsons({LIB_TRACK_EXTRACT_FIELDS.URL: self.MINE_TRACK_URL}, json_data))

    def post_lib_track(self, file_abs_path=None, data_json=None):
        if file_abs_path is None:
            return self.api_client.post(
                path=reverse('librarytrack-list'),
                data={LIB_TRACK_POST_FIELDS.FILE: ''},
                format='json',)
        with open(file_abs_path, "rb") as sample_file:
            file_json = {LIB_TRACK_POST_FIELDS.FILE: sample_file}
            if data_json is not None:
                data = self._merge_two_jsons(file_json, data_json)
            else:
                data = file_json
            response = self.api_client.post(path=reverse('librarytrack-list'), data=data)
            if response.status_code == status.HTTP_201_CREATED:
                self._set_saved_lib_track_attribute(response)
            return response

    def post_sample_lib_track(self, sample_filename=None, data_json=None):
        if sample_filename is None:
            return self.post_lib_track(file_abs_path=None, data_json=data_json)
        else:
            file_abs_path = self.specific_sample_dir_abs_path / sample_filename
            return self.post_lib_track(file_abs_path=file_abs_path, data_json=data_json)

    def put_lib_track(self, lib_track_uuid, data_json):
        response = self.api_client.put(
            path=reverse('librarytrack-detail', kwargs={'pk': lib_track_uuid}),
            data=data_json,
            format='json')
        if response.status_code == status.HTTP_200_OK:
            self._set_saved_lib_track_attribute(response)
        return response

    def search_mine(self, source, query):
        data = {
            'source': source,
            'query': query
        }
        return self.api_client.get(path=reverse('mine-track-list'), data=data)

    def download_lib_track(self, lib_track_uuid):
        return self.api_client.get(path=reverse('librarytrack-download', kwargs={'pk': lib_track_uuid}))

    def delete_lib_track(self, lib_track_uuid):
        return self.api_client.delete(path=reverse('librarytrack-detail', kwargs={'pk': lib_track_uuid}))

    def get_genres(self):
        return self.api_client.get(path=reverse('genre-list'))

    def post_genre(self, data_json):
        response = self.api_client.post(path=reverse('genre-list'), data=data_json, format='json')
        if response.status_code == status.HTTP_201_CREATED:
            self._set_saved_genre_attribute(response)
        return response

    def put_genre(self, genre_uuid, data_json):
        response = self.api_client.put(
            path=reverse('genre-detail', kwargs={'pk': genre_uuid}),
            data=data_json,
            format='json')
        if response.status_code == status.HTTP_200_OK:
            self._set_saved_genre_attribute(response)
        return response

    def post_simple_playlist(self, data_json):
        response = self.api_client.post(path=reverse('simple-playlist-list'), data=data_json, format='json')
        if response.status_code == status.HTTP_201_CREATED:
            self._set_saved_genre_attribute(response)
        return response

    def put_simple_playlist(self, simple_playlist_uuid, data_json):
        response = self.api_client.put(
            path=reverse('simple-playlist-detail', kwargs={'pk': simple_playlist_uuid}), data=data_json, format='json')
        if response.status_code == status.HTTP_200_OK:
            self._set_saved_genre_attribute(response)
        return response

    def get_genre_playlist(self, playlist_uuid):
        return self.api_client.get(path=reverse('genre-playlist-detail', kwargs={'pk': playlist_uuid}))

    def get_albums(self):
        return self.api_client.get(path=reverse('album-list'))

    def _set_saved_genre_attribute(self, response):
        uuid = response.json()[CRITERIA_GET_FIELDS.UUID]
        self.saved_genre = Criteria.objects.get(uuid=uuid)

    def _set_saved_lib_track_attribute(self, response):
        lib_track_uuid = response.json()[LIB_TRACK_GET_FIELDS.UUID]
        self.saved_lib_track = LibraryTrack.objects.get(uuid=lib_track_uuid)
        if self.saved_lib_track.file_exists:
            self.saved_lib_track_metadata = AudioMetadataManager.get_metadata_dict_from_file(
                file=self.saved_lib_track.file)
