#!/usr/bin/env python
from django.urls import reverse
from rest_framework import status
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.model.track.LibraryTrack import ATTRIBUTES_LABEL as TRACK_ATTRIBUTES_LABEL
from bodzify_api.model.criteria.Criteria import ATTRIBUTES_LABEL as CRITERIA_ATTRIBUTES_LABEL, \
    Criteria
from bodzify_api.test.view.ViewTestCase import ViewTestCase
import bodzify_api.service.AudioMetadataService as AudioMetadataService

class RESPONSE_KEYS:
    COUNT = 'count'
    NEXT = 'next'
    PREVIOUS = 'previous'
    RESULTS = 'results'

class ApiViewTestCase(ViewTestCase):

    savedTrack: LibraryTrack
    saved_genre: Criteria

    def extract(self, data):
        response = self.apiClient.post(
            path=reverse('librarytrack-extract'),
            data=data,
            format='json')
        
        if response.status_code == status.HTTP_201_CREATED:
            self._set_saved_track_attribute(response)
        return response

    def post_sample_track(self, sample_filename=None, data_json=None):
        if sample_filename is None:
            return self.apiClient.post(
                path=reverse('librarytrack-list'),
                data={TRACK_ATTRIBUTES_LABEL.FILE: ''},
                format='json',)
        with open(self.input_sample_dir_abs_path / sample_filename, "rb") as sample_file:
            file_json = {TRACK_ATTRIBUTES_LABEL.FILE: sample_file}
            if data_json is not None:
                data = self._merge_two_jsons(file_json, data_json)
            else:
                data = file_json
            response = self.apiClient.post(
                path=reverse('librarytrack-list'), data=data)
            if response.status_code == status.HTTP_201_CREATED:
                self._set_saved_track_attribute(response)
            return response

    def put_sample_track(self, track_uuid, data):
        response = self.apiClient.put(
            path=reverse('librarytrack-detail', kwargs={'pk': track_uuid}),
            data=data,
            format='json')
        if response.status_code == status.HTTP_200_OK:
            self._set_saved_track_attribute(response)
        return response

    def search_mine(self, source, query):
        data = {
            'source': source,
            'query': query
        }
        return self.apiClient.get(path=reverse('mine-track'), data=data)

    def downloadTrack(self, trackUuid):
        return self.apiClient.get(path=reverse('librarytrack-download', kwargs={'pk': trackUuid}))

    def deleteTrack(self, trackUuid):
        return self.apiClient.delete(path=reverse('librarytrack-detail', kwargs={'pk': trackUuid}))

    def _set_saved_track_attribute(self, response):
        trackUuid = response.json()[TRACK_ATTRIBUTES_LABEL.UUID]
        self.savedTrack = LibraryTrack.objects.get(uuid=trackUuid)
        if self.savedTrack.fileExists:
            self.savedTrackMetadata = AudioMetadataService.get_metadata_dict_from_file(
                file=self.savedTrack.file)

    def _merge_two_jsons(self, json1, json2):
        json1.update(json2)
        return json1
    
    def get_genres(self):
        return self.apiClient.get(path=reverse('genre-list'))

    def post_genre(self, data_json):
        response = self.apiClient.post(
            path=reverse('genre-list'),
            data=data_json,
            format='json')
        if response.status_code == status.HTTP_201_CREATED:
            self._setSavedGenreAttribute(response)
        return response

    def postSimplePlaylist(self, dataJson):
        response = self.apiClient.post(
            path=reverse('genre-list'),
            data=dataJson,
            format='json')
        if response.status_code == status.HTTP_201_CREATED:
            self._setSavedGenreAttribute(response)
        return response
            
    def _setSavedGenreAttribute(self, response):
        uuid = response.json()[CRITERIA_ATTRIBUTES_LABEL.UUID]
        self.saved_genre = Criteria.objects.get(uuid=uuid)

    def getPlaylist(self, playlistUuid):
        return self.apiClient.get(path=reverse('playlist-detail', kwargs={'pk': playlistUuid}))

    def get_albums(self):
        return self.apiClient.get(path=reverse('album-list'))