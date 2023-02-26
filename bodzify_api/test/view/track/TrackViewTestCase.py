#!/usr/bin/env python
from django.urls import reverse
from bodzify_api.test.view.ViewTestCase import ViewTestCase


class TrackViewTestCase(ViewTestCase):

    def postSampleTrack(self, sampleFileName, dataJson=None):
        with open(self.sampleDirectoryAbsolutePath + sampleFileName, "rb") as sampleFile:
            fileJson = {'file': sampleFile}
            if dataJson is None:
                data = self._mergeTwoJsons(fileJson, dataJson)
            else:
                data = fileJson
            return self.apiClient.post(
                path=reverse('librarytrack-list'), data=data)

    def putSampleTrack(self, trackUuid, data):
        return self.apiClient.put(
            path=reverse('librarytrack-detail', kwargs={'pk': trackUuid}), data=data)

    def downloadTrack(self, trackUuid):
        return self.apiClient.get(path=reverse('librarytrack-download', kwargs={'pk':trackUuid}))

    def deleteTrack(self, trackUuid):        
        return self.apiClient.delete(path=reverse('librarytrack-detail', kwargs={'pk':trackUuid}))

    def _mergeTwoJsons(self, json1, json2):
        json1.update(json2)
        return json1