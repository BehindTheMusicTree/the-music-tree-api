#!/usr/bin/env python
from typing import Union
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
    savedGenre: Criteria


    def extract(self, data):
        response = self.apiClient.post(
            path=reverse('librarytrack-extract'),
            data=data,
            format='json')
        
        if response.status_code == status.HTTP_201_CREATED:
            self._setSavedTrackAttribute(response)
        return response

    def postSampleTrack(self, sampleFilename=None, dataJson=None):
        if sampleFilename is None:
            return self.apiClient.post(
                path=reverse('librarytrack-list'),
                data={TRACK_ATTRIBUTES_LABEL.FILE: ''},
                format='json',)
        with open(self.inputSampleDirAbsPath + sampleFilename, "rb") as sampleFile:
            fileJson = {TRACK_ATTRIBUTES_LABEL.FILE: sampleFile}
            if dataJson is not None:
                data = self._mergeTwoJsons(fileJson, dataJson)
            else:
                data = fileJson
            response = self.apiClient.post(
                path=reverse('librarytrack-list'), data=data)
            if response.status_code == status.HTTP_201_CREATED:
                self._setSavedTrackAttribute(response)
            return response

    def putSampleTrack(self, trackUuid, data):
        response = self.apiClient.put(
            path=reverse('librarytrack-detail', kwargs={'pk': trackUuid}),
            data=data,
            format='json')
        if response.status_code == status.HTTP_200_OK:
            self._setSavedTrackAttribute(response)
        return response

    def searchMine(self, source, query):
        data = {
            'source': source,
            'query': query
        }
        return self.apiClient.get(path=reverse('mine-track'), data=data)

    def downloadTrack(self, trackUuid):
        return self.apiClient.get(path=reverse('librarytrack-download', kwargs={'pk': trackUuid}))

    def deleteTrack(self, trackUuid):
        return self.apiClient.delete(path=reverse('librarytrack-detail', kwargs={'pk': trackUuid}))

    def _setSavedTrackAttribute(self, response):
        trackUuid = response.json()[TRACK_ATTRIBUTES_LABEL.UUID]
        self.savedTrack = LibraryTrack.objects.get(uuid=trackUuid)
        if self.savedTrack.fileExists:
            self.savedTrackMetadata = AudioMetadataService.get_metadata_dict_from_file(
                file=self.savedTrack.file)

    def _mergeTwoJsons(self, json1, json2):
        json1.update(json2)
        return json1

    def postGenre(self, dataJson):
        response = self.apiClient.post(
            path=reverse('genre-list'),
            data=dataJson,
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
        self.savedGenre = Criteria.objects.get(uuid=uuid)

    def getPlaylist(self, playlistUuid):
        return self.apiClient.get(path=reverse('playlist-detail', kwargs={'pk': playlistUuid}))

    def get_albums(self):
        return self.apiClient.get(path=reverse('album-list'))