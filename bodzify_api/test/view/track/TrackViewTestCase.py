#!/usr/bin/env python
from django.urls import reverse
from rest_framework import status
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.model.track.LibraryTrack import ATTRIBUTES_LABEL as TRACK_ATTRIBUTES_LABEL
from bodzify_api.test.view.ViewTestCase import ViewTestCase
import bodzify_api.service.AudioMetadataService as AudioMetadataService


class TrackViewTestCase(ViewTestCase):

    savedTrack = None

    def extract(self, data):
        response = self.apiClient.post(
            path=reverse('librarytrack-extract'),
            data=data,
            format='json')
        if response.status_code == status.HTTP_201_CREATED:
            self._setSavedTrackData(response)
        return response

    def postSampleTrack(self, sampleFilename=None, dataJson=None):
        if sampleFilename is None:
            return self.apiClient.post(
                path=reverse('librarytrack-list'), data={TRACK_ATTRIBUTES_LABEL.FILE: ''},
                format='json')
        with open(self.inputSampleDirAbsPath + sampleFilename, "rb") as sampleFile:
            fileJson = {TRACK_ATTRIBUTES_LABEL.FILE: sampleFile}
            if dataJson is not None:
                data = self._mergeTwoJsons(fileJson, dataJson)
            else:
                data = fileJson
            response = self.apiClient.post(
                path=reverse('librarytrack-list'), data=data)
            if response.status_code == status.HTTP_201_CREATED:
                self._setSavedTrackData(response)
            return response

    def putSampleTrack(self, trackUuid, data):
        response = self.apiClient.put(
            path=reverse('librarytrack-detail', kwargs={'pk': trackUuid}),
            data=data,
            format='json')
        if response.status_code == status.HTTP_200_OK:
            self._setSavedTrackData(response)
        return response

    def downloadTrack(self, trackUuid):
        return self.apiClient.get(path=reverse('librarytrack-download', kwargs={'pk': trackUuid}))

    def deleteTrack(self, trackUuid):
        return self.apiClient.delete(path=reverse('librarytrack-detail', kwargs={'pk': trackUuid}))

    def _setSavedTrackData(self, response):
        trackUuid = response.json()[TRACK_ATTRIBUTES_LABEL.UUID]
        self.savedTrack = LibraryTrack.objects.get(uuid=trackUuid)
        self.savedTrackMetadata = AudioMetadataService.GetMetadataDictFromFile(
            file=self.savedTrack.file)

    def _mergeTwoJsons(self, json1, json2):
        json1.update(json2)
        return json1
