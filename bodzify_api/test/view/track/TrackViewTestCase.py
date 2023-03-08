#!/usr/bin/env python
from django.urls import reverse
from rest_framework import status
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.test.view.ViewTestCase import ViewTestCase


class TrackViewTestCase(ViewTestCase):
    
    postedTrack = None

    def _loginAndPostSampleTrack(self, sampleFileName=None, dataJson=None):
        self.login(self.testUser)
        if sampleFileName is None:
            return self.apiClient.post(
                path=reverse('librarytrack-list'), data={'file': None})
        with open(self.sampleDirectoryAbsolutePath + sampleFileName, "rb") as sampleFile:
            fileJson = {'file': sampleFile}
            if dataJson is not None:
                data = self._mergeTwoJsons(fileJson, dataJson)
            else:
                data = fileJson
            response = self.apiClient.post(
                path=reverse('librarytrack-list'), data=data)
            if response.status_code == status.HTTP_201_CREATED:
                trackUuid = response.json()[LibraryTrack.ATTRIBUTE_UUID_LABEL]
                self.postedTrack = LibraryTrack.objects.get(uuid=trackUuid)
                

    def _putSampleTrack(self, trackUuid, data):
        return self.apiClient.put(
            path=reverse('librarytrack-detail', kwargs={'pk': trackUuid}), data=data)

    def _downloadTrack(self, trackUuid):
        return self.apiClient.get(path=reverse('librarytrack-download', kwargs={'pk':trackUuid}))

    def _deleteTrack(self, trackUuid):        
        return self.apiClient.delete(path=reverse('librarytrack-detail', kwargs={'pk':trackUuid}))

    def _mergeTwoJsons(self, json1, json2):
        json1.update(json2)
        return json1