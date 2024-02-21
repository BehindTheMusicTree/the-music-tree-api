#!/usr/bin/env python

import logging

from django.urls import reverse
from rest_framework import status

import bodzify_api.AudioMetadataManager as AudioMetadataManager
from bodzify_api.model.criteria.Criteria import \
    ATTRIBUTES_LABEL as CRITERIA_ATTRIBUTES_LABEL
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.track.LibraryTrack import \
    ATTRIBUTES_LABEL as TRACK_ATTRIBUTES_LABEL
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.test.view.ViewTestCase import ViewTestCase

logger = logging.getLogger('bodzify_api')


class RESPONSE_KEYS:
    COUNT = 'count'
    NEXT = 'next'
    PREVIOUS = 'previous'
    RESULTS = 'results'
    OVERALL_TOTAL = 'overall_total'


class ApiViewTestCase(ViewTestCase):

    saved_track: LibraryTrack
    saved_genre: Criteria

    def search(self, query):
        return self.api_client.get(path=reverse('search-list'), data={'query': query})

    def extract(self, data):
        response = self.api_client.post(
            path=reverse('librarytrack-extract'),
            data=data,
            format='json')

        if response.status_code == status.HTTP_201_CREATED:
            self._set_saved_track_attribute(response)
        return response

    def post_sample_track(self, sample_filename=None, data_json=None):
        if sample_filename is None:
            return self.api_client.post(
                path=reverse('librarytrack-list'),
                data={TRACK_ATTRIBUTES_LABEL.FILE: ''},
                format='json',)
        with open(self.input_sample_dir_abs_path / sample_filename, "rb") as sample_file:
            file_json = {TRACK_ATTRIBUTES_LABEL.FILE: sample_file}
            if data_json is not None:
                data = self._merge_two_jsons(file_json, data_json)
            else:
                data = file_json
            response = self.api_client.post(
                path=reverse('librarytrack-list'), data=data)
            if response.status_code == status.HTTP_201_CREATED:
                self._set_saved_track_attribute(response)
            return response

    def put_sample_track(self, track_uuid, data_json):
        response = self.api_client.put(
            path=reverse('librarytrack-detail', kwargs={'pk': track_uuid}),
            data=data_json,
            format='json')
        if response.status_code == status.HTTP_200_OK:
            self._set_saved_track_attribute(response)
        return response

    def search_mine(self, source, query):
        data = {
            'source': source,
            'query': query
        }
        return self.api_client.get(path=reverse('mine-track-list'), data=data)

    def download_track(self, track_uuid):
        return self.api_client.get(path=reverse('librarytrack-download', kwargs={'pk': track_uuid}))

    def delete_track(self, track_uuid):
        return self.api_client.delete(path=reverse('librarytrack-detail', kwargs={'pk': track_uuid}))

    def _set_saved_track_attribute(self, response):
        track_uuid = response.json()[TRACK_ATTRIBUTES_LABEL.UUID]
        self.saved_track = LibraryTrack.objects.get(uuid=track_uuid)
        if self.saved_track.file_exists:
            self.saved_track_metadata = \
                AudioMetadataManager.get_metadata_dict_from_file(
                    file=self.saved_track.file)

    def _merge_two_jsons(self, json1, json2):
        json1.update(json2)
        return json1

    def get_genres(self):
        return self.api_client.get(path=reverse('genre-list'))

    def post_genre(self, data_json):
        response = self.api_client.post(
            path=reverse('genre-list'),
            data=data_json,
            format='json')
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
        response = self.api_client.post(
            path=reverse('genre-list'),
            data=data_json,
            format='json')
        if response.status_code == status.HTTP_201_CREATED:
            self._set_saved_genre_attribute(response)
        return response

    def _set_saved_genre_attribute(self, response):
        uuid = response.json()[CRITERIA_ATTRIBUTES_LABEL.UUID]
        self.saved_genre = Criteria.objects.get(uuid=uuid)

    def get_genre_playlist(self, playlist_uuid):
        return self.api_client.get(path=reverse('genre-playlist-detail', kwargs={'pk': playlist_uuid}))

    def get_albums(self):
        return self.api_client.get(path=reverse('album-list'))
